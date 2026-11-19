"""
Модели базы данных информационной системы развлекательного комплекса «Strike & Pocket».
Вариант 4: Бронирование дорожек в боулинге и столов в бильярдном клубе.
Студент: Верин Вадим Сергеевич, группа ИСдо-45.
Руководитель практики: Чернокрылов Леонид Сергеевич.
Ульяновск, 2026 г.
"""

from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    """Сущность: Клиент развлекательного комплекса."""
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        help_text="Фамилия клиента"
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        help_text="Имя клиента"
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Отчество",
        help_text="Отчество клиента (при наличии)"
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Номер телефона",
        help_text="Контактный номер в формате +7XXXXXXXXXX"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="E-mail для отправки чеков и уведомлений"
    )
    bonus_balance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name="Бонусный баланс (руб.)",
        help_text="Накопленные бонусные баллы"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Флаг активности учетной записи"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
        help_text="Дата и время создания профиля"
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['last_name', 'first_name']
        constraints = [
            models.CheckConstraint(
                check=Q(bonus_balance__gte=0),
                name="client_bonus_non_negative"
            )
        ]

    def __str__(self):
        fio = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            fio += f" {self.patronymic}"
        return f"{fio} ({self.phone})"


class ClubCard(models.Model):
    """Сущность: Клубная карта программы лояльности."""
    CARD_TIERS = [
        ('SILVER', 'Silver (Скидка 5%)'),
        ('GOLD', 'Gold (Скидка 10%)'),
        ('PLATINUM', 'Platinum (Скидка 15%)'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='club_cards',
        verbose_name="Владелец карты",
        help_text="Клиент, которому выдана карта"
    )
    card_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Номер карты",
        help_text="Уникальный номер карты (например, SP-SLV-00101)"
    )
    card_tier = models.CharField(
        max_length=15,
        choices=CARD_TIERS,
        default='SILVER',
        verbose_name="Уровень карты",
        help_text="Уровень привилегий программы лояльности"
    )
    discount_percent = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        verbose_name="Процент скидки",
        help_text="Размер предоставляемой скидки на аренду и бар"
    )
    issued_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата выдачи",
        help_text="Дата оформления карты"
    )
    expires_at = models.DateField(
        null=True,
        blank=True,
        verbose_name="Срок действия",
        help_text="Дата окончания действия карты (null — бессрочно)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Статус активности",
        help_text="Действительна ли карта на текущий момент"
    )

    class Meta:
        verbose_name = "Клубная карта"
        verbose_name_plural = "Клубные карты"
        ordering = ['-issued_at']
        constraints = [
            models.CheckConstraint(
                check=Q(discount_percent__gte=0) & Q(discount_percent__lte=100),
                name="card_discount_range"
            )
        ]

    def __str__(self):
        return f"Карта {self.card_number} [{self.get_card_tier_display()}] — {self.client.last_name}"


class ResourceCategory(models.Model):
    """Сущность: Категория игрового ресурса (боулинг, русский бильярд, пул, снукер)."""
    CATEGORY_CODES = [
        ('BOWLING', 'Боулинг'),
        ('RUSSIAN_BILLIARD', 'Русский бильярд (пирамида 12ft)'),
        ('AMERICAN_POOL', 'Американский пул (9ft)'),
        ('SNOOKER', 'Снукер (12ft)'),
    ]

    code = models.CharField(
        max_length=30,
        unique=True,
        choices=CATEGORY_CODES,
        verbose_name="Код категории",
        help_text="Системный строковый идентификатор категории"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование категории",
        help_text="Полное наименование игрового зала или зоны"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Краткое описание оборудования и правил"
    )
    min_players = models.PositiveIntegerField(
        default=1,
        verbose_name="Минимум игроков",
        help_text="Минимальное количество игроков на единицу ресурса"
    )
    max_players = models.PositiveIntegerField(
        default=6,
        verbose_name="Максимум игроков",
        help_text="Максимальная вместимость (на дорожку до 6, на стол до 4)"
    )

    class Meta:
        verbose_name = "Категория ресурса"
        verbose_name_plural = "Категории ресурсов"
        ordering = ['name']
        constraints = [
            models.CheckConstraint(
                check=Q(max_players__gte=F('min_players')),
                name="category_players_min_max_valid"
            )
        ]

    def __str__(self):
        return self.name


class ClubResource(models.Model):
    """Сущность: Конкретный игровой ресурс (дорожка боулинга, бильярдный стол)."""
    STATUS_CHOICES = [
        ('AVAILABLE', 'Доступен'),
        ('OCCUPIED', 'Занят'),
        ('MAINTENANCE', 'На техобслуживании'),
    ]

    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.PROTECT,
        related_name='resources',
        verbose_name="Категория ресурса",
        help_text="Привязка к типу оборудования"
    )
    resource_number = models.PositiveIntegerField(
        verbose_name="Порядковый номер",
        help_text="Номер дорожки (1-12) или стола (1-10)"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Наименование ресурса",
        help_text="Например: 'Дорожка №1 (Brunswick Pro)' или 'Стол №4 (Пирамида)'"
    )
    equipment_brand = models.CharField(
        max_length=100,
        verbose_name="Марка/модель оборудования",
        help_text="Производитель: Brunswick, QubicaAMF, Dynamic, Руптур"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE',
        verbose_name="Текущий статус",
        help_text="Статус готовности к приему гостей"
    )
    max_capacity = models.PositiveIntegerField(
        default=6,
        verbose_name="Макс. вместимость (чел.)",
        help_text="Предельное число гостей в игровой зоне"
    )

    class Meta:
        verbose_name = "Игровой ресурс"
        verbose_name_plural = "Игровые ресурсы"
        ordering = ['category', 'resource_number']
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'resource_number'],
                name="unique_resource_number_per_category"
            )
        ]

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"


class Tariff(models.Model):
    """Сущность: Тарифная сетка стоимости часа аренды."""
    DAY_TYPES = [
        ('WEEKDAY', 'Будний день (Пн–Чт)'),
        ('WEEKEND', 'Выходной/Праздник (Пт–Вс)'),
    ]
    TIME_SLOTS = [
        ('DAY', 'Дневной тариф (до 18:00)'),
        ('EVENING', 'Вечерний тариф (после 18:00)'),
    ]

    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.CASCADE,
        related_name='tariffs',
        verbose_name="Категория ресурса",
        help_text="Категория, к которой применяется ставка"
    )
    day_type = models.CharField(
        max_length=10,
        choices=DAY_TYPES,
        verbose_name="Тип дня недели"
    )
    time_slot = models.CharField(
        max_length=10,
        choices=TIME_SLOTS,
        verbose_name="Временной интервал"
    )
    price_per_hour = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Почасовая ставка (руб./час)",
        help_text="Стоимость 60 минут аренды дорожки или стола"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Действует ли данный тариф в расчетах"
    )

    class Meta:
        verbose_name = "Тарифная ставка"
        verbose_name_plural = "Тарифная сетка"
        ordering = ['category', 'day_type', 'time_slot']
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'day_type', 'time_slot'],
                name="unique_tariff_per_slot"
            ),
            models.CheckConstraint(
                check=Q(price_per_hour__gt=0),
                name="tariff_price_positive"
            )
        ]

    def __str__(self):
        return f"{self.category.name} | {self.get_day_type_display()} | {self.get_time_slot_display()} — {self.price_per_hour} руб./ч"


class Booking(models.Model):
    """Основная сущность: Бронирование игрового ресурса."""
    STATUS_CHOICES = [
        ('NEW', 'Новая заявка'),
        ('CONFIRMED', 'Подтверждена (депозит внесен)'),
        ('IN_PROGRESS', 'Сеанс игры активен'),
        ('COMPLETED', 'Сеанс завершен'),
        ('CANCELLED', 'Отменена'),
    ]

    booking_number = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Номер брони",
        help_text="Формат SP-ГГГГММДД-XXXXX"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name="Клиент",
        help_text="Клиент, оформивший бронирование"
    )
    resource = models.ForeignKey(
        ClubResource,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name="Игровой ресурс",
        help_text="Забронированная дорожка или бильярдный стол"
    )
    booking_date = models.DateField(
        verbose_name="Дата игры",
        help_text="Дата проведения сеанса"
    )
    time_start = models.TimeField(
        verbose_name="Время начала",
        help_text="Время старта игры"
    )
    time_end = models.TimeField(
        verbose_name="Время окончания",
        help_text="Время завершения игры"
    )
    duration_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.00,
        validators=[MinValueValidator(0.5)],
        verbose_name="Длительность (часов)",
        help_text="Продолжительность аренды"
    )
    players_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Количество игроков",
        help_text="Фактическое число гостей на сеансе"
    )
    rental_cost = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0.00,
        verbose_name="Стоимость аренды (руб.)",
        help_text="Базовая сумма аренды до применения скидок"
    )
    discount_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name="Сумма скидки (руб.)",
        help_text="Скидка по карте лояльности"
    )
    total_cost = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0.00,
        verbose_name="Итоговая сумма (руб.)",
        help_text="Итого к оплате с учетом скидок и бара"
    )
    deposit_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        verbose_name="Сумма предоплаты / депозита (руб.)",
        help_text="Обязательный 50% депозит в пиковые часы"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        verbose_name="Статус брони",
        help_text="Текущее состояние бронирования"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Примечания",
        help_text="Особые пожелания гостя (детские бортики, обувь и др.)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Момент оформления заказа в системе"
    )
    bar_items = models.ManyToManyField(
        'BarItem',
        through='BookingBarOrder',
        related_name='bookings',
        blank=True,
        verbose_name="Позиции бара/кухни"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-booking_date', '-time_start']
        constraints = [
            models.CheckConstraint(
                check=Q(time_end__gt=F('time_start')),
                name="booking_time_valid"
            ),
            models.CheckConstraint(
                check=Q(players_count__gt=0),
                name="booking_players_positive"
            ),
            models.CheckConstraint(
                check=Q(total_cost__gte=0),
                name="booking_total_cost_non_negative"
            ),
            models.UniqueConstraint(
                fields=['resource', 'booking_date', 'time_start'],
                name="unique_resource_time_slot"
            )
        ]

    def __str__(self):
        return f"Бронь №{self.booking_number} ({self.resource.title}, {self.booking_date} {self.time_start}-{self.time_end})"


class BarCategory(models.Model):
    """Сущность: Категория меню бара и кухни."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Категория меню",
        help_text="Например: Пицца, Закуски, Напитки, Десерты"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание категории меню"
    )
    order_priority = models.PositiveIntegerField(
        default=1,
        verbose_name="Приоритет в меню",
        help_text="Порядковый номер при выводе в каталоге"
    )

    class Meta:
        verbose_name = "Категория бара/кухни"
        verbose_name_plural = "Категории бара и кухни"
        ordering = ['order_priority', 'name']

    def __str__(self):
        return self.name


class BarItem(models.Model):
    """Сущность: Позиция меню бара или кухни развлекательного комплекса."""
    category = models.ForeignKey(
        BarCategory,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name="Категория меню",
        help_text="Раздел меню"
    )
    name = models.CharField(
        max_length=120,
        verbose_name="Наименование блюда/напитка",
        help_text="Название позиции меню"
    )
    portion_size = models.CharField(
        max_length=50,
        verbose_name="Выход порции / Объем",
        help_text="Например: '450 г', '0.5 л', '250 мл'"
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        verbose_name="Цена (руб.)",
        help_text="Розничная стоимость единицы"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступно к заказу",
        help_text="Наличие на кухне/баре"
    )

    class Meta:
        verbose_name = "Позиция меню бара"
        verbose_name_plural = "Позиции меню бара"
        ordering = ['category', 'name']
        constraints = [
            models.CheckConstraint(
                check=Q(price__gte=0),
                name="bar_item_price_non_negative"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.portion_size}) — {self.price} руб."


class BookingBarOrder(models.Model):
    """
    Связующая сущность (Many-to-Many through table):
    Заказ позиций бара и кухни, прикрепленный к бронированию дорожки/стола.
    """
    ORDER_STATUSES = [
        ('ORDERED', 'Принят кухней/баром'),
        ('PREPARING', 'Готовится'),
        ('SERVED', 'Подан к дорожке/столу'),
        ('CANCELLED', 'Отменен'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='bar_orders',
        verbose_name="Бронирование",
        help_text="Сеанс бронирования, к которому привязан заказ"
    )
    bar_item = models.ForeignKey(
        BarItem,
        on_delete=models.PROTECT,
        related_name='order_entries',
        verbose_name="Позиция меню",
        help_text="Выбранное блюдо или напиток"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество",
        help_text="Число порций"
    )
    price_at_order = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Цена фиксации (руб.)",
        help_text="Цена за единицу на момент оформления заказа"
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUSES,
        default='ORDERED',
        verbose_name="Статус заказа",
        help_text="Этап приготовления и подачи"
    )
    ordered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время заказа",
        help_text="Момент отправки заказа на кухню/бар"
    )

    class Meta:
        verbose_name = "Заказ бара к бронированию"
        verbose_name_plural = "Заказы бара к бронированиям"
        ordering = ['-ordered_at']
        constraints = [
            models.CheckConstraint(
                check=Q(quantity__gt=0),
                name="bar_order_quantity_positive"
            )
        ]

    @property
    def total_item_cost(self):
        return self.quantity * self.price_at_order

    def __str__(self):
        return f"Заказ {self.bar_item.name} x {self.quantity} к брони №{self.booking.booking_number}"


class Payment(models.Model):
    """Сущность: Финансовый платеж и фискализация по 54-ФЗ."""
    PAYMENT_TYPES = [
        ('PREPAYMENT_50', 'Предоплата 50% (Депозит бронирования)'),
        ('FINAL_PAYMENT', 'Окончательный расчет при закрытии сеанса'),
        ('FULL_PAYMENT', 'Полная предоплата (100%)'),
    ]
    PAYMENT_METHODS = [
        ('CARD', 'Банковская карта (онлайн-эквайринг)'),
        ('SBP', 'Система быстрых платежей (QR-код СБП)'),
        ('CASH', 'Наличные денежные средства (на кассе клуба)'),
    ]
    PAYMENT_STATUSES = [
        ('PENDING', 'Ожидает оплаты'),
        ('PAID', 'Успешно оплачен'),
        ('REFUNDED', 'Возврат средств'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name="Бронирование",
        help_text="Оплачиваемый сеанс бронирования"
    )
    transaction_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="ID транзакции эквайринга",
        help_text="Уникальный идентификатор платежного шлюза"
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPES,
        default='PREPAYMENT_50',
        verbose_name="Тип платежа"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='CARD',
        verbose_name="Способ оплаты"
    )
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Сумма платежа (руб.)",
        help_text="Фактически внесенная денежная сумма"
    )
    fiscal_receipt_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Номер фискального чека (54-ФЗ)",
        help_text="Номер электронного чека в ОФД"
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUSES,
        default='PAID',
        verbose_name="Статус платежа"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время транзакции"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи и фискальные чеки"
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name="payment_amount_positive"
            )
        ]

    def __str__(self):
        return f"Платеж №{self.transaction_id} ({self.amount} руб., {self.get_payment_type_display()}) — {self.get_status_display()}"
