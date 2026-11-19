from django.contrib import admin
from .models import (
    Client, ClubCard, ResourceCategory, ClubResource,
    Tariff, Booking, BarCategory, BarItem,
    BookingBarOrder, Payment
)


class ClubCardInline(admin.TabularInline):
    model = ClubCard
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'phone', 'email', 'bonus_balance', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('last_name', 'first_name', 'phone', 'email')
    inlines = [ClubCardInline]


@admin.register(ClubCard)
class ClubCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'client', 'card_tier', 'discount_percent', 'is_active', 'issued_at')
    list_filter = ('card_tier', 'is_active')
    search_fields = ('card_number', 'client__last_name', 'client__phone')


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'min_players', 'max_players')


@admin.register(ClubResource)
class ClubResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'resource_number', 'equipment_brand', 'status', 'max_capacity')
    list_filter = ('category', 'status')
    search_fields = ('title', 'equipment_brand')


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('category', 'day_type', 'time_slot', 'price_per_hour', 'is_active')
    list_filter = ('category', 'day_type', 'time_slot', 'is_active')


class BookingBarOrderInline(admin.TabularInline):
    model = BookingBarOrder
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'client', 'resource', 'booking_date', 'time_start', 'time_end', 'players_count', 'total_cost', 'deposit_amount', 'status')
    list_filter = ('status', 'booking_date', 'resource__category')
    search_fields = ('booking_number', 'client__last_name', 'client__phone')
    inlines = [BookingBarOrderInline, PaymentInline]


@admin.register(BarCategory)
class BarCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_priority')


@admin.register(BarItem)
class BarItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'portion_size', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)


@admin.register(BookingBarOrder)
class BookingBarOrderAdmin(admin.ModelAdmin):
    list_display = ('booking', 'bar_item', 'quantity', 'price_at_order', 'status', 'ordered_at')
    list_filter = ('status', 'ordered_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'payment_type', 'payment_method', 'amount', 'fiscal_receipt_number', 'status', 'created_at')
    list_filter = ('payment_type', 'payment_method', 'status')
    search_fields = ('transaction_id', 'fiscal_receipt_number', 'booking__booking_number')
