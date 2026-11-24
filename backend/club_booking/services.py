"""
Сервисный слой бизнес-логики развлекательного комплекса «Strike & Pocket».
Вариант 4: Бронирование дорожек в боулинге и столов в бильярдном клубе.
Студент: Верин Вадим Сергеевич, группа ИСдо-45.
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date, time
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import (
    Client, ClubCard, ResourceCategory, ClubResource,
    Tariff, Booking, BarItem, BookingBarOrder, Payment
)


def parse_time_obj(val):
    """Преобразование строки 'HH:MM' или объекта time в datetime.time."""
    if isinstance(val, time):
        return val
    if isinstance(val, str):
        parts = val.strip().split(':')
        return time(int(parts[0]), int(parts[1]))
    raise ValueError(f"Некорректное значение времени: {val}")


def parse_date_obj(val):
    """Преобразование строки 'YYYY-MM-DD' или объекта date в datetime.date."""
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        return datetime.strptime(val.strip(), '%Y-%m-%d').date()
    raise ValueError(f"Некорректное значение даты: {val}")


def get_day_type(booking_date):
    """
    Определение типа дня:
    Будни (Пн-Чт) -> 'WEEKDAY'
    Выходные и праздники (Пт-Вс) -> 'WEEKEND'
    """
    d = parse_date_obj(booking_date)
    # 0 = Monday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday
    return 'WEEKDAY' if d.weekday() < 4 else 'WEEKEND'


def calculate_booking_cost(resource, booking_date, time_start, time_end, club_card_number=None):
    """
    Динамический раздельный расчет стоимости сеанса игры:
    - Граница разделения тарифов: 18:00 (Дневной и Вечерний тарифы по FR-06, FR-07)
    - Учет типа дня недели (будни / выходные)
    - Учет скидки по клубной дисконтной карте (FR-17)
    - Расчет обязательного 50% депозита (FR-12)
    """
    d_date = parse_date_obj(booking_date)
    t_start = parse_time_obj(time_start)
    t_end = parse_time_obj(time_end)

    start_min = t_start.hour * 60 + t_start.minute
    end_min = t_end.hour * 60 + t_end.minute

    # Исправление BUG-05: обработка полуночи 00:00 как 24:00 (1440 мин) при вечернем бронировании
    if end_min == 0 and t_end == time(0, 0) and start_min > 0:
        end_min = 24 * 60

    if end_min <= start_min:
        raise ValidationError("Время окончания игры должно быть позже времени начала.")

    total_minutes = end_min - start_min
    total_hours = (Decimal(total_minutes) / Decimal(60)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    boundary_min = 18 * 60  # 18:00

    if end_min <= boundary_min:
        day_minutes = total_minutes
        evening_minutes = 0
    elif start_min >= boundary_min:
        day_minutes = 0
        evening_minutes = total_minutes
    else:
        day_minutes = boundary_min - start_min
        evening_minutes = end_min - boundary_min

    day_hours = (Decimal(day_minutes) / Decimal(60)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    evening_hours = (Decimal(evening_minutes) / Decimal(60)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    day_type = get_day_type(d_date)

    # Получение тарифов для категории ресурса
    category = resource.category

    tariff_day = Tariff.objects.filter(
        category=category,
        day_type=day_type,
        time_slot='DAY',
        is_active=True
    ).first()

    tariff_evening = Tariff.objects.filter(
        category=category,
        day_type=day_type,
        time_slot='EVENING',
        is_active=True
    ).first()

    day_rate = tariff_day.price_per_hour if tariff_day else Decimal('1000.00')
    evening_rate = tariff_evening.price_per_hour if tariff_evening else Decimal('1500.00')

    day_cost = (day_hours * day_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    evening_cost = (evening_hours * evening_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    rental_cost = day_cost + evening_cost

    # Проверка клубной карты
    discount_percent = Decimal('0.00')
    discount_amount = Decimal('0.00')
    card_tier_display = None
    card_obj = None

    if club_card_number:
        card = ClubCard.objects.filter(card_number=club_card_number.strip(), is_active=True).first()
        if card:
            card_obj = card
            discount_percent = card.discount_percent
            card_tier_display = card.get_card_tier_display()
            discount_amount = (rental_cost * (discount_percent / Decimal(100))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    total_rental_cost = rental_cost - discount_amount
    deposit_amount = (total_rental_cost * Decimal('0.50')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return {
        'day_type': day_type,
        'day_type_display': 'Будний день' if day_type == 'WEEKDAY' else 'Выходной/Праздничный день',
        'total_hours': total_hours,
        'day_hours': day_hours,
        'day_rate': day_rate,
        'day_cost': day_cost,
        'evening_hours': evening_hours,
        'evening_rate': evening_rate,
        'evening_cost': evening_cost,
        'rental_cost': rental_cost,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'card_tier_display': card_tier_display,
        'card_obj': card_obj,
        'total_cost': total_rental_cost,
        'deposit_amount': deposit_amount,
    }


def check_resource_availability(resource_id, booking_date, time_start, time_end, exclude_booking_id=None):
    """
    Проверка доступности игрового ресурса на заданный интервал времени (FR-11).
    Два интервала пересекаются, если start1 < end2 and end1 > start2.
    """
    d_date = parse_date_obj(booking_date)
    t_start = parse_time_obj(time_start)
    t_end = parse_time_obj(time_end)

    conflicting = Booking.objects.filter(
        resource_id=resource_id,
        booking_date=d_date,
        status__in=['NEW', 'CONFIRMED', 'IN_PROGRESS'],
        time_start__lt=t_end,
        time_end__gt=t_start
    )

    if exclude_booking_id:
        conflicting = conflicting.exclude(id=exclude_booking_id)

    is_available = not conflicting.exists()
    return is_available, list(conflicting)


def get_available_resources(category_code=None, booking_date=None, time_start=None, time_end=None):
    """Возвращает список свободных игровых ресурсов для заданного времени."""
    qs = ClubResource.objects.filter(status='AVAILABLE').select_related('category')
    if category_code:
        qs = qs.filter(category__code=category_code)

    if not (booking_date and time_start and time_end):
        return list(qs)

    d_date = parse_date_obj(booking_date)
    t_start = parse_time_obj(time_start)
    t_end = parse_time_obj(time_end)

    occupied_ids = Booking.objects.filter(
        booking_date=d_date,
        status__in=['NEW', 'CONFIRMED', 'IN_PROGRESS'],
        time_start__lt=t_end,
        time_end__gt=t_start
    ).values_list('resource_id', flat=True)

    return list(qs.exclude(id__in=occupied_ids))


def generate_booking_number(booking_date):
    """Формирование уникального номера бронирования вида SP-ГГГГММДД-XXXX."""
    d_date = parse_date_obj(booking_date)
    prefix = f"SP-{d_date.strftime('%Y%m%d')}"
    count_today = Booking.objects.filter(booking_date=d_date).count() + 1
    number = f"{prefix}-{count_today:04d}"
    # Гарантия уникальности
    suffix = 1
    while Booking.objects.filter(booking_number=number).exists():
        number = f"{prefix}-{(count_today + suffix):04d}"
        suffix += 1
    return number


def create_booking_atomic(
    client_data,
    resource_id,
    booking_date,
    time_start,
    time_end,
    players_count=1,
    club_card_number=None,
    bar_items_data=None,
    notes=""
):
    """
    Атомарное создание бронирования с защитой от состояния гонки (FR-11).
    Использует transaction.atomic() и select_for_update().
    """
    with transaction.atomic():
        # Блокировка строки ресурса
        resource = ClubResource.objects.select_for_update().get(id=resource_id)

        # Валидация лимита игроков
        players = int(players_count)
        if resource.category.code == 'BOWLING' and players > 6:
            raise ValidationError("На одну дорожку боулинга допускается не более 6 игроков (требование FR-05).")
        elif resource.category.code in ['RUSSIAN_BILLIARD', 'AMERICAN_POOL', 'SNOOKER'] and players > 4:
            raise ValidationError("На один бильярдный стол допускается не более 4 игроков.")

        # Проверка пересечения времени
        available, conflicts = check_resource_availability(resource.id, booking_date, time_start, time_end)
        if not available:
            raise ValidationError("Выбранная дорожка/стол уже забронирована на этот интервал времени.")

        # Расчет аренды
        cost_info = calculate_booking_cost(resource, booking_date, time_start, time_end, club_card_number)

        # Поиск или создание клиента
        phone = client_data.get('phone', '').strip()
        email = client_data.get('email', '').strip()
        last_name = client_data.get('last_name', '').strip() or 'Гость'
        first_name = client_data.get('first_name', '').strip() or 'Клуба'
        patronymic = client_data.get('patronymic', '').strip()

        client, _ = Client.objects.get_or_create(
            phone=phone,
            defaults={
                'last_name': last_name,
                'first_name': first_name,
                'patronymic': patronymic,
                'email': email,
            }
        )

        booking_number = generate_booking_number(booking_date)
        d_date = parse_date_obj(booking_date)
        t_start = parse_time_obj(time_start)
        t_end = parse_time_obj(time_end)

        booking = Booking.objects.create(
            booking_number=booking_number,
            client=client,
            resource=resource,
            booking_date=d_date,
            time_start=t_start,
            time_end=t_end,
            duration_hours=cost_info['total_hours'],
            players_count=players,
            rental_cost=cost_info['rental_cost'],
            discount_amount=cost_info['discount_amount'],
            total_cost=cost_info['total_cost'],
            deposit_amount=cost_info['deposit_amount'],
            status='NEW',
            notes=notes
        )

        # Добавление предзаказа бара
        bar_total = Decimal('0.00')
        if bar_items_data:
            for item_info in bar_items_data:
                item_id = item_info.get('item_id')
                qty = int(item_info.get('quantity', 1))
                if qty > 0 and item_id:
                    bar_item = BarItem.objects.get(id=item_id, is_available=True)
                    price = bar_item.price
                    # Скидка по карте распространяется и на меню
                    if cost_info['discount_percent'] > 0:
                        discounted_price = (price * (Decimal(1) - cost_info['discount_percent'] / Decimal(100))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    else:
                        discounted_price = price

                    BookingBarOrder.objects.create(
                        booking=booking,
                        bar_item=bar_item,
                        quantity=qty,
                        price_at_order=discounted_price,
                        status='ORDERED'
                    )
                    bar_total += discounted_price * qty

        # Обновление итоговой стоимости с учетом бара
        if bar_total > 0:
            booking.total_cost += bar_total
            # Депозит 50% от итоговой суммы аренды и бара
            booking.deposit_amount = (booking.total_cost * Decimal('0.50')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            booking.save(update_fields=['total_cost', 'deposit_amount'])

        # Создание предварительной записи платежа
        txn_id = f"TXN-{booking.booking_number}-{datetime.now().strftime('%H%M%S')}"
        Payment.objects.create(
            booking=booking,
            transaction_id=txn_id,
            payment_type='PREPAYMENT_50',
            payment_method='CARD',
            amount=booking.deposit_amount,
            status='PENDING'
        )

        return booking


def confirm_payment_and_fiscalize(booking_id, payment_method='CARD'):
    """
    Подтверждение оплаты депозита и фискализация чека по 54-ФЗ (FR-12).
    """
    with transaction.atomic():
        booking = Booking.objects.select_for_update().get(id=booking_id)
        payment = Payment.objects.filter(booking=booking, status='PENDING').first()

        now = datetime.now()
        fiscal_number = f"FP-{now.strftime('%Y%m%d%H%M%S')}-{booking.id:04d}"

        if not payment:
            txn_id = f"TXN-{booking.booking_number}-{now.strftime('%H%M%S')}"
            payment = Payment.objects.create(
                booking=booking,
                transaction_id=txn_id,
                payment_type='PREPAYMENT_50',
                payment_method=payment_method,
                amount=booking.deposit_amount,
                fiscal_receipt_number=fiscal_number,
                status='PAID'
            )
        else:
            payment.payment_method = payment_method
            payment.fiscal_receipt_number = fiscal_number
            payment.status = 'PAID'
            payment.save()

        booking.status = 'CONFIRMED'
        booking.save(update_fields=['status'])

        return payment
