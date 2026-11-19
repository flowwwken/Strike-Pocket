"""
Комплексный набор автоматических тестов веб-сервиса «Strike & Pocket».
Вариант 4: Бронирование дорожек в боулинге и столов в бильярдном клубе.
Студент: Верин Вадим Сергеевич, группа ИСдо-45.
"""

from decimal import Decimal
from datetime import date, time, datetime, timedelta
from django.test import TestCase, Client as HttpClient
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import (
    Client, ClubCard, ResourceCategory, ClubResource,
    Tariff, Booking, BarCategory, BarItem,
    BookingBarOrder, Payment
)
from .forms import BookingWizardForm, BookingSearchForm
from .services import (
    calculate_booking_cost, check_resource_availability,
    create_booking_atomic, confirm_payment_and_fiscalize
)


class BaseClubTestCase(TestCase):
    """Базовый класс с созданием тестового окружения (категории, ресурсы, тарифы, бар)."""

    def setUp(self):
        # 1. Категории ресурсов
        self.cat_bowling = ResourceCategory.objects.create(
            code='BOWLING',
            name='Боулинг',
            min_players=1,
            max_players=6
        )
        self.cat_pyramid = ResourceCategory.objects.create(
            code='RUSSIAN_BILLIARD',
            name='Русский бильярд (пирамида 12ft)',
            min_players=1,
            max_players=4
        )

        # 2. Игровые ресурсы
        self.lane_1 = ClubResource.objects.create(
            category=self.cat_bowling,
            resource_number=1,
            title='Дорожка №01 (Brunswick)',
            equipment_brand='Brunswick Pro GS-X',
            status='AVAILABLE',
            max_capacity=6
        )
        self.table_1 = ClubResource.objects.create(
            category=self.cat_pyramid,
            resource_number=1,
            title='Стол №01 (Пирамида 12ft)',
            equipment_brand='Руптур Магнат',
            status='AVAILABLE',
            max_capacity=4
        )

        # 3. Тарифная сетка для боулинга (будни и выходные, день и вечер)
        self.t_bowl_wd_day = Tariff.objects.create(
            category=self.cat_bowling,
            day_type='WEEKDAY',
            time_slot='DAY',
            price_per_hour=Decimal('1100.00'),
            is_active=True
        )
        self.t_bowl_wd_eve = Tariff.objects.create(
            category=self.cat_bowling,
            day_type='WEEKDAY',
            time_slot='EVENING',
            price_per_hour=Decimal('1600.00'),
            is_active=True
        )
        self.t_bowl_we_day = Tariff.objects.create(
            category=self.cat_bowling,
            day_type='WEEKEND',
            time_slot='DAY',
            price_per_hour=Decimal('1400.00'),
            is_active=True
        )
        self.t_bowl_we_eve = Tariff.objects.create(
            category=self.cat_bowling,
            day_type='WEEKEND',
            time_slot='EVENING',
            price_per_hour=Decimal('1900.00'),
            is_active=True
        )

        # 4. Клиент и клубная карта
        self.client_vadim = Client.objects.create(
            last_name='Верин',
            first_name='Вадим',
            patronymic='Сергеевич',
            phone='+79278001122',
            email='vadim.verin@mail.ru'
        )
        self.card_gold = ClubCard.objects.create(
            client=self.client_vadim,
            card_number='SP-GLD-TEST01',
            card_tier='GOLD',
            discount_percent=Decimal('10.00'),
            is_active=True
        )

        # 5. Категория бара и блюда
        self.bar_cat_pizza = BarCategory.objects.create(
            name='Пицца',
            order_priority=1
        )
        self.bar_pizza_pep = BarItem.objects.create(
            category=self.bar_cat_pizza,
            name='Пицца Пепперони',
            portion_size='550 г',
            price=Decimal('690.00'),
            is_available=True
        )

        # 6. Пользователи для тестирования АРМ
        self.staff_user = User.objects.create_user(
            username='staff_test',
            password='password123',
            is_staff=True
        )


class TariffCalculationTestCase(BaseClubTestCase):
    """Тестирование алгоритма тарификации и перехода через границу 18:00 (FR-06, FR-07, FR-17)."""

    def test_weekday_daytime_calculation(self):
        """Сеанс в будний день до 18:00 (14:00 - 17:00, 3 часа по дневному тарифу 1100 ₽)."""
        # 2026-11-23 - Понедельник (WEEKDAY)
        res = calculate_booking_cost(self.lane_1, '2026-11-23', '14:00', '17:00')
        self.assertEqual(res['day_type'], 'WEEKDAY')
        self.assertEqual(res['day_hours'], Decimal('3.00'))
        self.assertEqual(res['evening_hours'], Decimal('0.00'))
        self.assertEqual(res['rental_cost'], Decimal('3300.00'))
        self.assertEqual(res['deposit_amount'], Decimal('1650.00'))

    def test_transition_across_18_boundary(self):
        """Сеанс через границу 18:00 (17:00 - 19:00: 1ч день 1100 ₽ + 1ч вечер 1600 ₽ = 2700 ₽)."""
        res = calculate_booking_cost(self.lane_1, '2026-11-23', '17:00', '19:00')
        self.assertEqual(res['day_hours'], Decimal('1.00'))
        self.assertEqual(res['day_cost'], Decimal('1100.00'))
        self.assertEqual(res['evening_hours'], Decimal('1.00'))
        self.assertEqual(res['evening_cost'], Decimal('1600.00'))
        self.assertEqual(res['rental_cost'], Decimal('2700.00'))

    def test_discount_club_card_gold(self):
        """Применение дисконтной карты Gold (скидка 10%)."""
        res = calculate_booking_cost(self.lane_1, '2026-11-23', '17:00', '19:00', club_card_number='SP-GLD-TEST01')
        self.assertEqual(res['discount_percent'], Decimal('10.00'))
        self.assertEqual(res['discount_amount'], Decimal('270.00'))
        self.assertEqual(res['total_cost'], Decimal('2430.00'))
        self.assertEqual(res['deposit_amount'], Decimal('1215.00'))


class CapacityValidationTestCase(BaseClubTestCase):
    """Тестирование контроля лимита игроков (FR-05)."""

    def test_bowling_capacity_limit_pass(self):
        """До 6 игроков на дорожку боулинга разрешено."""
        booking = create_booking_atomic(
            client_data={'last_name': 'Тестов', 'first_name': 'Иван', 'phone': '+79270000001', 'email': 't@mail.ru'},
            resource_id=self.lane_1.id,
            booking_date='2026-11-24',
            time_start='14:00',
            time_end='16:00',
            players_count=6
        )
        self.assertIsNotNone(booking.id)
        self.assertEqual(booking.players_count, 6)

    def test_bowling_capacity_limit_fail(self):
        """7 игроков на 1 дорожку боулинга блокируется с предложением 2 дорожек (FR-05)."""
        with self.assertRaises(ValidationError):
            create_booking_atomic(
                client_data={'last_name': 'Тестов', 'first_name': 'Иван', 'phone': '+79270000002', 'email': 't2@mail.ru'},
                resource_id=self.lane_1.id,
                booking_date='2026-11-24',
                time_start='14:00',
                time_end='16:00',
                players_count=7
            )

    def test_billiard_capacity_limit_fail(self):
        """5 игроков на стол русского бильярда блокируется (лимит 4)."""
        with self.assertRaises(ValidationError):
            create_booking_atomic(
                client_data={'last_name': 'Тестов', 'first_name': 'Иван', 'phone': '+79270000003', 'email': 't3@mail.ru'},
                resource_id=self.table_1.id,
                booking_date='2026-11-24',
                time_start='14:00',
                time_end='16:00',
                players_count=5
            )


class OverbookingProtectionTestCase(BaseClubTestCase):
    """Тестирование защиты от овербукинга и пересечений временных слотов (FR-11)."""

    def test_overlapping_booking_rejected(self):
        """Попытка создать вторую бронь на пересекающийся интервал времени должна отклоняться."""
        # Первая бронь: 15:00 - 17:00
        create_booking_atomic(
            client_data={'last_name': 'Клиент1', 'first_name': 'Иван', 'phone': '+79271110001', 'email': 'c1@mail.ru'},
            resource_id=self.lane_1.id,
            booking_date='2026-11-25',
            time_start='15:00',
            time_end='17:00'
        )

        # Вторая бронь (пересекается: 16:00 - 18:00) -> Ошибка!
        with self.assertRaises(ValidationError):
            create_booking_atomic(
                client_data={'last_name': 'Клиент2', 'first_name': 'Петр', 'phone': '+79271110002', 'email': 'c2@mail.ru'},
                resource_id=self.lane_1.id,
                booking_date='2026-11-25',
                time_start='16:00',
                time_end='18:00'
            )

    def test_adjacent_booking_allowed(self):
        """Смежное бронирование (17:00 - 19:00 сразу после 15:00 - 17:00) разрешено."""
        # Первая бронь: 15:00 - 17:00
        create_booking_atomic(
            client_data={'last_name': 'Клиент1', 'first_name': 'Иван', 'phone': '+79271110001', 'email': 'c1@mail.ru'},
            resource_id=self.lane_1.id,
            booking_date='2026-11-25',
            time_start='15:00',
            time_end='17:00'
        )

        # Смежная бронь: 17:00 - 19:00 -> Должна пройти успешно
        b2 = create_booking_atomic(
            client_data={'last_name': 'Клиент2', 'first_name': 'Петр', 'phone': '+79271110002', 'email': 'c2@mail.ru'},
            resource_id=self.lane_1.id,
            booking_date='2026-11-25',
            time_start='17:00',
            time_end='19:00'
        )
        self.assertIsNotNone(b2.id)


class FullBookingFlowAndFiscalizationTestCase(BaseClubTestCase):
    """Тестирование полного сквозного цикла оформления, предзаказа бара и фискализации по 54-ФЗ."""

    def test_end_to_end_booking_flow(self):
        # 1. Оформление бронирования с предзаказом 2 пицц
        bar_order_items = [{'item_id': self.bar_pizza_pep.id, 'quantity': 2}]
        booking = create_booking_atomic(
            client_data={'last_name': 'Смирнов', 'first_name': 'Алексей', 'phone': '+79279998877', 'email': 'smirnov@mail.ru'},
            resource_id=self.lane_1.id,
            booking_date='2026-11-26',
            time_start='18:00',
            time_end='20:00',
            players_count=4,
            club_card_number='SP-GLD-TEST01',
            bar_items_data=bar_order_items,
            notes='Детские бортики на первые 3 фрейма'
        )

        self.assertTrue(booking.booking_number.startswith('SP-20261126-'))
        self.assertEqual(booking.status, 'NEW')
        self.assertEqual(booking.bar_orders.count(), 1)

        # 2. Оплата депозита и фискализация по 54-ФЗ (FR-12)
        payment = confirm_payment_and_fiscalize(booking.id, payment_method='CARD')
        self.assertEqual(payment.status, 'PAID')
        self.assertTrue(payment.fiscal_receipt_number.startswith('FP-'))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'CONFIRMED')


class WebViewsAndAPITestCase(BaseClubTestCase):
    """Тестирование доступности HTTP-страниц и REST API endpoints."""

    def setUp(self):
        super().setUp()
        self.http_client = HttpClient()

    def test_public_pages_status_200(self):
        """Проверка доступности публичных страниц веб-портала."""
        urls = [
            reverse('home'),
            reverse('catalog'),
            reverse('hall_map'),
            reverse('bar_menu'),
            reverse('booking_wizard'),
            reverse('my_bookings'),
        ]
        for url in urls:
            response = self.http_client.get(url)
            self.assertEqual(response.status_code, 200, f"Страница {url} вернула статус {response.status_code}")

    def test_api_calculate_price(self):
        """Проверка работы AJAX API расчета цены."""
        url = reverse('api_calculate_price')
        params = {
            'resource_id': self.lane_1.id,
            'date': '2026-11-23',
            'time_start': '17:00',
            'time_end': '19:00',
            'club_card': 'SP-GLD-TEST01'
        }
        response = self.http_client.get(url, params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['total_hours'], 2.0)
        self.assertEqual(data['day_hours'], 1.0)
        self.assertEqual(data['evening_hours'], 1.0)
        self.assertEqual(data['total_cost'], 2430.0)

    def test_api_check_card(self):
        """Проверка работы API валидации клубной карты."""
        url = reverse('api_check_card')
        # Валидная карта
        res_valid = self.http_client.get(url, {'card_number': 'SP-GLD-TEST01'})
        data_valid = res_valid.json()
        self.assertTrue(data_valid['valid'])
        self.assertEqual(data_valid['discount_percent'], 10.0)

        # Несуществующая карта
        res_invalid = self.http_client.get(url, {'card_number': 'NON_EXISTENT'})
        data_invalid = res_invalid.json()
        self.assertFalse(data_invalid['valid'])

    def test_staff_dashboard_access_control(self):
        """Проверка защиты АРМ Администратора (FR-18)."""
        url = reverse('staff_dashboard')
        # Без авторизации -> редирект на логин
        res_guest = self.http_client.get(url)
        self.assertEqual(res_guest.status_code, 302)

        # С авторизацией сотрудника -> 200 OK
        self.http_client.login(username='staff_test', password='password123')
        res_staff = self.http_client.get(url)
        self.assertEqual(res_staff.status_code, 200)


class FormsAndValidationTestCase(BaseClubTestCase):
    """
    Тестирование серверной валидации форм и клиентских сценариев (Занятие 9).
    Вариант 4: Ограничение 6 игроков на дорожку боулинга, формат телефона, сохранение полей.
    """

    def setUp(self):
        super().setUp()
        self.http_client = HttpClient()
        self.future_date = (date.today() + timedelta(days=25)).strftime('%Y-%m-%d')

    def test_booking_form_bowling_limit_exceeded(self):
        """Особое требование Варианта 4: на 1 дорожку боулинга не более 6 человек."""
        form_data = {
            'resource_id': self.lane_1.id,
            'booking_date': self.future_date,
            'time_start': '15:00',
            'time_end': '17:00',
            'players_count': 8,  # Превышение лимита 6 игроков!
            'last_name': 'Смирнов',
            'first_name': 'Алексей',
            'phone': '+7 (927) 123-45-67',
            'email': 'smirnov@mail.ru',
            'bar_items_json': '[]'
        }
        form = BookingWizardForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('players_count', form.errors)
        self.assertIn('не более 6 человек', form.errors['players_count'][0])

    def test_booking_form_bowling_valid_capacity(self):
        """Компания из 6 человек на дорожку боулинга — валидно."""
        form_data = {
            'resource_id': self.lane_1.id,
            'booking_date': self.future_date,
            'time_start': '15:00',
            'time_end': '17:00',
            'players_count': 6,
            'last_name': 'Смирнов',
            'first_name': 'Алексей',
            'phone': '+7 (927) 123-45-67',
            'email': 'smirnov@mail.ru',
            'bar_items_json': '[]'
        }
        form = BookingWizardForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_booking_form_phone_validation(self):
        """Серверная валидация телефонного номера."""
        # Некорректный телефон
        bad_data = {
            'resource_id': self.lane_1.id,
            'booking_date': self.future_date,
            'time_start': '14:00',
            'time_end': '16:00',
            'players_count': 4,
            'last_name': 'Петров',
            'first_name': 'Петр',
            'phone': '12345',  # Недостаточно цифр
            'email': 'petrov@mail.ru',
        }
        form = BookingWizardForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_booking_form_past_date_rejected(self):
        """Бронирование на прошедшую дату должно отклоняться."""
        past_date = (date.today() - timedelta(days=5)).strftime('%Y-%m-%d')
        bad_data = {
            'resource_id': self.lane_1.id,
            'booking_date': past_date,
            'time_start': '14:00',
            'time_end': '16:00',
            'players_count': 4,
            'last_name': 'Петров',
            'first_name': 'Петр',
            'phone': '+7 (927) 800-11-22',
            'email': 'petrov@mail.ru',
        }
        form = BookingWizardForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertIn('booking_date', form.errors)

    def test_booking_wizard_post_invalid_retains_values(self):
        """При ошибке валидации форма отображает ошибки и сохраняет введённые значения."""
        url = reverse('booking_wizard')
        post_data = {
            'resource_id': self.lane_1.id,
            'booking_date': self.future_date,
            'time_start': '17:00',
            'time_end': '19:00',
            'players_count': 9,  # Ошибка: > 6 игроков!
            'last_name': 'Кузнецов',
            'first_name': 'Николай',
            'phone': '+79275556677',
            'email': 'kuznetsov@mail.ru',
            'notes': 'Нужен столик поближе',
            'bar_items_json': '[]'
        }
        response = self.http_client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        # Проверяем сохранение введенных данных
        self.assertIn('Кузнецов', content)
        self.assertIn('Николай', content)
        self.assertIn('Нужен столик поближе', content)
        # Проверяем вывод ошибки рядом с полем
        self.assertIn('не более 6 человек', content)

    def test_booking_wizard_post_valid_redirects(self):
        """При успешной отправке происходит создание бронирования и редирект на оплату."""
        url = reverse('booking_wizard')
        post_data = {
            'resource_id': self.lane_1.id,
            'booking_date': self.future_date,
            'time_start': '17:00',
            'time_end': '19:00',
            'players_count': 4,
            'last_name': 'Кузнецов',
            'first_name': 'Николай',
            'phone': '+79275556677',
            'email': 'kuznetsov@mail.ru',
            'bar_items_json': '[]'
        }
        response = self.http_client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/payment/' in response.url)
