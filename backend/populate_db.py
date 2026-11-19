"""
Скрипт генерации тестовых данных для БД Strike & Pocket.
Создает более 35 бронирований и свыше 10 записей в каждой связанной таблице.
Студент: Верин Вадим Сергеевич, гр. ИСдо-45.
"""

import os
import sys
import django
from datetime import date, time, timedelta, datetime
from decimal import Decimal
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strike_pocket_backend.settings')
django.setup()

from club_booking.models import (
    Client, ClubCard, ResourceCategory, ClubResource,
    Tariff, Booking, BarCategory, BarItem,
    BookingBarOrder, Payment
)

def populate():
    print("Начало наполнения базы данных...")
    # Очистка таблиц в правильном порядке
    Payment.objects.all().delete()
    BookingBarOrder.objects.all().delete()
    Booking.objects.all().delete()
    ClubCard.objects.all().delete()
    Client.objects.all().delete()
    Tariff.objects.all().delete()
    ClubResource.objects.all().delete()
    ResourceCategory.objects.all().delete()
    BarItem.objects.all().delete()
    BarCategory.objects.all().delete()

    # 1. Категории ресурсов (4 шт.)
    cat_bowling = ResourceCategory.objects.create(
        code='BOWLING',
        name='Боулинг',
        description='Профессиональные дорожки Brunswick с синтетическим покрытием Anvilane и автоматическим возвратом шаров',
        min_players=1,
        max_players=6
    )
    cat_pyramid = ResourceCategory.objects.create(
        code='RUSSIAN_BILLIARD',
        name='Русский бильярд (пирамида 12ft)',
        description='Турнирные 12-футовые столы на натуральном ардезитном сланце (плита 45 мм), сукно Iwan Simonis 760',
        min_players=1,
        max_players=4
    )
    cat_pool = ResourceCategory.objects.create(
        code='AMERICAN_POOL',
        name='Американский пул (9ft)',
        description='Столы Dynamic III 9ft, утвержденные европейской федерацией EPBF, сукно Simonis 860',
        min_players=1,
        max_players=4
    )
    cat_snooker = ResourceCategory.objects.create(
        code='SNOOKER',
        name='Снукер (12ft)',
        description='Английский снукерный стол Riley Aristocrat 12ft, отборное сукно Strachan 6811 Gold',
        min_players=1,
        max_players=4
    )
    print(f"Категории ресурсов созданы: {ResourceCategory.objects.count()}")

    # 2. Игровые ресурсы (22 шт.: 12 дорожек + 6 пирамид + 3 пула + 1 снукер)
    resources = []
    # 12 дорожек боулинга
    for i in range(1, 13):
        res = ClubResource.objects.create(
            category=cat_bowling,
            resource_number=i,
            title=f"Дорожка №{i:02d}",
            equipment_brand="Brunswick Pro Anvilane GS-X",
            status='AVAILABLE',
            max_capacity=6
        )
        resources.append(res)

    # 6 столов русской пирамиды
    for i in range(1, 7):
        res = ClubResource.objects.create(
            category=cat_pyramid,
            resource_number=i,
            title=f"Стол №{i:02d} (Пирамида 12ft)",
            equipment_brand="Руптур Магнат 12ft / Ardesia",
            status='AVAILABLE',
            max_capacity=4
        )
        resources.append(res)

    # 3 стола американского пула
    for i in range(7, 10):
        res = ClubResource.objects.create(
            category=cat_pool,
            resource_number=i,
            title=f"Стол №{i:02d} (Пул 9ft)",
            equipment_brand="Dynamic III 9ft Tournament",
            status='AVAILABLE',
            max_capacity=4
        )
        resources.append(res)

    # 1 стол снукера
    res_snooker = ClubResource.objects.create(
        category=cat_snooker,
        resource_number=10,
        title="Стол №10 (Снукер 12ft)",
        equipment_brand="Riley Aristocrat Match 12ft",
        status='AVAILABLE',
        max_capacity=4
    )
    resources.append(res_snooker)
    print(f"Игровые ресурсы созданы: {ClubResource.objects.count()} (12 дорожек, 10 столов)")

    # 3. Тарифная сетка (16 записей: 4 категории * 2 типа дня * 2 слота)
    tariffs_data = [
        # Боулинг
        (cat_bowling, 'WEEKDAY', 'DAY', Decimal('1100.00')),
        (cat_bowling, 'WEEKDAY', 'EVENING', Decimal('1600.00')),
        (cat_bowling, 'WEEKEND', 'DAY', Decimal('1700.00')),
        (cat_bowling, 'WEEKEND', 'EVENING', Decimal('2200.00')),
        # Русский бильярд
        (cat_pyramid, 'WEEKDAY', 'DAY', Decimal('750.00')),
        (cat_pyramid, 'WEEKDAY', 'EVENING', Decimal('1100.00')),
        (cat_pyramid, 'WEEKEND', 'DAY', Decimal('1000.00')),
        (cat_pyramid, 'WEEKEND', 'EVENING', Decimal('1350.00')),
        # Американский пул
        (cat_pool, 'WEEKDAY', 'DAY', Decimal('600.00')),
        (cat_pool, 'WEEKDAY', 'EVENING', Decimal('900.00')),
        (cat_pool, 'WEEKEND', 'DAY', Decimal('800.00')),
        (cat_pool, 'WEEKEND', 'EVENING', Decimal('1100.00')),
        # Снукер
        (cat_snooker, 'WEEKDAY', 'DAY', Decimal('850.00')),
        (cat_snooker, 'WEEKDAY', 'EVENING', Decimal('1250.00')),
        (cat_snooker, 'WEEKEND', 'DAY', Decimal('1100.00')),
        (cat_snooker, 'WEEKEND', 'EVENING', Decimal('1500.00')),
    ]
    for cat, dt, ts, pr in tariffs_data:
        Tariff.objects.create(
            category=cat,
            day_type=dt,
            time_slot=ts,
            price_per_hour=pr,
            is_active=True
        )
    print(f"Тарифные ставки созданы: {Tariff.objects.count()}")

    # 4. Клиенты (16 клиентов)
    clients_info = [
        ("Алексеев", "Максим", "Игоревич", "+79278011234", "m.alekseev@mail.ru", Decimal('450.00')),
        ("Васильева", "Елена", "Сергеевна", "+79278022345", "elena.vas@yandex.ru", Decimal('1200.00')),
        ("Григорьев", "Артем", "Владимирович", "+79021233456", "artem.grig@gmail.com", Decimal('0.00')),
        ("Дмитриева", "Ольга", "Андреевна", "+79021244567", "olga.dmitr@mail.ru", Decimal('850.00')),
        ("Елисеев", "Денис", "Михайлович", "+79278055678", "d.eliseev@inbox.ru", Decimal('320.00')),
        ("Жданов", "Кирилл", "Олегович", "+79278066789", "k.zhdanov@yandex.ru", Decimal('2100.00')),
        ("Зайцева", "Анна", "Павловна", "+79021277890", "anna.zaytseva@mail.ru", Decimal('600.00')),
        ("Иванов", "Сергей", "Николаевич", "+79278088901", "serg.ivanov@gmail.com", Decimal('150.00')),
        ("Ковалев", "Роман", "Денисович", "+79278099012", "r.kovalev@yandex.ru", Decimal('950.00')),
        ("Лебедева", "Мария", "Константиновна", "+79021300123", "m.lebedeva@mail.ru", Decimal('1800.00')),
        ("Морозов", "Павел", "Алексеевич", "+79278111234", "p.morozov@gmail.com", Decimal('400.00')),
        ("Новиков", "Илья", "Сергеевич", "+79278122345", "i.novikov@yandex.ru", Decimal('0.00')),
        ("Орлова", "Светлана", "Валерьевна", "+79021333456", "sveta.orlova@mail.ru", Decimal('730.00')),
        ("Павлов", "Виталий", "Евгеньевич", "+79278144567", "v.pavlov@gmail.com", Decimal('1150.00')),
        ("Романов", "Владислав", "Артемович", "+79278155678", "vlad.romanov@inbox.ru", Decimal('2500.00')),
        ("Семенова", "Дарья", "Геннадьевна", "+79021366789", "daria.semenova@yandex.ru", Decimal('300.00')),
    ]
    clients = []
    for ln, fn, pat, ph, em, bon in clients_info:
        c = Client.objects.create(
            last_name=ln,
            first_name=fn,
            patronymic=pat,
            phone=ph,
            email=em,
            bonus_balance=bon,
            is_active=True
        )
        clients.append(c)
    print(f"Клиенты созданы: {Client.objects.count()}")

    # 5. Клубные карты (12 карт)
    card_tiers_plan = [
        (clients[0], "SP-SLV-00101", "SILVER", Decimal('5.00')),
        (clients[1], "SP-GLD-00201", "GOLD", Decimal('10.00')),
        (clients[3], "SP-SLV-00102", "SILVER", Decimal('5.00')),
        (clients[4], "SP-SLV-00103", "SILVER", Decimal('5.00')),
        (clients[5], "SP-PLT-00301", "PLATINUM", Decimal('15.00')),
        (clients[6], "SP-SLV-00104", "SILVER", Decimal('5.00')),
        (clients[8], "SP-GLD-00202", "GOLD", Decimal('10.00')),
        (clients[9], "SP-PLT-00302", "PLATINUM", Decimal('15.00')),
        (clients[10], "SP-SLV-00105", "SILVER", Decimal('5.00')),
        (clients[12], "SP-SLV-00106", "SILVER", Decimal('5.00')),
        (clients[13], "SP-GLD-00203", "GOLD", Decimal('10.00')),
        (clients[14], "SP-PLT-00303", "PLATINUM", Decimal('15.00')),
    ]
    for cl, cn, tr, disc in card_tiers_plan:
        ClubCard.objects.create(
            client=cl,
            card_number=cn,
            card_tier=tr,
            discount_percent=disc,
            is_active=True
        )
    print(f"Клубные карты созданы: {ClubCard.objects.count()}")

    # 6. Категории бара/кухни (5 шт.)
    bc_pizza = BarCategory.objects.create(name='Пицца из каменной печи', description='Тонкое итальянское тесто, натуральный сыр моцарелла', order_priority=1)
    bc_snacks = BarCategory.objects.create(name='Горячие закуски к дорожкам', description='Идеальный формат закусок для компании игроков', order_priority=2)
    bc_burgers = BarCategory.objects.create(name='Бургеры и сэндвичи', description='Сочные котлеты из мраморной говядины на гриле', order_priority=3)
    bc_drinks = BarCategory.objects.create(name='Безалкогольные напитки', description='Домашние морсы, лимонады и освежающие напитки', order_priority=4)
    bc_desserts = BarCategory.objects.create(name='Кофе и десерты', description='Классические чизкейки и ароматный кофе', order_priority=5)
    print(f"Категории бара созданы: {BarCategory.objects.count()}")

    # 7. Позиции меню бара (16 шт.)
    bar_items_data = [
        (bc_pizza, "Пицца Пепперони", "550 г", Decimal('690.00')),
        (bc_pizza, "Пицца Четыре сыра", "520 г", Decimal('750.00')),
        (bc_pizza, "Пицца Мясная барбекю", "600 г", Decimal('820.00')),
        (bc_pizza, "Пицца Ветчина и грибы", "540 г", Decimal('670.00')),
        (bc_snacks, "Куриные крылья Баффало", "300 г", Decimal('480.00')),
        (bc_snacks, "Сырные палочки с клюквой", "200 г", Decimal('390.00')),
        (bc_snacks, "Картофель фри классический", "150 г", Decimal('220.00')),
        (bc_snacks, "Чесночные гренки тар-тар", "180 г", Decimal('260.00')),
        (bc_snacks, "Начос с горячим сыром", "220 г", Decimal('340.00')),
        (bc_burgers, "Бургер Strike Classic", "380 г", Decimal('560.00')),
        (bc_burgers, "Чизбургер Double Beef", "420 г", Decimal('640.00')),
        (bc_drinks, "Морс клюквенный домашний", "1.0 л", Decimal('350.00')),
        (bc_drinks, "Лимонад Цитрус-Мята", "0.5 л", Decimal('280.00')),
        (bc_drinks, "Кола Strike Reserve", "0.5 л", Decimal('190.00')),
        (bc_drinks, "Чай Ассам с чабрецом", "800 мл", Decimal('320.00')),
        (bc_desserts, "Чизкейк Нью-Йорк", "160 г", Decimal('360.00')),
    ]
    bar_items = []
    for cat, nm, ps, pr in bar_items_data:
        bi = BarItem.objects.create(
            category=cat,
            name=nm,
            portion_size=ps,
            price=pr,
            is_available=True
        )
        bar_items.append(bi)
    print(f"Позиции меню бара созданы: {BarItem.objects.count()}")

    # 8. Бронирования (36 записей: 20 по боулингу, 16 по бильярду)
    # Используем реалистичные даты в октябре-ноябре 2026 года
    bookings_configs = [
        # (day_offset, start_hour, duration, res_idx, client_idx, players, status)
        # Боулинг (res_idx 0..11)
        (1, 14, 2.0, 0, 0, 4, 'COMPLETED'),   # Дорожка 1, Алексеев, дневной
        (1, 16, 1.5, 1, 1, 5, 'COMPLETED'),   # Дорожка 2, Васильева, дневной
        (1, 19, 2.0, 2, 2, 6, 'COMPLETED'),   # Дорожка 3, Григорьев, вечерний
        (2, 18, 3.0, 3, 3, 4, 'COMPLETED'),   # Дорожка 4, Дмитриева, вечерний
        (2, 20, 2.0, 4, 4, 6, 'COMPLETED'),   # Дорожка 5, Елисеев, вечерний
        (3, 13, 2.0, 5, 5, 3, 'COMPLETED'),   # Дорожка 6, Жданов, дневной
        (3, 15, 1.0, 6, 6, 4, 'COMPLETED'),   # Дорожка 7, Зайцева, дневной
        (3, 19, 2.5, 7, 7, 5, 'COMPLETED'),   # Дорожка 8, Иванов, вечерний
        (4, 17, 2.0, 8, 8, 6, 'COMPLETED'),   # Дорожка 9, Ковалев
        (4, 20, 2.0, 9, 9, 4, 'COMPLETED'),   # Дорожка 10, Лебедева
        (5, 14, 2.0, 10, 10, 5, 'COMPLETED'), # Дорожка 11, Морозов
        (5, 18, 2.0, 11, 11, 6, 'COMPLETED'), # Дорожка 12, Новиков
        (6, 12, 1.5, 0, 12, 3, 'COMPLETED'),  # Дорожка 1, Орлова
        (6, 15, 2.0, 1, 13, 5, 'COMPLETED'),  # Дорожка 2, Павлов
        (7, 18, 2.0, 2, 14, 6, 'COMPLETED'),  # Дорожка 3, Романов
        (8, 19, 2.0, 3, 15, 4, 'CONFIRMED'),  # Дорожка 4, Семенова
        (8, 21, 1.5, 4, 0, 5, 'CONFIRMED'),   # Дорожка 5, Алексеев
        (9, 15, 2.0, 5, 1, 6, 'CONFIRMED'),   # Дорожка 6, Васильева
        (9, 18, 2.0, 6, 5, 4, 'IN_PROGRESS'), # Дорожка 7, Жданов
        (10, 19, 2.0, 7, 9, 6, 'NEW'),        # Дорожка 8, Лебедева

        # Бильярд: Пирамида (res_idx 12..17), Пул (res_idx 18..20), Снукер (res_idx 21)
        (1, 15, 2.0, 12, 2, 2, 'COMPLETED'),  # Пирамида 1, Григорьев
        (1, 18, 3.0, 13, 4, 4, 'COMPLETED'),  # Пирамида 2, Елисеев
        (2, 14, 2.0, 14, 6, 2, 'COMPLETED'),  # Пирамида 3, Зайцева
        (2, 17, 2.5, 15, 8, 3, 'COMPLETED'),  # Пирамида 4, Ковалев
        (3, 16, 2.0, 16, 10, 2, 'COMPLETED'), # Пирамида 5, Морозов
        (3, 19, 2.0, 17, 12, 4, 'COMPLETED'), # Пирамида 6, Орлова
        (4, 15, 2.0, 18, 14, 2, 'COMPLETED'), # Пул 7, Романов
        (4, 18, 2.0, 19, 3, 3, 'COMPLETED'),  # Пул 8, Дмитриева
        (5, 16, 1.5, 20, 7, 2, 'COMPLETED'),  # Пул 9, Иванов
        (5, 19, 3.0, 21, 5, 2, 'COMPLETED'),  # Снукер 10, Жданов
        (6, 14, 2.0, 12, 9, 4, 'COMPLETED'),  # Пирамида 1, Лебедева
        (6, 18, 2.0, 13, 11, 2, 'COMPLETED'), # Пирамида 2, Новиков
        (7, 16, 2.0, 18, 13, 2, 'CONFIRMED'), # Пул 7, Павлов
        (7, 19, 2.5, 19, 15, 4, 'CONFIRMED'), # Пул 8, Семенова
        (8, 18, 3.0, 21, 1, 2, 'CONFIRMED'),  # Снукер 10, Васильева
        (9, 19, 2.0, 14, 0, 2, 'CANCELLED'),  # Пирамида 3, Алексеев
    ]

    base_date = date(2026, 11, 1)
    bookings = []
    
    for idx, (day_off, start_h, dur, res_idx, cl_idx, players, stat) in enumerate(bookings_configs, start=1):
        b_date = base_date + timedelta(days=day_off)
        t_start = time(start_h, 0)
        end_dt = datetime.combine(b_date, t_start) + timedelta(hours=dur)
        t_end = end_dt.time()
        
        target_res = resources[res_idx]
        target_client = clients[cl_idx]
        
        # Определяем ставку
        is_weekend = b_date.weekday() >= 4  # Пт, Сб, Вс считаем повышенными
        day_type = 'WEEKEND' if is_weekend else 'WEEKDAY'
        time_slot = 'EVENING' if start_h >= 18 else 'DAY'
        
        tariff = Tariff.objects.get(
            category=target_res.category,
            day_type=day_type,
            time_slot=time_slot
        )
        
        base_rent = tariff.price_per_hour * Decimal(str(dur))
        
        # Проверяем наличие карты у клиента
        card = target_client.club_cards.filter(is_active=True).first()
        discount_rate = card.discount_percent if card else Decimal('0.00')
        discount_amt = (base_rent * discount_rate / Decimal('100.00')).quantize(Decimal('0.01'))
        total_rent = base_rent - discount_amt
        deposit_val = (total_rent * Decimal('0.50')).quantize(Decimal('0.01')) if start_h >= 18 else Decimal('0.00')
        
        b = Booking.objects.create(
            booking_number=f"SP-202611{b_date.day:02d}-{idx:04d}",
            client=target_client,
            resource=target_res,
            booking_date=b_date,
            time_start=t_start,
            time_end=t_end,
            duration_hours=Decimal(str(dur)),
            players_count=players,
            rental_cost=base_rent,
            discount_amount=discount_amt,
            total_cost=total_rent,
            deposit_amount=deposit_val,
            status=stat,
            notes=f"Бронирование {target_res.title}. Игроков: {players}."
        )
        bookings.append(b)

    print(f"Бронирования созданы: {Booking.objects.count()} (требовалось не менее 30)")

    # 9. Заказы бара и кухни (BookingBarOrder) (50+ записей M:M through)
    bar_orders_created = 0
    for b in bookings:
        if b.status == 'CANCELLED':
            continue
        # Добавляем от 1 до 3 позиций бара к большинству броней
        items_count = random.choice([1, 2, 2, 3])
        chosen_items = random.sample(bar_items, items_count)
        bar_subtotal = Decimal('0.00')
        for item in chosen_items:
            qty = random.choice([1, 1, 2])
            price = item.price
            status = 'SERVED' if b.status in ['COMPLETED', 'IN_PROGRESS'] else 'ORDERED'
            bbo = BookingBarOrder.objects.create(
                booking=b,
                bar_item=item,
                quantity=qty,
                price_at_order=price,
                status=status
            )
            bar_subtotal += (price * qty)
            bar_orders_created += 1
        
        # Обновляем total_cost брони с учетом бара
        card = b.client.club_cards.filter(is_active=True).first()
        bar_disc = (bar_subtotal * card.discount_percent / Decimal('100.00')).quantize(Decimal('0.01')) if card else Decimal('0.00')
        b.discount_amount += bar_disc
        b.total_cost += (bar_subtotal - bar_disc)
        b.save()

    print(f"Заказы бара BookingBarOrder созданы: {BookingBarOrder.objects.count()} (связей M:M)")

    # 10. Платежи и фискальные чеки (Payment) (40+ записей)
    payments_count = 0
    for b in bookings:
        if b.status == 'CANCELLED':
            continue
        
        # 1. Если был депозит (вечерний слот)
        if b.deposit_amount > 0:
            Payment.objects.create(
                booking=b,
                transaction_id=f"TXN-DEP-{b.id:04d}-{random.randint(100000, 999999)}",
                payment_type='PREPAYMENT_50',
                payment_method=random.choice(['CARD', 'SBP']),
                amount=b.deposit_amount,
                fiscal_receipt_number=f"ФД-{random.randint(10000, 99999)}/ФП-{random.randint(10000000, 99999999)}",
                status='PAID'
            )
            payments_count += 1
        
        # 2. Если сеанс завершен — окончательный расчет
        if b.status == 'COMPLETED':
            final_due = b.total_cost - b.deposit_amount
            if final_due > 0:
                Payment.objects.create(
                    booking=b,
                    transaction_id=f"TXN-FIN-{b.id:04d}-{random.randint(100000, 999999)}",
                    payment_type='FINAL_PAYMENT',
                    payment_method=random.choice(['CARD', 'SBP', 'CASH']),
                    amount=final_due,
                    fiscal_receipt_number=f"ФД-{random.randint(10000, 99999)}/ФП-{random.randint(10000000, 99999999)}",
                    status='PAID'
                )
                payments_count += 1

    print(f"Финансовые платежи Payment созданы: {Payment.objects.count()}")
    print("Генерация данных успешно завершена!")

if __name__ == '__main__':
    populate()
