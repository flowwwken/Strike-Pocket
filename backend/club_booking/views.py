"""
Контроллеры веб-сервиса развлекательного комплекса «Strike & Pocket».
Вариант 4: Бронирование дорожек в боулинге и столов в бильярдном клубе.
Студент: Верин Вадим Сергеевич, группа ИСдо-45.
"""

import json
from decimal import Decimal
from datetime import datetime, date, timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum, Avg, Q

from .models import (
    Client, ClubCard, ResourceCategory, ClubResource,
    Tariff, Booking, BarCategory, BarItem,
    BookingBarOrder, Payment
)
from .services import (
    calculate_booking_cost, check_resource_availability,
    get_available_resources, create_booking_atomic,
    confirm_payment_and_fiscalize, parse_date_obj, parse_time_obj
)


def home_view(request):
    """Главная страница развлекательного комплекса «Strike & Pocket»."""
    categories = ResourceCategory.objects.all()
    resources_count = ClubResource.objects.count()
    bowling_count = ClubResource.objects.filter(category__code='BOWLING').count()
    billiard_count = ClubResource.objects.exclude(category__code='BOWLING').count()
    bookings_count = Booking.objects.filter(status__in=['CONFIRMED', 'COMPLETED']).count()

    # Тарифы "от" для витрины
    min_tariffs = {}
    for cat in categories:
        min_t = Tariff.objects.filter(category=cat, is_active=True).order_by('price_per_hour').first()
        min_tariffs[cat.code] = min_t.price_per_hour if min_t else Decimal('800.00')

    # Популярные блюда бара для превью
    featured_bar = BarItem.objects.filter(is_available=True)[:4]

    context = {
        'categories': categories,
        'resources_count': resources_count,
        'bowling_count': bowling_count,
        'billiard_count': billiard_count,
        'bookings_count': bookings_count,
        'min_tariffs': min_tariffs,
        'featured_bar': featured_bar,
    }
    return render(request, 'club_booking/home.html', context)


def catalog_view(request):
    """Постраничный каталог оборудования и залов с фильтрами (FR-01, FR-02)."""
    category_filter = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    resources = ClubResource.objects.select_related('category').all()

    if category_filter:
        resources = resources.filter(category__code=category_filter)
    if status_filter:
        resources = resources.filter(status=status_filter)

    # Присоединяем тарифы для каждого ресурса
    resource_cards = []
    for r in resources:
        day_t = Tariff.objects.filter(category=r.category, day_type='WEEKDAY', time_slot='DAY').first()
        eve_t = Tariff.objects.filter(category=r.category, day_type='WEEKDAY', time_slot='EVENING').first()
        weekend_eve_t = Tariff.objects.filter(category=r.category, day_type='WEEKEND', time_slot='EVENING').first()

        card_info = {
            'obj': r,
            'day_rate': day_t.price_per_hour if day_t else Decimal('1000.00'),
            'eve_rate': eve_t.price_per_hour if eve_t else Decimal('1500.00'),
            'weekend_rate': weekend_eve_t.price_per_hour if weekend_eve_t else Decimal('1800.00'),
        }

        if max_price:
            try:
                limit = Decimal(max_price)
                if card_info['day_rate'] > limit and card_info['eve_rate'] > limit:
                    continue
            except Exception:
                pass

        resource_cards.append(card_info)

    categories = ResourceCategory.objects.all()

    context = {
        'resource_cards': resource_cards,
        'categories': categories,
        'selected_category': category_filter,
        'selected_status': status_filter,
        'max_price': max_price,
    }
    return render(request, 'club_booking/catalog.html', context)


def hall_map_view(request):
    """Интерактивная векторная SVG-карта развлекательного комплекса (FR-04)."""
    resources = ClubResource.objects.select_related('category').all()
    categories = ResourceCategory.objects.all()

    context = {
        'resources': resources,
        'categories': categories,
    }
    return render(request, 'club_booking/hall_map.html', context)


def booking_wizard_view(request, resource_id=None):
    """
    Пошаговый мастер онлайн-бронирования (FR-03, FR-05, FR-06, FR-07, FR-08, FR-10, FR-11).
    """
    if request.method == 'POST':
        try:
            req_resource_id = request.POST.get('resource_id')
            booking_date = request.POST.get('booking_date')
            time_start = request.POST.get('time_start')
            time_end = request.POST.get('time_end')
            players_count = int(request.POST.get('players_count', 1))
            club_card_number = request.POST.get('club_card_number', '').strip() or None
            notes = request.POST.get('notes', '').strip()

            client_data = {
                'last_name': request.POST.get('last_name', '').strip(),
                'first_name': request.POST.get('first_name', '').strip(),
                'patronymic': request.POST.get('patronymic', '').strip(),
                'phone': request.POST.get('phone', '').strip(),
                'email': request.POST.get('email', '').strip(),
            }

            if not client_data['phone'] or not client_data['last_name'] or not client_data['first_name']:
                messages.error(request, "Пожалуйста, заполните обязательные контактные данные (Фамилия, Имя, Телефон).")
                return redirect(request.path)

            # Парсинг позиций бара
            bar_items_raw = request.POST.get('bar_items_json', '[]')
            try:
                bar_items_data = json.loads(bar_items_raw)
            except Exception:
                bar_items_data = []

            booking = create_booking_atomic(
                client_data=client_data,
                resource_id=req_resource_id,
                booking_date=booking_date,
                time_start=time_start,
                time_end=time_end,
                players_count=players_count,
                club_card_number=club_card_number,
                bar_items_data=bar_items_data,
                notes=notes
            )

            messages.success(request, f"Бронирование №{booking.booking_number} успешно создано!")
            return redirect('payment_process', booking_id=booking.id)

        except ValidationError as e:
            messages.error(request, f"Ошибка оформления: {e}")
            return redirect(request.path)
        except Exception as e:
            messages.error(request, f"Системная ошибка: {e}")
            return redirect(request.path)

    # GET запрос
    resources = ClubResource.objects.filter(status='AVAILABLE').select_related('category')
    categories = ResourceCategory.objects.all()
    bar_categories = BarCategory.objects.prefetch_related('items').all()

    selected_resource = None
    if resource_id:
        selected_resource = ClubResource.objects.filter(id=resource_id).first()

    default_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    context = {
        'resources': resources,
        'categories': categories,
        'bar_categories': bar_categories,
        'selected_resource': selected_resource,
        'default_date': default_date,
    }
    return render(request, 'club_booking/booking_wizard.html', context)


def booking_success_view(request, booking_id):
    """Страница подтверждения созданного бронирования."""
    booking = get_object_or_404(
        Booking.objects.select_related('client', 'resource', 'resource__category'),
        id=booking_id
    )
    bar_orders = booking.bar_orders.select_related('bar_item').all()
    payments = booking.payments.all()

    context = {
        'booking': booking,
        'bar_orders': bar_orders,
        'payments': payments,
    }
    return render(request, 'club_booking/booking_success.html', context)


def payment_process_view(request, booking_id):
    """Экран оплаты депозита и генерации фискального чека (FR-12)."""
    booking = get_object_or_404(
        Booking.objects.select_related('client', 'resource', 'resource__category'),
        id=booking_id
    )

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'CARD')
        payment = confirm_payment_and_fiscalize(booking_id=booking.id, payment_method=payment_method)
        messages.success(request, "Оплата депозита успешно принята! Фискальный чек сформирован.")
        return render(request, 'club_booking/payment.html', {
            'booking': booking,
            'payment': payment,
            'is_paid': True,
        })

    # GET запрос
    payment = booking.payments.first()
    is_paid = booking.status in ['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']

    context = {
        'booking': booking,
        'payment': payment,
        'is_paid': is_paid,
    }
    return render(request, 'club_booking/payment.html', context)


def my_bookings_view(request):
    """Личный кабинет и поиск бронирования гостя (FR-14)."""
    query = request.GET.get('q', '').strip()
    bookings = []

    if query:
        bookings = Booking.objects.select_related('client', 'resource', 'resource__category')\
            .prefetch_related('bar_orders__bar_item', 'payments')\
            .filter(
                Q(booking_number__icontains=query) |
                Q(client__phone__icontains=query) |
                Q(client__email__icontains=query)
            ).order_by('-booking_date', '-time_start')

    if request.method == 'POST':
        action = request.POST.get('action')
        booking_id = request.POST.get('booking_id')
        if action == 'cancel' and booking_id:
            booking = get_object_or_404(Booking, id=booking_id)
            if booking.status in ['NEW', 'CONFIRMED']:
                booking.status = 'CANCELLED'
                booking.save(update_fields=['status'])
                messages.success(request, f"Бронирование №{booking.booking_number} отменено.")
            else:
                messages.warning(request, "Невозможно отменить бронирование в текущем статусе.")
            return redirect(f"/my-bookings/?q={query}")

    context = {
        'query': query,
        'bookings': bookings,
    }
    return render(request, 'club_booking/my_bookings.html', context)


def bar_menu_view(request):
    """Каталог ресторанного меню кухни и бара (FR-08)."""
    categories = BarCategory.objects.prefetch_related('items').all()
    context = {
        'categories': categories,
    }
    return render(request, 'club_booking/bar_menu.html', context)


@staff_member_required
def staff_dashboard_view(request):
    """
    АРМ Администратора клуба с интерактивной шахматкой занятости ресурсов (FR-15, FR-16).
    """
    date_str = request.GET.get('date', '').strip()
    if date_str:
        try:
            target_date = parse_date_obj(date_str)
        except Exception:
            target_date = date.today()
    else:
        target_date = date.today()

    resources = ClubResource.objects.select_related('category').all().order_by('category_id', 'resource_number')
    bookings = Booking.objects.filter(booking_date=target_date)\
        .select_related('client', 'resource', 'resource__category')\
        .prefetch_related('bar_orders__bar_item', 'payments')

    # Сводные KPI дня
    kpi_total_revenue = bookings.filter(status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']).aggregate(s=Sum('total_cost'))['s'] or Decimal('0.00')
    kpi_bookings_count = bookings.count()
    kpi_active_count = bookings.filter(status__in=['CONFIRMED', 'IN_PROGRESS']).count()

    # Генерация тайм-слотов (с 12:00 до 02:00)
    time_slots = []
    for h in range(12, 24):
        time_slots.append(f"{h:02d}:00")
    time_slots.extend(["00:00", "01:00", "02:00"])

    context = {
        'target_date': target_date,
        'target_date_str': target_date.strftime('%Y-%m-%d'),
        'resources': resources,
        'bookings': bookings,
        'time_slots': time_slots,
        'kpi_total_revenue': kpi_total_revenue,
        'kpi_bookings_count': kpi_bookings_count,
        'kpi_active_count': kpi_active_count,
    }
    return render(request, 'club_booking/staff_dashboard.html', context)


@staff_member_required
@require_POST
def staff_change_status_view(request, booking_id):
    """Быстрое изменение статуса бронирования из АРМ Администратора."""
    booking = get_object_or_404(Booking, id=booking_id)
    new_status = request.POST.get('status')
    valid_statuses = dict(Booking.STATUS_CHOICES).keys()

    if new_status in valid_statuses:
        booking.status = new_status
        booking.save(update_fields=['status'])
        messages.success(request, f"Статус брони №{booking.booking_number} изменен на: {booking.get_status_display()}")
    else:
        messages.error(request, "Передан недопустимый статус.")

    redirect_url = request.META.get('HTTP_REFERER') or '/staff/dashboard/'
    return redirect(redirect_url)


# =========================================================================
# REST API ENDPOINTS
# =========================================================================

def api_calculate_price(request):
    """
    API динамического пересчета цены сеанса (FR-06, FR-07):
    Разделение часов до 18:00 и после 18:00, скидка по клубной карте, расчет 50% депозита.
    """
    try:
        resource_id = request.GET.get('resource_id') or request.POST.get('resource_id')
        booking_date = request.GET.get('date') or request.POST.get('date')
        time_start = request.GET.get('time_start') or request.POST.get('time_start')
        time_end = request.GET.get('time_end') or request.POST.get('time_end')
        club_card = request.GET.get('club_card') or request.POST.get('club_card')

        if not (resource_id and booking_date and time_start and time_end):
            return JsonResponse({'error': 'Не переданы обязательные параметры.'}, status=400)

        resource = get_object_or_404(ClubResource, id=resource_id)
        calc = calculate_booking_cost(resource, booking_date, time_start, time_end, club_card)

        # Конвертация Decimal в float/str для JSON
        data = {
            'status': 'success',
            'day_type': calc['day_type'],
            'day_type_display': calc['day_type_display'],
            'total_hours': float(calc['total_hours']),
            'day_hours': float(calc['day_hours']),
            'day_rate': float(calc['day_rate']),
            'day_cost': float(calc['day_cost']),
            'evening_hours': float(calc['evening_hours']),
            'evening_rate': float(calc['evening_rate']),
            'evening_cost': float(calc['evening_cost']),
            'rental_cost': float(calc['rental_cost']),
            'discount_percent': float(calc['discount_percent']),
            'discount_amount': float(calc['discount_amount']),
            'card_tier_display': calc['card_tier_display'],
            'total_cost': float(calc['total_cost']),
            'deposit_amount': float(calc['deposit_amount']),
        }
        return JsonResponse(data)

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f"Ошибка расчета: {str(e)}"}, status=500)


def api_available_resources(request):
    """
    API получения списка свободных ресурсов на дату и время (FR-03).
    """
    category_code = request.GET.get('category')
    booking_date = request.GET.get('date')
    time_start = request.GET.get('time_start')
    time_end = request.GET.get('time_end')

    resources = get_available_resources(category_code, booking_date, time_start, time_end)

    data = [
        {
            'id': r.id,
            'title': r.title,
            'category_code': r.category.code,
            'category_name': r.category.name,
            'resource_number': r.resource_number,
            'max_capacity': r.max_capacity,
            'equipment_brand': r.equipment_brand,
        }
        for r in resources
    ]
    return JsonResponse({'status': 'success', 'resources': data})


def api_check_card(request):
    """
    API валидации клубной карты (FR-17).
    """
    card_number = request.GET.get('card_number', '').strip()
    if not card_number:
        return JsonResponse({'valid': False, 'message': 'Номер карты не указан.'})

    card = ClubCard.objects.filter(card_number=card_number, is_active=True).select_related('client').first()
    if card:
        return JsonResponse({
            'valid': True,
            'card_number': card.card_number,
            'card_tier': card.card_tier,
            'card_tier_display': card.get_card_tier_display(),
            'discount_percent': float(card.discount_percent),
            'client_name': f"{card.client.last_name} {card.client.first_name}",
        })
    else:
        return JsonResponse({'valid': False, 'message': 'Карта не найдена или заблокирована.'})


def api_bar_items(request):
    """API получения позиций меню бара."""
    items = BarItem.objects.filter(is_available=True).select_related('category')
    data = [
        {
            'id': item.id,
            'category': item.category.name,
            'name': item.name,
            'portion_size': item.portion_size,
            'price': float(item.price),
        }
        for item in items
    ]
    return JsonResponse({'status': 'success', 'items': data})


def about_view(request):
    """Статическая страница: О комплексе Strike & Pocket, правила, тарифы день/вечер и стандарты оборудования."""
    categories = ResourceCategory.objects.all()
    tariffs = Tariff.objects.filter(is_active=True).select_related('category').order_by('category', 'day_type', 'time_slot')
    
    context = {
        'categories': categories,
        'tariffs': tariffs,
    }
    return render(request, 'club_booking/about.html', context)


def check_booking_view(request):
    """Страница поиска и оперативной проверки статуса бронирования по коду или телефону (FR-14)."""
    query = request.GET.get('q', '').strip()
    booking = None
    time_diff_hours = None
    can_cancel = False

    if query:
        booking = Booking.objects.select_related('client', 'resource', 'resource__category')\
            .prefetch_related('bar_orders__bar_item', 'payments')\
            .filter(
                Q(booking_number__iexact=query) |
                Q(client__phone__icontains=query)
            ).order_by('-booking_date', '-time_start').first()

        if booking and booking.status in ['NEW', 'CONFIRMED']:
            now_dt = datetime.now()
            booking_dt = datetime.combine(booking.booking_date, booking.time_start)
            time_diff = booking_dt - now_dt
            time_diff_hours = time_diff.total_seconds() / 3600.0
            can_cancel = time_diff_hours >= 2.0

    if request.method == 'POST' and booking:
        action = request.POST.get('action')
        if action == 'cancel':
            now_dt = datetime.now()
            booking_dt = datetime.combine(booking.booking_date, booking.time_start)
            if (booking_dt - now_dt).total_seconds() / 3600.0 >= 2.0:
                booking.status = 'CANCELLED'
                booking.save(update_fields=['status'])
                messages.success(request, f"Бронирование #{booking.booking_number} успешно отменено. Средства будут возвращены.")
            else:
                messages.error(request, "Отмена менее чем за 2 часа невозможна онлайн. Пожалуйста, обратитесь к администратору по телефону.")
            return redirect(f"/check-booking/?q={booking.booking_number}")

    context = {
        'query': query,
        'booking': booking,
        'time_diff_hours': time_diff_hours,
        'can_cancel': can_cancel,
    }
    return render(request, 'club_booking/check_booking.html', context)


def profile_view(request):
    """Личный кабинет постоянного клиента, виртуальная клубная карта лояльности и история бронирований."""
    # Для демонстрации и тестирования используем первого клиента из БД
    phone = request.GET.get('phone', '').strip()
    if phone:
        client = Client.objects.filter(phone__icontains=phone).first()
    else:
        client = Client.objects.filter(club_cards__isnull=False).first() or Client.objects.first()

    club_card = client.club_cards.filter(is_active=True).first() if client else None
    
    # История бронирований с пагинацией по 20 записей
    bookings_qs = Booking.objects.filter(client=client).select_related('resource', 'resource__category').order_by('-booking_date', '-time_start') if client else Booking.objects.none()
    paginator = Paginator(bookings_qs, 20)
    page = request.GET.get('page')
    try:
        bookings_page = paginator.page(page)
    except PageNotAnInteger:
        bookings_page = paginator.page(1)
    except EmptyPage:
        bookings_page = paginator.page(paginator.num_pages)

    context = {
        'client': client,
        'club_card': club_card,
        'bookings': bookings_page,
    }
    return render(request, 'club_booking/profile.html', context)


def booking_create_view(request):
    """Отдельная страница формы быстрого бронирования слота."""
    # Будет расширена формой Django на Занятии 9
    return redirect('booking_wizard')

