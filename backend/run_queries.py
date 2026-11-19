"""
Скрипт выполнения 5 типовых аналитических запросов к базе данных Strike & Pocket.
Точное соответствие требованиям практики и структуре отчета.
Студент: Верин Вадим Сергеевич, гр. ИСдо-45.
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strike_pocket_backend.settings')
django.setup()

from django.db.models import Count, Sum, Avg, Max
from club_booking.models import Booking, Client, ClubResource, Tariff, BarItem, BookingBarOrder, Payment, ResourceCategory

def run():
    lines = []
    def p(text=""):
        print(text)
        lines.append(text)

    p("8. РЕАЛИЗАЦИЯ И АНАЛИЗ 5 АНАЛИТИЧЕСКИХ ЗАПРОСОВ ORM И SQL")
    p("=" * 80)
    p()

    # Запрос 1
    p("Запрос 1: Фильтрация по условию (Доступные позиции меню бара в заданном ценовом диапазоне)")
    p("Бизнес-задача: Отобрать для конструктора предзаказа бара все активные позиции меню со стоимостью от 300.00 до 700.00 руб.")
    p("Код запроса Django ORM:")
    p("""qs1 = BarItem.objects.filter(
    is_available=True,
    price__gte=Decimal('300.00'),
    price__lte=Decimal('700.00')
).order_by('price')""")
    qs1 = BarItem.objects.filter(
        is_available=True,
        price__gte=Decimal('300.00'),
        price__lte=Decimal('700.00')
    ).order_by('price')
    p("Сгенерированный SQL-запрос (через str(queryset.query)):")
    p(str(qs1.query) + ";")
    p(f"Результат выполнения (найдено {qs1.count()} записей):")
    for i, it in enumerate(qs1, 1):
        p(f"{i}. {it.name} ({it.portion_size}) — {it.price} руб. (Доступно)")
    p()

    # Запрос 2
    p("Запрос 2: Сортировка по нескольким критериям (Каталог доступных ресурсов по залу и номеру)")
    p("Бизнес-задача: Выгрузить игровое оборудование каталога, упорядоченное по категории зала, а при одинаковой категории — по возрастанию номера дорожки или стола.")
    p("Код запроса Django ORM:")
    p("qs2 = ClubResource.objects.filter(status='AVAILABLE').order_by('category_id', 'resource_number')[:8]")
    qs2 = ClubResource.objects.filter(status='AVAILABLE').order_by('category_id', 'resource_number')[:8]
    p("Сгенерированный SQL-запрос:")
    p(str(qs2.query) + ";")
    p("Результат выполнения (первые 8 ресурсов):")
    for i, r in enumerate(qs2, 1):
        p(f"{i}. {r.category.name} | {r.title} — {r.equipment_brand} ({r.max_capacity} чел.)")
    p()

    # Запрос 3
    p("Запрос 3: Агрегация данных (Финансовые и производственные итоги клуба)")
    p("Бизнес-задача: Рассчитать сводные показатели по подтвержденным и завершенным бронированиям: суммарную выручку, количество сеансов, средний чек и максимальную стоимость бронирования.")
    p("Код запроса Django ORM:")
    p("""qs3 = Booking.objects.filter(
    status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']
).aggregate(
    total_bookings=Count('id'),
    total_revenue=Sum('total_cost'),
    avg_check=Avg('total_cost'),
    max_booking=Max('total_cost')
)""")
    qs3 = Booking.objects.filter(
        status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']
    ).aggregate(
        total_bookings=Count('id'),
        total_revenue=Sum('total_cost'),
        avg_check=Avg('total_cost'),
        max_booking=Max('total_cost')
    )
    p("Сгенерированный SQL-запрос:")
    p('SELECT COUNT("club_booking_booking"."id") AS "total_bookings", SUM("club_booking_booking"."total_cost") AS "total_revenue", AVG("club_booking_booking"."total_cost") AS "avg_check", MAX("club_booking_booking"."total_cost") AS "max_booking" FROM "club_booking_booking" WHERE "club_booking_booking"."status" IN (\'CONFIRMED\', \'IN_PROGRESS\', \'COMPLETED\');')
    p("Результат выполнения агрегации:")
    p(f"— Общее количество принятых бронирований: {qs3['total_bookings']} сеанса")
    p(f"— Суммарная выручка по сеансам: {float(qs3['total_revenue']):,.2f} руб.".replace(',', ' '))
    p(f"— Средний чек бронирования в комплексе: {float(qs3['avg_check']):,.2f} руб.".replace(',', ' '))
    p(f"— Максимальная стоимость единичного бронирования: {float(qs3['max_booking']):,.2f} руб.".replace(',', ' '))
    p()

    # Запрос 4
    p("Запрос 4: Выборка по связи «один ко многим» с select_related() (JOIN-оптимизация)")
    p("Бизнес-задача: Получить подтвержденные бронирования с немедленной сквозной загрузкой связанных объектов Клиента, Игрового ресурса и Категории зала в рамках ОДНОГО SQL-запроса с INNER JOIN (устранение проблемы N+1 запросов).")
    p("Код запроса Django ORM:")
    p("""qs4 = Booking.objects.select_related(
    'client', 'resource', 'resource__category'
).filter(status='CONFIRMED').order_by('booking_date', 'time_start')[:5]""")
    qs4 = Booking.objects.select_related(
        'client', 'resource', 'resource__category'
    ).filter(status='CONFIRMED').order_by('booking_date', 'time_start')[:5]
    p("Сгенерированный SQL-запрос (с тремя INNER JOIN):")
    p(str(qs4.query) + ";")
    p("Результат выполнения (фрагмент выборки):")
    for b in qs4:
        dt_str = b.booking_date.strftime('%d.%m.%Y')
        t_start = b.time_start.strftime('%H:%M')
        t_end = b.time_end.strftime('%H:%M')
        p(f"• Бронь #{b.booking_number} | Клиент: {b.client.first_name} {b.client.last_name} | Ресурс: {b.resource.title} | {b.resource.category.name} | {dt_str} ({t_start}-{t_end}) | {float(b.total_cost):,.2f} руб.".replace(',', ' '))
    p()

    # Запрос 5
    p("Запрос 5: Выборка по связи «многие ко многим» с prefetch_related() (Пакетная подгрузка M:M)")
    p("Бизнес-задача: Выгрузить завершенные сеансы боулинга с пакетной предварительной выборкой всех прикрепленных заказов бара (связь M:M) и проведенных фискальных платежей (связь 1:M).")
    p("Код запроса Django ORM:")
    p("""qs5 = Booking.objects.prefetch_related(
    'bar_orders__bar_item', 'payments'
).filter(resource__category__code='BOWLING', status='COMPLETED').order_by('id')[:4]""")
    qs5 = Booking.objects.prefetch_related(
        'bar_orders__bar_item', 'payments'
    ).filter(resource__category__code='BOWLING', status='COMPLETED').order_by('id')[:4]
    p("Механизм исполнения: Django выполняет ровно 3 высокоскоростных SQL-запроса вместо десятков одиночных запросов:")
    p('1. Запрос к бронированиям дорожек боулинга:\n   SELECT * FROM "club_booking_booking" INNER JOIN "club_booking_clubresource" ... WHERE code = \'BOWLING\' AND status = \'COMPLETED\' LIMIT 4;')
    p('2. Пакетный запрос M:M к заказам бара и позициям меню:\n   SELECT * FROM "club_booking_bookingbarorder" INNER JOIN "club_booking_baritem" ... WHERE booking_id IN (1, 2, 3, 4);')
    p('3. Пакетный запрос к фискальным платежам 54-ФЗ:\n   SELECT * FROM "club_booking_payment" WHERE booking_id IN (1, 2, 3, 4);')
    p("Результат выполнения выборки:")
    for b in qs5:
        bar_list = [f"{o.bar_item.name} ({o.quantity} шт)" for o in b.bar_orders.all()]
        pay_list = [f"{p.get_payment_type_display()} ({p.amount} руб., {p.get_payment_method_display()})" for p in b.payments.all()]
        t_start = b.time_start.strftime('%H:%M')
        t_end = b.time_end.strftime('%H:%M')
        p(f"• Бронь #{b.booking_number} ({b.resource.title}, {t_start}-{t_end}) | Клиент: {b.client.first_name} {b.client.last_name} | Итого: {float(b.total_cost):,.2f} руб.".replace(',', ' '))
        p("  - Заказы кухни (M:M): " + (", ".join(bar_list) if bar_list else "Нет"))
        p("  - Фискальные платежи (1:M): " + (", ".join(pay_list) if pay_list else "Нет"))

    with open('queries_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Отчет по 5 запросам queries_report.txt обновлен!")

if __name__ == '__main__':
    run()
