import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strike_pocket_backend.settings')
django.setup()

from django.db.models import Count, Sum, Avg, Max
from club_booking.models import Booking, Client, ClubResource, Tariff, BarItem, BookingBarOrder, Payment, ResourceCategory

print("=== TEST QUERY 1: Filter Bar Items ===")
qs1 = BarItem.objects.filter(
    is_available=True,
    price__gte=Decimal('300.00'),
    price__lte=Decimal('700.00')
).order_by('price')
print("SQL 1:", str(qs1.query))
for i, item in enumerate(qs1, 1):
    print(f"{i}. {item.name} ({item.portion_size}) — {item.price} руб. (Доступно)")

print("\n=== TEST QUERY 2: Multi-column Sort Resources ===")
qs2 = ClubResource.objects.filter(status='AVAILABLE').order_by('category_id', 'resource_number')[:8]
print("SQL 2:", str(qs2.query))
for i, r in enumerate(qs2, 1):
    print(f"{i}. {r.category.name} | {r.title} — {r.equipment_brand} ({r.max_capacity} чел.)")

print("\n=== TEST QUERY 3: Aggregate Bookings ===")
qs3 = Booking.objects.filter(
    status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']
).aggregate(
    total_bookings=Count('id'),
    total_revenue=Sum('total_cost'),
    avg_check=Avg('total_cost'),
    max_check=Max('total_cost')
)
print("Aggregates:", qs3)

print("\n=== TEST QUERY 4: 1:M select_related ===")
qs4 = Booking.objects.select_related(
    'client', 'resource', 'resource__category'
).filter(status='CONFIRMED').order_by('booking_date', 'time_start')[:5]
print("SQL 4:", str(qs4.query))
for b in qs4:
    dt_str = b.booking_date.strftime('%d.%m.%Y')
    t_start = b.time_start.strftime('%H:%M')
    t_end = b.time_end.strftime('%H:%M')
    print(f"• Бронь #{b.booking_number} | Клиент: {b.client.first_name} {b.client.last_name} | Ресурс: {b.resource.title} | {b.resource.category.name} | {dt_str} ({t_start}-{t_end}) | {b.total_cost} руб.")

print("\n=== TEST QUERY 5: M:M prefetch_related ===")
qs5 = Booking.objects.prefetch_related(
    'bar_orders__bar_item', 'payments'
).filter(resource__category__code='BOWLING', status='COMPLETED').order_by('id')[:4]
print("SQL 5 main:", str(qs5.query))
for b in qs5:
    bar_list = [f"{o.bar_item.name} ({o.quantity} шт)" for o in b.bar_orders.all()]
    pay_list = [f"{p.get_payment_type_display()} ({p.amount} руб., {p.get_payment_method_display()})" for p in b.payments.all()]
    t_start = b.time_start.strftime('%H:%M')
    t_end = b.time_end.strftime('%H:%M')
    print(f"• Бронь #{b.booking_number} ({b.resource.title}, {t_start}-{t_end}) | Клиент: {b.client.first_name} {b.client.last_name} | Итого: {b.total_cost} руб.")
    print("  - Заказы кухни (M:M):", ", ".join(bar_list) if bar_list else "Нет")
    print("  - Фискальные платежи (1:M):", ", ".join(pay_list) if pay_list else "Нет")
