"""
Формы веб-сервиса развлекательного комплекса «Strike & Pocket».
Вариант 4: Бронирование дорожек в боулинге и столов в бильярдном клубе.
Студент: Верин Вадим Сергеевич, группа ИСдо-45.
"""

import re
import json
from decimal import Decimal
from datetime import date, datetime, time, timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import Client, ClubCard, ClubResource, ResourceCategory, Booking, BarItem
from .services import check_resource_availability, parse_date_obj, parse_time_obj


class BookingWizardForm(forms.Form):
    """
    Основная форма онлайн-бронирования дорожек и бильярдных столов (FR-03, FR-05, FR-07, FR-10).
    Включает серверную валидацию специального требования Варианта 4 (лимит 6 гостей на дорожку).
    """
    resource_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
        error_messages={'required': 'Пожалуйста, выберите дорожку или стол на схеме зала.'}
    )
    booking_date = forms.DateField(
        label="Дата сеанса",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control-custom',
            'id': 'dateInput'
        }),
        required=True,
        error_messages={'required': 'Укажите дату проведения игры.'}
    )
    time_start = forms.CharField(
        label="Время начала",
        widget=forms.Select(attrs={
            'class': 'form-select-custom',
            'id': 'startTimeInput'
        }, choices=[
            ('12:00', '12:00 (Дневной тариф)'),
            ('13:00', '13:00'),
            ('14:00', '14:00'),
            ('15:00', '15:00'),
            ('16:00', '16:00'),
            ('17:00', '17:00 (Стык тарифов)'),
            ('18:00', '18:00 (Вечерний тариф)'),
            ('19:00', '19:00'),
            ('20:00', '20:00'),
            ('21:00', '21:00'),
            ('22:00', '22:00'),
            ('23:00', '23:00'),
        ]),
        required=True,
        initial='17:00'
    )
    time_end = forms.CharField(
        label="Время окончания",
        widget=forms.Select(attrs={
            'class': 'form-select-custom',
            'id': 'endTimeInput'
        }, choices=[
            ('13:00', '13:00 (1 час)'),
            ('14:00', '14:00 (2 часа)'),
            ('15:00', '15:00 (3 часа)'),
            ('16:00', '16:00'),
            ('17:00', '17:00'),
            ('18:00', '18:00'),
            ('19:00', '19:00 (2 часа)'),
            ('20:00', '20:00 (3 часа)'),
            ('21:00', '21:00'),
            ('22:00', '22:00'),
            ('23:00', '23:00'),
            ('00:00', '00:00'),
        ]),
        required=True,
        initial='19:00'
    )
    players_count = forms.IntegerField(
        label="Количество игроков",
        min_value=1,
        max_value=12,
        initial=4,
        widget=forms.NumberInput(attrs={
            'class': 'form-control-custom',
            'id': 'playersInput',
            'min': '1',
            'max': '12'
        }),
        required=True,
        error_messages={
            'required': 'Укажите количество игроков в компании.',
            'min_value': 'Количество игроков должно быть не менее 1 человека.',
            'max_value': 'Для компании свыше 6 человек требуется бронирование двух дорожек.'
        }
    )
    club_card_number = forms.CharField(
        label="Номер клубной карты",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'id': 'cardInput',
            'placeholder': 'SP-GLD-00201'
        })
    )
    last_name = forms.CharField(
        label="Фамилия гостя",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'id': 'id_last_name',
            'placeholder': 'Иванов'
        }),
        error_messages={'required': 'Пожалуйста, введите фамилию гостя.'}
    )
    first_name = forms.CharField(
        label="Имя гостя",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'id': 'id_first_name',
            'placeholder': 'Иван'
        }),
        error_messages={'required': 'Пожалуйста, введите имя гостя.'}
    )
    patronymic = forms.CharField(
        label="Отчество гостя",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'id': 'id_patronymic',
            'placeholder': 'Иванович'
        })
    )
    phone = forms.CharField(
        label="Контактный телефон",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'id': 'id_phone',
            'placeholder': '+7 (927) 800-00-00'
        }),
        error_messages={'required': 'Укажите номер телефона для связи и SMS-уведомления.'}
    )
    email = forms.EmailField(
        label="Электронная почта",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-custom',
            'id': 'id_email',
            'placeholder': 'guest@mail.ru'
        }),
        error_messages={
            'required': 'Укажите e-mail для отправки электронного кассового чека (54-ФЗ).',
            'invalid': 'Введите корректный адрес электронной почты (например: user@mail.ru).'
        }
    )
    notes = forms.CharField(
        label="Особые пожелания",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control-custom',
            'id': 'id_notes',
            'rows': 2,
            'placeholder': 'Поднять детские бортики, подготовить обувь...'
        })
    )
    bar_items_json = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial='[]'
    )

    def clean_booking_date(self):
        """Проверка даты бронирования: не в прошлом."""
        b_date = self.cleaned_data.get('booking_date')
        if b_date and b_date < date.today():
            raise ValidationError("Нельзя оформить бронирование на прошедшую дату.")
        return b_date

    def clean_phone(self):
        """Серверная валидация формата номера телефона РФ."""
        raw_phone = self.cleaned_data.get('phone', '').strip()
        # Извлекаем только цифры
        digits = re.sub(r'\D', '', raw_phone)
        if len(digits) == 11 and digits[0] in ['7', '8']:
            formatted = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
            return formatted
        elif len(digits) == 10:
            formatted = f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
            return formatted
        else:
            raise ValidationError("Введите корректный номер телефона РФ в формате +7 (9XX) XXX-XX-XX.")

    def clean_club_card_number(self):
        """Проверка существования и активности клубной карты в базе данных."""
        card_num = self.cleaned_data.get('club_card_number', '').strip()
        if card_num:
            card = ClubCard.objects.filter(card_number=card_num, is_active=True).first()
            if not card:
                raise ValidationError("Указанная клубная карта не найдена в базе клуба или заблокирована.")
        return card_num

    def clean(self):
        """
        Комплексная серверная валидация:
        1. Особое требование Варианта 4: не более 6 человек на дорожку боулинга!
        2. Корректность временного интервала (time_end > time_start).
        3. Доступность ресурса в базе данных.
        """
        cleaned_data = super().clean()
        resource_id = cleaned_data.get('resource_id')
        players_count = cleaned_data.get('players_count')
        booking_date = cleaned_data.get('booking_date')
        time_start = cleaned_data.get('time_start')
        time_end = cleaned_data.get('time_end')

        if not resource_id:
            raise ValidationError({'resource_id': "Пожалуйста, выберите игровую дорожку или стол."})

        resource = ClubResource.objects.filter(id=resource_id).select_related('category').first()
        if not resource:
            raise ValidationError({'resource_id': "Выбранный ресурс не существует в базе клуба."})

        # --- ОСОБОЕ ТРЕБОВАНИЕ ВАРИАНТА 4: ЛИМИТ 6 ИГРОКОВ НА ДОРОЖКУ БОУЛИНГА (BUG-01) ---
        if resource.category.code == 'BOWLING':
            if players_count and int(players_count) > 6:
                raise ValidationError({
                    'players_count': (
                        f"На одну дорожку боулинга допускается компания не более 6 человек "
                        f"(указано: {players_count} чел.). При превышении числа гостей система требует "
                        f"добавить в бронь вторую дорожку (требование FR-05)."
                    )
                })

        # Проверка временного интервала
        if time_start and time_end:
            t_start = parse_time_obj(time_start)
            t_end = parse_time_obj(time_end)

            if t_end <= t_start and t_end != time(0, 0):
                raise ValidationError({'time_end': "Время окончания игры должно быть позже времени начала."})

            # Проверка доступности слота в БД
            if booking_date:
                is_free, _ = check_resource_availability(resource.id, booking_date, time_start, time_end)
                if not is_free:
                    raise ValidationError({
                        'resource_id': f"К сожалению, {resource.title} уже забронирован на этот интервал времени. Выберите другое время или соседний слот."
                    })

        return cleaned_data


class BookingSearchForm(forms.Form):
    """Форма поиска бронирования по номеру или телефону гостя."""
    q = forms.CharField(
        label="Номер бронирования или телефон",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-custom',
            'placeholder': 'SP-10001 или +79278000000',
            'aria-label': 'Номер бронирования или телефон'
        }),
        error_messages={'required': 'Пожалуйста, введите номер брони или телефон.'}
    )
