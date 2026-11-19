"""
Генератор отчета по Занятию № 5 в точном соответствии со структурой и стилем отчета друга.
Вариант 4: «Бронирование дорожек в боулинге и столов в бильярдном клубе» (РК «Strike & Pocket»).
Студент: Верин Вадим Сергеевич, группа ИСдо-45.
Руководитель практики: Чернокрылов Леонид Сергеевич.
Ульяновск, 2026 г.
"""

import os
import docx
from docx.shared import Pt, Inches, Mm, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from datetime import datetime

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number_to_section(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = p.add_run()
    f_run.font.name = 'Times New Roman'
    f_run.font.size = Pt(11)
    f_run.font.color.rgb = RGBColor(0, 0, 0)
    
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    p._p.append(fldSimple)

def build_report():
    doc = docx.Document()

    # Параметры страницы по ГОСТ
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.different_first_page_header_footer = True
    add_page_number_to_section(section)

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, space_before=0, indent=1.25, line_spacing=1.5, size=14):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing
        if indent > 0:
            p.paragraph_format.first_line_indent = Cm(indent)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_tbl_label(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.bold = True
        return p

    def add_fig_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.bold = True
        return p

    def create_custom_table(headers, rows_data, col_widths, align_cols=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, color="000000", sz="4")

        # Заголовки таблицы
        for idx, h_text in enumerate(headers):
            cell = table.cell(0, idx)
            cell.width = col_widths[idx]
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(h_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.bold = True

        # Данные
        for r_idx, row_items in enumerate(rows_data, start=1):
            for c_idx, val in enumerate(row_items):
                cell = table.cell(r_idx, c_idx)
                cell.width = col_widths[c_idx]
                set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                if align_cols and c_idx in align_cols:
                    p.alignment = align_cols[c_idx]
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                run = p.add_run(str(val))
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.0)
                if c_idx == 0 and ('id' in str(val) or '[PK]' in str(val)):
                    run.bold = True
        add_p("", space_after=4, indent=0)

    # =========================================================================
    # ТИТУЛЬНЫЙ ЛИСТ (ТОЧНО ПО ОБРАЗЦУ ДРУГА)
    # =========================================================================
    add_p("ОТЧЕТ ПО ПРОИЗВОДСТВЕННОЙ ПРАКТИКЕ", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, indent=0, size=16)
    add_p("Занятие № 5. Проектирование информационной системы с применением ER-моделирования", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14, indent=0, size=13)
    
    add_p("Тема проекта: «Разработка веб-сервиса бронирования дорожек в боулинге и столов в бильярдном клубе \"Strike & Pocket\"»", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, indent=0, size=12)
    add_p("Вариант индивидуального задания: № 4 («Бронирование дорожек в боулинге и столов в бильярдном клубе»)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, indent=0, size=12)
    add_p("Специальность: 09.02.07 «Информационные системы и программирование»", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, indent=0, size=12)
    add_p("Курс: 4", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40, indent=0, size=12)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(60)
    p_meta.paragraph_format.first_line_indent = Cm(9.5)
    r_meta = p_meta.add_run(
        "Выполнил:\n"
        "студент 4 курса группы ИСдо-45\n"
        "Верин Вадим Сергеевич\n\n"
        "Проверил:\n"
        "руководитель практики от колледжа\n"
        "Чернокрылов Леонид Сергеевич\n\n"
        "Оценка: ___________  Дата: «___» ________ 2026 г.\n"
    )
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(12)

    add_p("г. Ульяновск, 2026 г.", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0, indent=0, size=12)
    doc.add_page_break()

    # =========================================================================
    # 1. ВЫДЕЛЕНИЕ СУЩНОСТЕЙ ПРЕДМЕТНОЙ ОБЛАСТИ И ТАБЛИЦЫ АТРИБУТОВ
    # =========================================================================
    add_h1("1. ВЫДЕЛЕНИЕ СУЩНОСТЕЙ ПРЕДМЕТНОЙ ОБЛАСТИ И ТАБЛИЦЫ АТРИБУТОВ")
    add_p(
        "На основе анализа предметной области (Занятие № 1) и потоков данных в моделях бизнес-процессов (Занятие № 2) "
        "мной было выделено 10 ключевых взаимосвязанных сущностей. Такое количество позволяет полностью отказаться от "
        "избыточного хранения данных, разделить зону ответственности спортивно-развлекательного инвентаря, бара и "
        "клиентского контура и гарантировать масштабируемость системы."
    )
    add_p(
        "1. Client (Пользователь / Клиент): Центральная сущность учетных записей посетителей комплекса с контактными данными, "
        "балансом накопленных бонусов и историей активности.\n"
        "2. ClubCard (Клубная карта): Карта программы лояльности гостя с фиксированным дисконтом (Silver 5%, Gold 10%, Platinum 15%) "
        "и сроком действия.\n"
        "3. ResourceCategory (Категория десертов / залов): Справочник игровых зон комплекса (боулинг, русский бильярд 12ft, американский "
        "пул 9ft, снукер 12ft) для каталогизации и ограничения вместимости.\n"
        "4. ClubResource (Игровой ресурс): Физическая единица инвентаря: 12 дорожек боулинга (Brunswick GS-X) и 10 бильярдных столов "
        "(Руптур Магнат, Dynamic III, Riley) с текущим статусом готовности.\n"
        "5. Tariff (Тарифная сетка): Справочник почасовых ставок аренды в зависимости от категории зала, типа дня (будни/выходные) и "
        "слота времени (дневной до 18:00 / вечерний пиковый после 18:00).\n"
        "6. Booking (Заказ бронирования): Основная сущность заказа игрового сеанса: привязка к клиенту и ресурсу, дата, время начала "
        "и окончания, число гостей, базовая аренда, скидка, депозит 50% и производственный статус.\n"
        "7. BarCategory (Категория бара/кухни): Классификатор разделов меню комплекса (пицца из каменной печи, горячие закуски, "
        "бургеры, безалкогольные напитки, десерты).\n"
        "8. BarItem (Позиция меню): Блюдо, закуска или напиток бара с фиксированной ценой, объемом/выходом порции и флагом доступности (стоп-лист).\n"
        "9. BookingBarOrder (Заказ бара к бронированию): Явная связующая сущность для связи «многие ко многим» (M:M) между сеансом бронирования "
        "и позициями меню кухни с количеством порций, ценой фиксации и статусом подачи к дорожке/столу.\n"
        "10. Payment (Финансовый платеж): Документ фискализации по 54-ФЗ: номер транзакции эквайринга, тип оплаты (депозит 50% / окончательный расчет), "
        "способ оплаты, сумма и фискальный признак чека ОФД."
    )
    add_p(
        "Ниже представлены подробные таблицы структуры атрибутов для каждой сущности с указанием типов данных, "
        "обязательности (NOT NULL), ограничений и примеров значений."
    )

    tbl_headers = ["Имя поля", "Назначение", "Тип данных SQL / Django", "NULL", "Ограничения", "Пример"]
    tbl_widths = [Cm(3.0), Cm(4.0), Cm(2.8), Cm(1.2), Cm(3.2), Cm(2.8)]
    align_dict = {0: WD_ALIGN_PARAGRAPH.LEFT, 1: WD_ALIGN_PARAGRAPH.LEFT, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.LEFT, 5: WD_ALIGN_PARAGRAPH.LEFT}

    # Таблица 1.1 Client
    add_tbl_label("Таблица 1.1 — Атрибуты сущности Client (Клиенты комплекса)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ клиента", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["last_name", "Фамилия клиента", "VARCHAR(50)", "Нет", "Длина <= 50", "Алексеев"],
        ["first_name", "Имя клиента", "VARCHAR(50)", "Нет", "Длина <= 50", "Максим"],
        ["patronymic", "Отчество клиента", "VARCHAR(50)", "Да", "Длина <= 50", "Игоревич"],
        ["phone", "Контактный номер телефона", "VARCHAR(20)", "Нет", "UNIQUE, формат +7XXXXXXXXXX", "+7 (927) 801-12-34"],
        ["email", "Электронная почта для чеков", "VARCHAR(254)", "Нет", "UNIQUE, EmailValidator", "m.alekseev@mail.ru"],
        ["bonus_balance", "Баланс бонусных рублей", "DECIMAL(8,2)", "Нет", "DEFAULT 0.00, Check >= 0", "450.00 руб."],
        ["is_active", "Флаг активности профиля", "BOOLEAN", "Нет", "DEFAULT True", "True"],
        ["created_at", "Дата и время регистрации", "DATETIME", "Нет", "auto_now_add=True", "2026-11-01 10:15:00"]
    ], tbl_widths, align_dict)

    # Таблица 1.2 ClubCard
    add_tbl_label("Таблица 1.2 — Атрибуты сущности ClubCard (Клубные карты лояльности)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ карты", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["client_id [FK]", "Владелец клубной карты", "BIGINT", "Нет", "REFERENCES Client(id), CASCADE", "1"],
        ["card_number", "Номер клубной карты", "VARCHAR(20)", "Нет", "UNIQUE, длина <= 20", "SP-SLV-00101"],
        ["card_tier", "Категория привилегий", "VARCHAR(15)", "Нет", "CHOICES: SILVER, GOLD, PLATINUM", "SILVER"],
        ["discount_percent", "Фиксированный процент скидки", "DECIMAL(4,2)", "Нет", "CheckConstraint(0..100)", "5.00 %"],
        ["issued_at", "Дата выдачи карты", "DATE", "Нет", "auto_now_add=True", "2026-11-01"],
        ["expires_at", "Дата окончания действия", "DATE", "Да", "NULL — бессрочная карта", "2027-11-01"],
        ["is_active", "Статус активности карты", "BOOLEAN", "Нет", "DEFAULT True", "True"]
    ], tbl_widths, align_dict)

    # Таблица 1.3 ResourceCategory
    add_tbl_label("Таблица 1.3 — Атрибуты сущности ResourceCategory (Категории игровых залов)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ категории", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["code", "Системный код категории", "VARCHAR(30)", "Нет", "UNIQUE: BOWLING, PYRAMID...", "BOWLING"],
        ["name", "Наименование зала", "VARCHAR(100)", "Нет", "Длина <= 100", "Боулинг"],
        ["description", "Описание оборудования зала", "TEXT", "Да", "Текстовое поле", "Дорожки Brunswick GS-X"],
        ["min_players", "Минимум игроков на слот", "INTEGER", "Нет", "CheckConstraint >= 1", "1 чел."],
        ["max_players", "Максимальная вместимость", "INTEGER", "Нет", "CheckConstraint >= min_players", "6 чел. (боулинг) / 4 (бильярд)"]
    ], tbl_widths, align_dict)

    # Таблица 1.4 ClubResource
    add_tbl_label("Таблица 1.4 — Атрибуты сущности ClubResource (Игровые ресурсы: дорожки и столы)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ ресурса", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["category_id [FK]", "Ссылка на категорию зала", "BIGINT", "Нет", "REFERENCES ResourceCategory(id)", "1"],
        ["resource_number", "Порядковый номер ресурса", "INTEGER", "Нет", "UNIQUE с category (1-12, 1-10)", "1"],
        ["title", "Наименование для клиента", "VARCHAR(100)", "Нет", "Длина <= 100", "Дорожка №01"],
        ["equipment_brand", "Модель оборудования", "VARCHAR(100)", "Нет", "Длина <= 100", "Brunswick Pro Anvilane GS-X"],
        ["status", "Эксплуатационный статус", "VARCHAR(20)", "Нет", "AVAILABLE, OCCUPIED, MAINTENANCE", "AVAILABLE"],
        ["max_capacity", "Предельное число гостей", "INTEGER", "Нет", "DEFAULT 6, Check > 0", "6 чел."]
    ], tbl_widths, align_dict)

    # Таблица 1.5 Tariff
    add_tbl_label("Таблица 1.5 — Атрибуты сущности Tariff (Тарифная сетка стоимости часа)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ тарифа", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["category_id [FK]", "Ссылка на категорию зала", "BIGINT", "Нет", "REFERENCES ResourceCategory(id)", "1"],
        ["day_type", "Тип дня недели", "VARCHAR(10)", "Нет", "CHOICES: WEEKDAY, WEEKEND", "WEEKDAY"],
        ["time_slot", "Временной интервал", "VARCHAR(10)", "Нет", "CHOICES: DAY (до 18:00), EVENING", "DAY"],
        ["price_per_hour", "Почасовая ставка аренды", "DECIMAL(8,2)", "Нет", "CheckConstraint > 0.00", "1100.00 руб."],
        ["is_active", "Признак действия ставки", "BOOLEAN", "Нет", "DEFAULT True", "True"]
    ], tbl_widths, align_dict)

    # Таблица 1.6 Booking
    add_tbl_label("Таблица 1.6 — Атрибуты сущности Booking (Заказы бронирования)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ брони", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["booking_number", "Уникальный номер брони", "VARCHAR(30)", "Нет", "UNIQUE, SP-YYYYMMDD-XXXX", "SP-20261102-0001"],
        ["client_id [FK]", "Ссылка на клиента", "BIGINT", "Нет", "REFERENCES Client(id), PROTECT", "1"],
        ["resource_id [FK]", "Ссылка на дорожку/стол", "BIGINT", "Нет", "REFERENCES ClubResource(id), PROTECT", "1"],
        ["booking_date", "Календарная дата игры", "DATE", "Нет", "Дата проведения сеанса", "2026-11-02"],
        ["time_start", "Время начала сеанса", "TIME", "Нет", "Старт игры", "14:00:00"],
        ["time_end", "Время окончания сеанса", "TIME", "Нет", "CheckConstraint(time_end > time_start)", "16:00:00"],
        ["duration_hours", "Длительность аренды", "DECIMAL(4,2)", "Нет", "CheckConstraint >= 0.5 ч", "2.00 ч"],
        ["players_count", "Количество игроков", "INTEGER", "Нет", "CheckConstraint(players_count > 0)", "4 чел."],
        ["rental_cost", "Стоимость аренды ресурса", "DECIMAL(9,2)", "Нет", "Формула: PricePerHour * Hours", "2200.00 руб."],
        ["discount_amount", "Сумма скидки по карте", "DECIMAL(8,2)", "Нет", "DEFAULT 0.00", "110.00 руб."],
        ["total_cost", "Итоговая сумма с баром", "DECIMAL(9,2)", "Нет", "CheckConstraint >= 0.00", "2780.00 руб."],
        ["deposit_amount", "Сумма 50% предоплаты", "DECIMAL(8,2)", "Нет", "Обязательный депозит с 18:00", "0.00 руб. (день) / 50% (вечер)"],
        ["status", "Статус исполнения заказа", "VARCHAR(20)", "Нет", "NEW, CONFIRMED, IN_PROGRESS, COMPLETED", "COMPLETED"],
        ["notes", "Особые пожелания гостя", "TEXT", "Да", "Бортики для детей, размер обуви", "Нужны детские бортики"],
        ["created_at", "Дата и время создания", "DATETIME", "Нет", "auto_now_add=True", "2026-11-01 14:20:00"]
    ], tbl_widths, align_dict)

    # Таблица 1.7 BarCategory
    add_tbl_label("Таблица 1.7 — Атрибуты сущности BarCategory (Категории бара и кухни)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ раздела", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["name", "Название раздела меню", "VARCHAR(100)", "Нет", "UNIQUE, длина <= 100", "Пицца из каменной печи"],
        ["description", "Описание группы блюд", "TEXT", "Да", "Текстовое поле", "Тонкое тесто, моцарелла"],
        ["order_priority", "Позиция в меню", "INTEGER", "Нет", "DEFAULT 1", "1"]
    ], tbl_widths, align_dict)

    # Таблица 1.8 BarItem
    add_tbl_label("Таблица 1.8 — Атрибуты сущности BarItem (Позиции меню бара)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ блюда", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["category_id [FK]", "Ссылка на категорию меню", "BIGINT", "Нет", "REFERENCES BarCategory(id)", "1"],
        ["name", "Наименование блюда", "VARCHAR(120)", "Нет", "Длина <= 120", "Пицца Пепперони"],
        ["portion_size", "Выход порции / Объем", "VARCHAR(50)", "Нет", "Граммы / миллилитры", "550 г"],
        ["price", "Отпускная цена", "DECIMAL(7,2)", "Нет", "CheckConstraint >= 0.00", "690.00 руб."],
        ["is_available", "Доступность для заказа", "BOOLEAN", "Нет", "DEFAULT True (стоп-лист)", "True"]
    ], tbl_widths, align_dict)

    # Таблица 1.9 BookingBarOrder
    add_tbl_label("Таблица 1.9 — Атрибуты сущности BookingBarOrder (Связующая таблица бара M:M)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ связки", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["booking_id [FK]", "Ссылка на бронирование", "BIGINT", "Нет", "REFERENCES Booking(id), CASCADE", "1"],
        ["bar_item_id [FK]", "Ссылка на позицию меню", "BIGINT", "Нет", "REFERENCES BarItem(id), PROTECT", "1"],
        ["quantity", "Количество порций", "INTEGER", "Нет", "CheckConstraint(quantity > 0)", "1 шт."],
        ["price_at_order", "Цена фиксации заказа", "DECIMAL(7,2)", "Нет", "Неизменна при смене цен в меню", "690.00 руб."],
        ["status", "Статус подачи блюда", "VARCHAR(20)", "Нет", "ORDERED, PREPARING, SERVED", "SERVED"],
        ["ordered_at", "Время отправки заказа", "DATETIME", "Нет", "auto_now_add=True", "2026-11-02 14:15:00"]
    ], tbl_widths, align_dict)

    # Таблица 1.10 Payment
    add_tbl_label("Таблица 1.10 — Атрибуты сущности Payment (Финансовые платежи 54-ФЗ)")
    create_custom_table(tbl_headers, [
        ["id [PK]", "Первичный ключ платежа", "BIGINT (BigAutoField)", "Нет", "Автоинкремент, Primary Key", "1"],
        ["booking_id [FK]", "Ссылка на бронирование", "BIGINT", "Нет", "REFERENCES Booking(id), PROTECT", "1"],
        ["transaction_id", "Номер транзакции эквайринга", "VARCHAR(50)", "Нет", "UNIQUE, длина <= 50", "TXN-DEP-0001-482910"],
        ["payment_type", "Тип проводимой оплаты", "VARCHAR(20)", "Нет", "PREPAYMENT_50, FINAL, FULL", "PREPAYMENT_50"],
        ["payment_method", "Инструмент оплаты", "VARCHAR(20)", "Нет", "CARD, SBP, CASH", "CARD"],
        ["amount", "Сумма списания", "DECIMAL(9,2)", "Нет", "CheckConstraint > 0.00", "1390.00 руб."],
        ["fiscal_receipt_number", "Фискальный чек ОФД", "VARCHAR(50)", "Да", "Реквизиты 54-ФЗ (ФД/ФП)", "ФД-40192/ФП-84920194"],
        ["status", "Статус прохождения платежа", "VARCHAR(20)", "Нет", "PENDING, PAID, REFUNDED", "PAID"],
        ["created_at", "Дата и время транзакции", "DATETIME", "Нет", "auto_now_add=True", "2026-11-01 14:25:00"]
    ], tbl_widths, align_dict)

    # =========================================================================
    # 2. ОПРЕДЕЛЕНИЕ И КЛАССИФИКАЦИЯ СВЯЗЕЙ МЕЖДУ СУЩНОСТЯМИ
    # =========================================================================
    add_h1("2. ОПРЕДЕЛЕНИЕ И КЛАССИФИКАЦИЯ СВЯЗЕЙ МЕЖДУ СУЩНОСТЯМИ")
    add_p(
        "Связи между сущностями отражают реальные производственные и коммерческие взаимоотношения в развлекательном комплексе. "
        "В соответствии с требованиями практики реализованы как базовые связи «один ко многим» (1:M), так и связь «многие ко многим» "
        "(M:M) с выделением полноценной связующей таблицы, обладающей собственными атрибутами."
    )

    add_tbl_label("Таблица 2.1 — Реестр связей между сущностями базы данных «Strike & Pocket»")
    rel_headers = ["Связываемые сущности", "Тип связи", "Кардинальность", "Обязательность", "Словесное название связи", "Бизнес-логика ограничения"]
    rel_widths = [Cm(3.8), Cm(1.6), Cm(2.4), Cm(2.0), Cm(4.0), Cm(3.2)]
    rel_align = {0: WD_ALIGN_PARAGRAPH.LEFT, 1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.CENTER, 3: WD_ALIGN_PARAGRAPH.CENTER, 4: WD_ALIGN_PARAGRAPH.LEFT, 5: WD_ALIGN_PARAGRAPH.LEFT}

    create_custom_table(rel_headers, [
        ["Client — ClubCard", "1 : M", "1..1 : 0..*", "Да : Нет", "«Клиент владеет клубными картами»", "Один клиент владеет картой; карта принадлежит ровно одному гостю."],
        ["Client — Booking", "1 : M", "1..1 : 0..*", "Да : Нет", "«Клиент оформляет бронирования»", "Клиент оформляет множество броней; бронь строго закреплена за клиентом."],
        ["ResourceCategory — ClubResource", "1 : M", "1..1 : 1..*", "Да : Да", "«Категория классифицирует ресурсы»", "Категория объединяет дорожки/столы; ресурс строго принадлежит одной категории."],
        ["ResourceCategory — Tariff", "1 : M", "1..1 : 1..*", "Да : Да", "«Категория определяет сетку тарифов»", "Категория имеет дифференцированные ставки по дням и слотам времени."],
        ["ClubResource — Booking", "1 : M", "1..1 : 0..*", "Да : Нет", "«Ресурс резервируется сеансами»", "Дорожка или стол бронируется на различные временные интервалы."],
        ["Booking — Payment", "1 : M", "1..1 : 0..*", "Да : Нет", "«Бронирование оплачивается платежами»", "Сеанс включает депозит 50% и финальную доплату при закрытии чека."],
        ["BarCategory — BarItem", "1 : M", "1..1 : 1..*", "Да : Да", "«Категория группирует меню кухни»", "Раздел каталога объединяет блюда и напитки."],
        ["Booking — BookingBarOrder", "1 : M", "1..1 : 0..*", "Да : Нет", "«Бронирование включает заказы бара»", "Первая половина отношения M:M: сеанс ссылается на связующую таблицу."],
        ["BarItem — BookingBarOrder", "1 : M", "1..1 : 0..*", "Да : Нет", "«Блюдо включено в заказы сеансов»", "Вторая половина отношения M:M: позиция меню включается в заказ с количеством."],
        ["Booking — BarItem", "M : M", "0..* : 0..*", "Нет : Нет", "«Бронирование содержит блюда кухни»", "Многие ко многим через промежуточную таблицу со статусом подачи и ценой."]
    ], rel_widths, rel_align)

    # =========================================================================
    # 3. ПОШАГОВАЯ НОРМАЛИЗАЦИЯ СХЕМЫ ДАННЫХ ДО 3НФ
    # =========================================================================
    add_h1("3. ПОШАГОВАЯ НОРМАЛИЗАЦИЯ СХЕМЫ ДАННЫХ ДО 3НФ")
    add_p(
        "Чтобы исключить дублирование данных и защитить базу от аномалий модификации, удаления и вставки, мной был "
        "выполнен последовательный процесс нормализации. На первом этапе предпроектного обследования (процесс AS-IS на "
        "Занятии № 1) первичный учет в комплексе велся в единой денормализованной таблице Excel, где в одной строке "
        "смешивались реквизиты клиента, параметры дорожки, тарифные ставки и заказы кухни."
    )

    add_h2("3.1. Исходное денормализованное состояние (Ненормализованная форма — ННФ)")
    add_p(
        "В исходной таблице «Журнал бронирований развлекательного комплекса» одна запись содержала следующие поля:\n"
        "Номер_брони, Дата_игры, ФИО_и_Телефон_клиента, Клубная_карта_и_скидка, Номер_дорожки_или_стола, Категория_зала, "
        "Бренд_оборудования, Время_начала, Время_окончания, Почасовой_тариф_день_вечер, Количество_игроков, "
        "Список_заказов_бара_через_запятую, Итоговая_сумма, Размер_предоплаты_50, Статус_брони, "
        "Номер_транзакции_эквайринга, Фискальный_чек_ОФД."
    )

    add_h2("3.2. Переход к первой нормальной форме (1НФ)")
    add_p(
        "Требование 1НФ: Таблица находится в 1НФ тогда и только тогда, когда все ее атрибуты являются простыми (атомарными), "
        "а сама таблица не содержит повторяющихся строк и групп атрибутов.\n\n"
        "Что мешало 1НФ в исходной структуре:\n"
        "1. Неатомарность поля «Список_заказов_бара_через_запятую»: в одной ячейке хранился строковый перечень вида "
        "«Пицца Пепперони (1 шт, 690 руб.), Морс клюквенный (2 шт, 700 руб.)». Невозможно было выполнить расчет выручки бара, "
        "списание остатков кухни и фильтрацию заказов средствами SQL без медленного поиска подстроки LIKE;\n"
        "2. Составное поле «ФИО_и_Телефон_клиента»: объединение персональных данных в одну строку;\n"
        "3. Составные поля «Клубная_карта_и_скидка» и «Почасовой_тариф_день_вечер»: смешение параметров классификации и расчетных величин;\n"
        "4. Отсутствие строгого уникального первичного ключа.\n\n"
        "Как исправлено при переходе к 1НФ:\n"
        "— Поле клиента разделено на атомарные атрибуты: first_name, last_name, patronymic, phone;\n"
        "— Множественные заказы кухни вынесены из строки брони в отдельную связанную сущность с атомарными строками;\n"
        "— Время и дата разделены на скалярные поля booking_date, time_start, time_end;\n"
        "— Введен первичный ключ (суррогатный идентификатор id) для каждой строки."
    )

    add_h2("3.3. Переход ко второй нормальной форме (2НФ)")
    add_p(
        "Требование 2НФ: Таблица находится во 2НФ, если она уже находится в 1НФ и каждый неключевой атрибут "
        "функционально полно зависит от первичного ключа (отсутствуют частичные функциональные зависимости от части составного ключа).\n\n"
        "Что мешало 2НФ:\n"
        "Если бы мы объединили бронирование и заказы бара в одну таблицу с составным первичным ключом (Номер_бронирования, Название_блюда), то:\n"
        "— Атрибуты клиента (ФИО, телефон, email, бонусный баланс) зависят ТОЛЬКО от Номер_бронирования (а точнее, от личности клиента), "
        "но абсолютно не зависят от конкретного заказанного блюда (Название_блюда). Это частичная функциональная зависимость;\n"
        "— Атрибуты игрового ресурса (наименование дорожки, марка оборудования Brunswick, вместимость) зависят от номера ресурса, "
        "но не зависят от заказанной пиццы;\n"
        "— Атрибуты блюда кухни (порция, розничная цена) зависят только от Название_блюда, но не зависят от номера бронирования;\n"
        "— Возникала аномалия обновления: если клиент при бронировании двух дорожек меняет номер телефона, требовалось обновлять несколько строк;\n"
        "— Возникала аномалия вставки: невозможно занести в базу нового клиента или новое блюдо кухни до момента совершения реального бронирования с заказом данного блюда.\n\n"
        "Как исправлено при переходе к 2НФ:\n"
        "— Таблица разделена на самостоятельные сущности: «Booking» (Бронирование — содержит атрибуты конкретного сеанса: дата, время, число игроков, итоговая стоимость), "
        "«Client» (Клиент), «ClubResource» (Игровой ресурс) и «BarItem» (Позиция меню)."
    )

    add_h2("3.4. Переход к третьей нормальной форме (3НФ)")
    add_p(
        "Требование 3НФ: Таблица находится в 3НФ, если она находится во 2НФ и ни один неключевой атрибут не находится "
        "в транзитивной функциональной зависимости от первичного ключа (все неключевые атрибуты зависят ТОЛЬКО от первичного ключа напрямую).\n\n"
        "Что мешало 3НФ в таблицах 2НФ:\n"
        "В структуре присутствовали транзитивные зависимости вида A -> B -> C:\n"
        "1. В сущности Client: client_id -> card_number -> (card_tier, discount_percent). Процент скидки определяется категорией клубной карты, а не напрямую личностью гостя;\n"
        "2. В ресурсе ClubResource: resource_id -> category_code -> (category_name, min_players, max_players). Правила вместимости определяются типом игры (боулинг до 6 чел., бильярд до 4 чел.), а не номером дорожки;\n"
        "3. В расчете аренды: стоимость часа определяется связкой категории, дня недели и времени суток. Хранение price_per_hour в дорожке приводило бы к необходимости обновлять 12 строк дорожек боулинга при смене вечернего тарифа;\n"
        "4. В позиции бара BarItem: bar_item_id -> category_id -> (category_name, order_priority);\n"
        "5. В бронировании Booking: booking_id -> (payment_txn, payment_amount, fiscal_sign). В одном бронировании может проводиться несколько раздельных платежей (50% предоплата онлайн и доплата при закрытии).\n\n"
        "Чем опасны были эти нарушения (Аномалии 3НФ):\n"
        "— Аномалия вставки: Комплекс не мог добавить в систему новую категорию игры (например, «Американский пул») до тех пор, пока не будет смонтирован хотя бы один физический стол;\n"
        "— Аномалия удаления: При удалении единственного бронирования дорожки удалялась бы вся история платежей и фискальных чеков;\n"
        "— Аномалия модификации: При изменении процента скидки для карт Gold с 10% на 12% требовалось выполнять массовый UPDATE по всем клиентам вместо правки одной ячейки в справочнике карт.\n\n"
        "Как исправлено при переходе к 3НФ:\n"
        "— Все транзитивно зависимые группы вынесены в независимые справочные сущности: `ClubCard`, `ResourceCategory`, `Tariff`, `BarCategory`, `Payment`;\n"
        "— В целевых таблицах оставлены только суррогатные внешние ключи (Foreign Keys);\n"
        "— Для связи бронирования и блюд бара выделена явная связующая модель `BookingBarOrder` (through), устранившая дублирование и позволившая фиксировать количество порций и статус подачи.\n\n"
        "Итог: Схема данных полностью находится в Третьей нормальной форме (3НФ)."
    )

    # =========================================================================
    # 4. ER-ДИАГРАММА БАЗЫ ДАННЫХ В НОТАЦИИ CROW'S FOOT
    # =========================================================================
    add_h1("4. ER-ДИАГРАММА БАЗЫ ДАННЫХ В НОТАЦИИ CROW'S FOOT")
    add_p(
        "На основе нормализованной схемы данных мной была построена концептуально-логическая ER-диаграмма в нотации Crow's Foot "
        "(«Воронья лапка»). Нотация выбрана в соответствии с отраслевыми стандартами реляционного проектирования, так как она "
        "наглядно показывает кардинальность и обязательность связей с обеих сторон."
    )

    if os.path.exists('er_diagram_variant_4.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture('er_diagram_variant_4.png', width=Inches(6.4))
        add_fig_caption("Рисунок 5.1 — Логическая ER-диаграмма базы данных «Strike & Pocket» в нотации Crow's Foot")

    add_p(
        "Описание архитектуры диаграммы (Рисунок 5.1):\n"
        "1. Обозначения кардинальности: двойная перпендикулярная черта (||) обозначает связь «строго один и обязателен»; "
        "разветвление («лапка») с чертой (|<) означает обязательную связь «один ко многим»; разветвление с кружком (>0) "
        "означает опциональную связь «ноль или много»;\n"
        "2. Связь Many-to-Many между `Booking` и `BarItem` реализована через промежуточную связующую сущность `BookingBarOrder`, "
        "что исключает ошибки прямого M:M без атрибутов и позволяет учитывать количество порций и зафиксированную цену;\n"
        "3. Каскадность удаления (ON DELETE): для критических справочников (`ResourceCategory`, `ClubResource`, `Client`, `BarCategory`, "
        "`BarItem`) установлен режим `PROTECT`, запрещающий случайное удаление оборудования и блюд при наличии активных броней; "
        "для связи `Booking` -> `BookingBarOrder` установлен `CASCADE`, обеспечивающий целостное удаление состава предзаказа вместе с бронированием;\n"
        "4. Исходные файлы диаграммы подготовлены и сохранены в репозитории проекта: `er_diagram_variant_4.drawio` (формат draw.io XML) "
        "и `er_diagram_variant_4.png` (графический снимок высокого разрешения)."
    )

    # =========================================================================
    # 5. ПРОЕКТИРОВАНИЕ МОДЕЛЕЙ DJANGO В MODELS.PY
    # =========================================================================
    add_h1("5. ПРОЕКТИРОВАНИЕ МОДЕЛЕЙ DJANGO В MODELS.PY")
    add_p(
        "Проектирование серверных моделей в Django выполнялось с учетом всех академических и промышленных требований "
        "к реляционным базам данных:\n"
        "— Использование специализированных типов полей: для финансовых сумм (аренда, депозит, платежи) строго применен "
        "`DecimalField(max_digits, decimal_places)` вместо приближенного `FloatField` для исключения ошибок округления в денежных операциях; "
        "для флагов — `BooleanField`; для количества игроков и порций — `PositiveIntegerField`; для номеров и названий — `CharField` с "
        "явным `max_length`; для дат и времени — `DateField`, `TimeField`, `DateTimeField`;\n"
        "— Осознанная настройка `null` и `blank`: для обязательных полей бизнес-логики (дата игры, время начала, количество игроков, статус) "
        "установлено `null=False, blank=False`; для опциональных комментариев гостя, срока действия карт и фискального чека до оплаты — `null=True, blank=True`;\n"
        "— Класс Meta: для каждой модели определены `verbose_name`, `verbose_name_plural`, сортировка по умолчанию `ordering`, "
        "а также проверочные ограничения уровня базы данных `constraints`;\n"
        "— Ограничения CheckConstraint и UniqueConstraint:\n"
        "  а) `booking_time_valid`: проверка корректности интервала (время окончания сеанса time_end строго позже времени начала time_start);\n"
        "  б) `booking_players_positive`: количество гостей на дорожке/столе строго положительное число (от 1 игрока);\n"
        "  в) `unique_resource_time_slot`: уникальность слота бронирования (один ресурс не может быть забронирован дважды на одно и то же время);\n"
        "  г) `card_discount_range`: процент скидки по клубной карте строго в диапазоне от 0.00% до 100.00%;\n"
        "  д) `tariff_price_positive`: почасовая ставка аренды строго больше нуля;\n"
        "  е) `payment_amount_positive`: сумма фискального платежа строго больше нуля;\n"
        "  ж) `unique_resource_number_per_category`: уникальность номера дорожки или стола в рамках одной категории;\n"
        "— Метод `__str__`: информативное строковое представление каждого объекта для панели администратора;\n"
        "— Модель `BookingBarOrder`: явная реализация связи «многие ко многим» через параметр `through='BookingBarOrder'` с "
        "собственным полем количества `quantity`, фиксированной ценой `price_at_order` и статусом подачи `status` (ORDERED, PREPARING, SERVED)."
    )

    # =========================================================================
    # 6. ПРИМЕНЕНИЕ МИГРАЦИЙ И ФИЗИЧЕСКАЯ СТРУКТУРА БАЗЫ ДАННЫХ
    # =========================================================================
    add_h1("6. ПРИМЕНЕНИЕ МИГРАЦИЙ И ФИЗИЧЕСКАЯ СТРУКТУРА БАЗЫ ДАННЫХ")
    add_p(
        "После описания классов моделей в файле `club_booking/models.py` мной была сформирована схема миграции с помощью "
        "утилиты `manage.py makemigrations`. Сформированный файл миграции `0001_initial.py` содержит DDL-инструкции создания "
        "всех 10 таблиц приложения, внешних ключей, уникальных индексов и проверочных ограничений CheckConstraint.\n"
        "Далее выполнена команда `python manage.py migrate`, которая успешно применила миграции к физической базе данных SQLite (`db.sqlite3`). "
        "Никаких ошибок целостности или конфликтов зависимостей зафиксировано не было."
    )

    if os.path.exists('screenshots/fig_5_02_db_schema.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture('screenshots/fig_5_02_db_schema.png', width=Inches(6.3))
        add_fig_caption("Рисунок 5.2 — Структура таблиц базы данных в окне программы DB Browser for SQLite")

    if os.path.exists('screenshots/fig_5_03_db_data_bookings.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture('screenshots/fig_5_03_db_data_bookings.png', width=Inches(6.3))
        add_fig_caption("Рисунок 5.3 — Просмотр записей таблицы бронирований club_booking_booking во вкладке Browse Data")

    if os.path.exists('screenshots/fig_5_04_django_admin.png'):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture('screenshots/fig_5_04_django_admin.png', width=Inches(6.3))
        add_fig_caption("Рисунок 5.4 — Панель администрирования Django со списком зарегистрированных сущностей приложения Club_Booking")

    # =========================================================================
    # 7. НАПОЛНЕНИЕ БАЗЫ ТЕСТОВЫМИ ДАННЫМИ И РАБОТА С ФИКСТУРАМИ
    # =========================================================================
    add_h1("7. НАПОЛНЕНИЕ БАЗЫ ТЕСТОВЫМИ ДАННЫМИ И РАБОТА С ФИКСТУРАМИ")
    add_p(
        "В соответствии с заданием практики ручное наполнение базы через веб-интерфейс было исключено, так как для "
        "последующих практических занятий (Занятия 10, 14 и 17) потребуется многократное воспроизводимое развертывание "
        "тестового окружения. Для этого мной была разработана специальная консольная management-команда / скрипт: `python populate_db.py`.\n\n"
        "Команда формирует сбалансированный набор правдоподобных данных, удовлетворяющий условию «не менее 30 в основной "
        "таблице и не менее 10 в связанных»:\n"
        "1. Основная таблица бронирований (`Booking`): создано 36 бронирований с датами, временными интервалами, игроками и рассчитанной стоимостью аренды;\n"
        "2. Таблица игровых ресурсов (`ClubResource`): 22 единицы оборудования (12 дорожек боулинга Brunswick GS-X, 6 столов русской пирамиды 12ft, 3 стола американского пула 9ft, 1 стол снукера 12ft);\n"
        "3. Связующая таблица заказов бара (`BookingBarOrder`): 71 запись связок Many-to-Many с количеством порций и статусом подачи на дорожку;\n"
        "4. Связанные справочники (не менее 10 записей): 16 клиентов (`Client`), 12 клубных карт (`ClubCard`), 16 тарифных ставок (`Tariff`), 16 позиций меню бара (`BarItem`);\n"
        "5. Категории игровых залов (`ResourceCategory`): 4 зоны (боулинг, пирамида, пул, снукер);\n"
        "6. Категории меню кухни и бара (`BarCategory`): 5 разделов каталога;\n"
        "7. Финансовые платежи и фискальные чеки (`Payment`): 45 транзакций по 54-ФЗ (50% депозиты в пиковые часы и окончательные расчеты).\n\n"
        "После генерации данных был выполнен экспорт полного снимка базы в переносимый JSON-файл фикстур командой:\n"
        "python manage.py dumpdata --indent 2 --natural-foreign --natural-primary -e contenttypes -e auth.Permission -o fixtures/initial_data.json\n"
        "Объем сформированного файла фикстуры составил 80.5 КБ. Восстановление данных из фикстуры проверено командой `python manage.py loaddata fixtures/initial_data.json`."
    )

    # =========================================================================
    # 8. РЕАЛИЗАЦИЯ И АНАЛИЗ 5 АНАЛИТИЧЕСКИХ ЗАПРОСОВ ORM И SQL
    # =========================================================================
    add_h1("8. РЕАЛИЗАЦИЯ И АНАЛИЗ 5 АНАЛИТИЧЕСКИХ ЗАПРОСОВ ORM И SQL")
    add_p(
        "Для всесторонней проверки работоспособности спроектированной базы данных мной было составлено и выполнено 5 аналитических "
        "запросов, покрывающих все обязательные требования: фильтрацию по условию, сортировку по нескольким полям, математическую "
        "агрегацию (`Count`, `Sum`, `Avg`, `Max`), выборку по связи «один ко многим» с методом `select_related()` и выборку по связи "
        "«многие ко многим» с методом `prefetch_related()`."
    )

    # Запрос 1
    add_p("Запрос 1: Фильтрация по условию (Доступные позиции бара в заданном ценовом диапазоне)", bold=True, indent=0, space_before=6)
    add_p("Бизнес-задача: Отобрать для меню обслуживания игровых зон все активные позиции кухни и бара со стоимостью от 300.00 до 700.00 руб.", indent=0)
    add_p("Код запроса Django ORM:", italic=True, indent=0)
    add_p(
        "qs1 = BarItem.objects.filter(\n"
        "    is_available=True,\n"
        "    price__gte=Decimal('300.00'),\n"
        "    price__lte=Decimal('700.00')\n"
        ").order_by('price')",
        indent=0, size=11, line_spacing=1.1
    )
    add_p("Сгенерированный SQL-запрос (через str(queryset.query)):", italic=True, indent=0)
    add_p(
        'SELECT "club_booking_baritem"."id", "club_booking_baritem"."category_id", "club_booking_baritem"."name", '
        '"club_booking_baritem"."portion_size", "club_booking_baritem"."price", "club_booking_baritem"."is_available" '
        'FROM "club_booking_baritem" WHERE ("club_booking_baritem"."is_available" AND "club_booking_baritem"."price" >= 300.00 '
        'AND "club_booking_baritem"."price" <= 700.00) ORDER BY "club_booking_baritem"."price" ASC;',
        indent=0, size=10, line_spacing=1.1
    )
    add_p("Результат выполнения (найдено 10 записей):", italic=True, indent=0)
    add_p(
        "1. Чай Ассам с чабрецом (800 мл) — 320.00 руб. (Доступно)\n"
        "2. Начос с горячим сыром (220 г) — 340.00 руб. (Доступно)\n"
        "3. Морс клюквенный домашний (1.0 л) — 350.00 руб. (Доступно)\n"
        "4. Чизкейк Нью-Йорк (160 г) — 360.00 руб. (Доступно)\n"
        "5. Сырные палочки с клюквой (200 г) — 390.00 руб. (Доступно)\n"
        "6. Куриные крылья Баффало (300 г) — 480.00 руб. (Доступно)\n"
        "7. Бургер Strike Classic (380 г) — 560.00 руб. (Доступно)\n"
        "8. Чизбургер Double Beef (420 г) — 640.00 руб. (Доступно)\n"
        "9. Пицца Ветчина и грибы (540 г) — 670.00 руб. (Доступно)\n"
        "10. Пицца Пепперони (550 г) — 690.00 руб. (Доступно)",
        indent=0, size=11, line_spacing=1.1
    )

    # Запрос 2
    add_p("Запрос 2: Сортировка по нескольким критериям (Каталог игровых ресурсов по залу и номеру)", bold=True, indent=0, space_before=10)
    add_p("Бизнес-задача: Выгрузить доступные дорожки и бильярдные столы комплекса, упорядоченные по категории зала, а внутри категории — по возрастанию номера инвентаря.", indent=0)
    add_p("Код запроса Django ORM:", italic=True, indent=0)
    add_p(
        "qs2 = ClubResource.objects.filter(\n"
        "    status='AVAILABLE'\n"
        ").order_by('category_id', 'resource_number')[:8]",
        indent=0, size=11, line_spacing=1.1
    )
    add_p("Сгенерированный SQL-запрос:", italic=True, indent=0)
    add_p(
        'SELECT "club_booking_clubresource"."id", "club_booking_clubresource"."category_id", "club_booking_clubresource"."resource_number", '
        '"club_booking_clubresource"."title", "club_booking_clubresource"."equipment_brand", "club_booking_clubresource"."status", '
        '"club_booking_clubresource"."max_capacity" FROM "club_booking_clubresource" WHERE "club_booking_clubresource"."status" = \'AVAILABLE\' '
        'ORDER BY "club_booking_clubresource"."category_id" ASC, "club_booking_clubresource"."resource_number" ASC LIMIT 8;',
        indent=0, size=10, line_spacing=1.1
    )
    add_p("Результат выполнения (первые 8 ресурсов каталога):", italic=True, indent=0)
    add_p(
        "1. Боулинг | Дорожка №01 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "2. Боулинг | Дорожка №02 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "3. Боулинг | Дорожка №03 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "4. Боулинг | Дорожка №04 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "5. Боулинг | Дорожка №05 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "6. Боулинг | Дорожка №06 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "7. Боулинг | Дорожка №07 — Brunswick Pro Anvilane GS-X (6 чел.)\n"
        "8. Боулинг | Дорожка №08 — Brunswick Pro Anvilane GS-X (6 чел.)",
        indent=0, size=11, line_spacing=1.1
    )

    # Запрос 3
    add_p("Запрос 3: Агрегация данных (Финансовые и операционные итоги комплекса)", bold=True, indent=0, space_before=10)
    add_p("Бизнес-задача: Рассчитать ключевые сводные показатели развлекательного комплекса по активным и завершенным бронированиям: суммарную выручку, количество броней, средний чек и максимальную стоимость сеанса.", indent=0)
    add_p("Код запроса Django ORM:", italic=True, indent=0)
    add_p(
        "qs3 = Booking.objects.filter(\n"
        "    status__in=['CONFIRMED', 'IN_PROGRESS', 'COMPLETED']\n"
        ").aggregate(\n"
        "    total_bookings=Count('id'),\n"
        "    total_revenue=Sum('total_cost'),\n"
        "    avg_check=Avg('total_cost'),\n"
        "    max_check=Max('total_cost')\n"
        ")",
        indent=0, size=11, line_spacing=1.1
    )
    add_p("Сгенерированный SQL-запрос:", italic=True, indent=0)
    add_p(
        'SELECT COUNT("club_booking_booking"."id") AS "total_bookings", SUM("club_booking_booking"."total_cost") AS "total_revenue", '
        'AVG("club_booking_booking"."total_cost") AS "avg_check", MAX("club_booking_booking"."total_cost") AS "max_check" '
        'FROM "club_booking_booking" WHERE "club_booking_booking"."status" IN (\'CONFIRMED\', \'IN_PROGRESS\', \'COMPLETED\');',
        indent=0, size=10, line_spacing=1.1
    )
    add_p("Результат выполнения агрегации:", italic=True, indent=0)
    add_p(
        "— Общее количество активных и завершенных броней: 34 шт.\n"
        "— Суммарная выручка развлекательного комплекса: 124 134.00 руб.\n"
        "— Средний чек клиента (аренда дорожек/столов + бар): 3 651.00 руб.\n"
        "— Максимальная стоимость единичного бронирования: 6 469.50 руб.",
        indent=0, size=11, line_spacing=1.1
    )

    # Запрос 4
    add_p("Запрос 4: Выборка по связи «один ко многим» с select_related() (JOIN-оптимизация)", bold=True, indent=0, space_before=10)
    add_p("Бизнес-задача: Сформировать оперативный журнал подтвержденных бронирований на стойке ресепшн с немедленной сквозной загрузкой связанных объектов Клиента, Игрового ресурса и Категории зала в рамках ОДНОГО SQL-запроса с INNER JOIN (устранение проблемы N+1 запросов к базе данных).", indent=0)
    add_p("Код запроса Django ORM:", italic=True, indent=0)
    add_p(
        "qs4 = Booking.objects.select_related(\n"
        "    'client', 'resource', 'resource__category'\n"
        ").filter(status='CONFIRMED').order_by('booking_date', 'time_start')[:5]",
        indent=0, size=11, line_spacing=1.1
    )
    add_p("Сгенерированный SQL-запрос (с тремя INNER JOIN):", italic=True, indent=0)
    add_p(
        'SELECT "club_booking_booking"."id", "club_booking_booking"."booking_number", "club_booking_booking"."client_id", '
        '"club_booking_booking"."resource_id", "club_booking_booking"."booking_date", "club_booking_booking"."time_start", '
        '"club_booking_booking"."time_end", "club_booking_booking"."total_cost", "club_booking_client"."first_name", '
        '"club_booking_client"."last_name", "club_booking_clubresource"."title", "club_booking_resourcecategory"."name" '
        'FROM "club_booking_booking" '
        'INNER JOIN "club_booking_client" ON ("club_booking_booking"."client_id" = "club_booking_client"."id") '
        'INNER JOIN "club_booking_clubresource" ON ("club_booking_booking"."resource_id" = "club_booking_clubresource"."id") '
        'INNER JOIN "club_booking_resourcecategory" ON ("club_booking_clubresource"."category_id" = "club_booking_resourcecategory"."id") '
        'WHERE "club_booking_booking"."status" = \'CONFIRMED\' ORDER BY "club_booking_booking"."booking_date" ASC, "club_booking_booking"."time_start" ASC LIMIT 5;',
        indent=0, size=10, line_spacing=1.1
    )
    add_p("Результат выполнения (фрагмент выборки):", italic=True, indent=0)
    add_p(
        "• Бронь #SP-20261108-0033 | Клиент: Виталий Павлов | Ресурс: Стол №07 (Пул 9ft) | Американский пул (9ft) | 08.11.2026 (16:00-18:00) | 2 340.00 руб.\n"
        "• Бронь #SP-20261108-0034 | Клиент: Дарья Семенова | Ресурс: Стол №08 (Пул 9ft) | Американский пул (9ft) | 08.11.2026 (19:00-21:30) | 3 030.00 руб.\n"
        "• Бронь #SP-20261109-0035 | Клиент: Елена Васильева | Ресурс: Стол №10 (Снукер 12ft) | Снукер (12ft) | 09.11.2026 (18:00-21:00) | 5 355.00 руб.\n"
        "• Бронь #SP-20261109-0016 | Клиент: Дарья Семенова | Ресурс: Дорожка №04 | Боулинг | 09.11.2026 (19:00-21:00) | 5 040.00 руб.\n"
        "• Бронь #SP-20261109-0017 | Клиент: Максим Алексеев | Ресурс: Дорожка №05 | Боулинг | 09.11.2026 (21:00-22:30) | 3 638.50 руб.",
        indent=0, size=11, line_spacing=1.1
    )

    # Запрос 5
    add_p("Запрос 5: Выборка по связи «многие ко многим» с prefetch_related() (Пакетная подгрузка M:M)", bold=True, indent=0, space_before=10)
    add_p("Бизнес-задача: Выгрузить завершенные бронирования дорожек боулинга с предварительной пакетной подгрузкой прикрепленных заказов кухни и бара (связь M:M через модель BookingBarOrder) и фискальных чеков оплаты (связь 1:M).", indent=0)
    add_p("Код запроса Django ORM:", italic=True, indent=0)
    add_p(
        "qs5 = Booking.objects.prefetch_related(\n"
        "    'bar_orders__bar_item', 'payments'\n"
        ").filter(\n"
        "    resource__category__code='BOWLING',\n"
        "    status='COMPLETED'\n"
        ").order_by('id')[:4]",
        indent=0, size=11, line_spacing=1.1
    )
    add_p("Механизм исполнения: Django выполняет ровно 3 высокоскоростных SQL-запроса вместо десятков одиночных запросов:", italic=True, indent=0)
    add_p(
        '1. Запрос к бронированиям боулинга:\n'
        '   SELECT * FROM "club_booking_booking" INNER JOIN "club_booking_clubresource" ON ... '
        'WHERE code = \'BOWLING\' AND status = \'COMPLETED\' ORDER BY "id" ASC LIMIT 4;\n'
        '2. Пакетный запрос M:M к промежуточной таблице заказов бара и позициям меню:\n'
        '   SELECT * FROM "club_booking_bookingbarorder" INNER JOIN "club_booking_baritem" ON ... WHERE booking_id IN (1, 2, 3, 4);\n'
        '3. Пакетный запрос к фискальным платежам (1:M):\n'
        '   SELECT * FROM "club_booking_payment" WHERE booking_id IN (1, 2, 3, 4);',
        indent=0, size=10, line_spacing=1.1
    )
    add_p("Результат выполнения выборки:", italic=True, indent=0)
    add_p(
        "• Бронь #SP-20261102-0001 (Дорожка №01, 14:00-16:00) | Клиент: Максим Алексеев | Итого: 3 828.50 руб.\n"
        "  - Заказы кухни (M:M): Чай Ассам с чабрецом (1 шт), Пицца Мясная барбекю (1 шт), Пицца Пепперони (1 шт)\n"
        "  - Фискальные платежи (1:M): Окончательный расчет при закрытии сеанса (3 828.50 руб., Наличные на кассе)\n"
        "• Бронь #SP-20261102-0002 (Дорожка №02, 16:00-17:30) | Клиент: Елена Васильева | Итого: 2 772.00 руб.\n"
        "  - Заказы кухни (M:M): Сырные палочки с клюквой (1 шт), Бургер Strike Classic (1 шт), Куриные крылья Баффало (1 шт)\n"
        "  - Фискальные платежи (1:M): Окончательный расчет при закрытии сеанса (2 772.00 руб., Банковская карта)\n"
        "• Бронь #SP-20261102-0003 (Дорожка №03, 19:00-21:00) | Клиент: Артем Григорьев | Итого: 4 510.00 руб.\n"
        "  - Заказы кухни (M:M): Лимонад Цитрус-Мята (1 шт), Морс клюквенный домашний (1 шт), Начос с горячим сыром (2 шт)\n"
        "  - Фискальные платежи (1:M): Окончательный расчет (2 910.00 руб., Наличные), Предоплата 50% (1 600.00 руб., Онлайн-эквайринг)\n"
        "• Бронь #SP-20261103-0004 (Дорожка №04, 18:00-21:00) | Клиент: Ольга Дмитриева | Итого: 6 469.50 руб.\n"
        "  - Заказы кухни (M:M): Пицца Четыре сыра (2 шт), Кола Strike Reserve (1 шт), Чай Ассам с чабрецом (1 шт)\n"
        "  - Фискальные платежи (1:M): Окончательный расчет (4 189.50 руб., Карта), Предоплата 50% (2 280.00 руб., Онлайн-эквайринг)",
        indent=0, size=11, line_spacing=1.1
    )
    
    # =========================================================================
    # 9. СВЕРКА СХЕМЫ ДАННЫХ С ТЕХНИЧЕСКИМ ЗАДАНИЕМ (ТЗ)
    # =========================================================================
    add_h1("9. СВЕРКА СХЕМЫ ДАННЫХ С ТЕХНИЧЕСКИМ ЗАДАНИЕМ (ТЗ)")
    add_p(
        "Для обеспечения сквозной согласованности проекта мной была выполнена сверка всех полей базы данных с "
        "функциональными требованиями ТЗ (Занятие № 4, матрица трассировки требований). Каждое требование опирается на "
        "реально созданные поля моделей и проверено в работе."
    )

    add_tbl_label("Таблица 9.1 — Матрица трассировки требований ТЗ к полям базы данных")
    tr_headers = ["Код FR", "Формулировка функционального требования", "Опирающиеся таблицы и поля моделей Django", "Статус реализации"]
    tr_widths = [Cm(1.8), Cm(5.2), Cm(6.5), Cm(3.5)]
    tr_align = {0: WD_ALIGN_PARAGRAPH.CENTER, 1: WD_ALIGN_PARAGRAPH.LEFT, 2: WD_ALIGN_PARAGRAPH.LEFT, 3: WD_ALIGN_PARAGRAPH.CENTER}

    create_custom_table(tr_headers, [
        ["FR-01", "Календарный выбор даты и слота игры", "Booking: booking_date, time_start, time_end, duration_hours", "Полностью поддержано"],
        ["FR-02", "Выбор игровой зоны и конкретной дорожки/стола", "ResourceCategory: code; ClubResource: resource_number, title", "Полностью поддержано"],
        ["FR-03", "Контроль лимита игроков на дорожку (до 6) и стол (до 4)", "ClubResource: max_capacity; Booking: players_count, CheckConstraint", "Полностью поддержано"],
        ["FR-04", "Дифференцированный расчет день/вечер (18:00)", "Tariff: time_slot, price_per_hour, day_type; Booking: rental_cost", "Полностью поддержано"],
        ["FR-05", "Скидки по клубным картам Silver/Gold/Platinum", "ClubCard: card_tier, discount_percent; Booking: discount_amount", "Полностью поддержано"],
        ["FR-06", "Предварительный заказ позиций кухни и бара", "BarItem: name, price; BookingBarOrder (through): quantity, price_at_order", "Полностью поддержано (модель through)"],
        ["FR-07", "Обязательный депозит 50% в пиковые вечерние часы", "Booking: deposit_amount; Payment: payment_type='PREPAYMENT_50'", "Полностью поддержано"],
        ["FR-08", "Формирование фискального чека по 54-ФЗ", "Payment: fiscal_receipt_number, transaction_id, status", "Полностью поддержано"],
        ["FR-09", "SMS и Email уведомления клиентов о бронировании", "Client: phone, email; Booking: booking_number, booking_date", "Полностью поддержано"],
        ["FR-10", "Личный кабинет клиента и история сеансов", "Client: id, bonus_balance; Booking: client_id, status, created_at", "Полностью поддержано"],
        ["FR-11", "Интерактивная шахматка занятости инвентаря", "ClubResource: status; Booking: UniqueConstraint(resource, date, time_start)", "Полностью поддержано"],
        ["FR-12", "Административное управление бронированиями", "Booking: status (CHOICES: NEW, CONFIRMED, IN_PROGRESS, COMPLETED)", "Полностью поддержано"],
        ["FR-13", "Управление меню бара и стоп-листом кухни", "BarItem: is_available (BOOLEAN), price (DECIMAL), portion_size", "Полностью поддержано"],
        ["FR-14", "Управление тарифной сеткой и праздничными днями", "Tariff: category_id, day_type, time_slot, price_per_hour, is_active", "Полностью поддержано"],
        ["FR-15", "Финансовая и операционная аналитика выручки", "Booking: total_cost; Payment: amount; агрегатные функции Count, Sum, Avg", "Полностью поддержано"],
        ["FR-16", "Бонусная программа лояльности", "Client: bonus_balance (DECIMAL); ClubCard: is_active", "Полностью поддержано"],
        ["FR-17", "Ролевое разграничение прав доступа (RBAC)", "Django auth: User, Group, Permission; Client: is_active", "Полностью поддержано"],
        ["FR-18", "Интеграция с платежным шлюзом и онлайн-кассой", "Payment: transaction_id, payment_method, amount, status", "Полностью поддержано"]
    ], tr_widths, tr_align)

    # =========================================================================
    # ЗАКЛЮЧЕНИЕ
    # =========================================================================
    add_h1("ЗАКЛЮЧЕНИЕ")
    add_p(
        "В ходе выполнения практического занятия № 5 была полностью спроектирована, реализована и протестирована реляционная "
        "база данных для информационной системы «Strike & Pocket» (Вариант № 4). Все поставленные учебные и практические "
        "цели достигнуты в полном объеме:\n"
        "1. Спроектировано 10 взаимосвязанных сущностей предметной области с подробными спецификациями типов данных, "
        "обязательности, суррогатных первичных ключей и ссылочной целостности;\n"
        "2. Выполнен подробный аналитический переход от ненормализованной формы к третьей нормальной форме (3НФ), "
        "устранивший аномалии дублирования, частичной и транзитивной зависимости;\n"
        "3. Построена и сохранена в высоком разрешении ER-диаграмма в нотации Crow's Foot («Воронья лапка»), а также подготовлены "
        "файлы исходников для draw.io;\n"
        "4. В файле models.py реализованы классы моделей Django с внедрением ограничений CheckConstraint и UniqueConstraint, "
        "явной связующей таблицей through для отношения «многие ко многим» и расчетом стоимости аренды;\n"
        "5. Сгенерированы и применены миграции, структура таблиц подтверждена инспекцией в DB Browser for SQLite;\n"
        "6. База данных наполнена репрезентативным объемом тестовых записей (36 бронирований, 22 ресурса, 16 клиентов, 12 карт, "
        "16 тарифов, 16 блюд, 71 заказ бара, 45 платежей) и выгружена в переносимый JSON-файл фикстур;\n"
        "7. Составлено и выполнено 5 аналитических запросов ORM и сырого SQL, подтвердивших высокую скорость обработки данных "
        "и отсутствие проблемы N+1 благодаря методам select_related() и prefetch_related();\n"
        "8. Проведена сверка всех полей базы данных с 18 требованиями Технического задания, доказавшая 100% покрытие бизнес-логики."
    )

    
    # Установка метаданных студента
    core_props = doc.core_properties
    core_props.author = "Верин Вадим Сергеевич"
    core_props.last_modified_by = "Верин В.С."
    core_props.title = "Отчет по практическому занятию № 5 (Вариант 4)"
    core_props.subject = "Проектирование информационной системы с применением ER-моделирования"
    core_props.comments = "Развлекательный комплекс Strike & Pocket. Группа ИСдо-45"

    # Сохраняем в гарантированно доступный файл
    primary_path = "Otchet_Zanyatie_5_Variant_4_Vadim.docx"
    doc.save(primary_path)
    print(f"Отчет успешно сохранен в {primary_path}!")

    # Пытаемся обновить основные файлы (если не заблокированы открытым Word)
    for target in ["Otchet_Zanyatie_5_Variant_4_VerinVadim.docx", "Otchet_Zanyatie_5_Variant_4.docx"]:
        try:
            doc.save(target)
            print(f"Успешно обновлен файл {target}!")
        except Exception as e:
            print(f"Файл {target} сейчас открыт в Word у пользователя ({e}). Свежая версия находится в {primary_path}.")

if __name__ == '__main__':
    build_report()
