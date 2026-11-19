import os
import docx
from docx.shared import Pt, Inches, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def create_tz_document():
    doc = docx.Document()
    
    # 1. Поля по ГОСТ 19.201-78 / ГОСТ 7.32 (левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм)
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    
    # Титульный лист без номера страницы
    section.different_first_page_header_footer = True
    
    # Настройка базового стиля
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    font.color.rgb = RGBColor(0, 0, 0)
    p_format = style.paragraph_format
    p_format.line_spacing = 1.5
    p_format.space_before = Pt(0)
    p_format.space_after = Pt(0)
    p_format.first_line_indent = Mm(12.5)
    p_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    # Добавляем колонтитул с номером страницы со 2-й страницы
    add_page_number_to_section(section)
    
    def add_p(text, bold_prefix="", indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.first_line_indent = Mm(12.5) if indent else Mm(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(14)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(0, 0, 0)
            
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(14)
        r_text.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.5
        
        r_bullet = p.add_run("— ")
        r_bullet.font.name = 'Times New Roman'
        r_bullet.font.size = Pt(14)
        r_bullet.font.color.rgb = RGBColor(0, 0, 0)
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(14)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(0, 0, 0)
            
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(14)
        r_text.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Mm(12.5)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_image(img_path, caption_text, width=Inches(6.2)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.first_line_indent = Mm(0)
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            r = p_img.add_run()
            r.add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.first_line_indent = Mm(0)
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(12)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(0, 0, 0)
        else:
            print(f"Warning: Image file not found: {img_path}")

    # ==================== ТИТУЛЬНЫЙ ЛИСТ ====================
    # В точности как в примере друга
    for _ in range(4):
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.first_line_indent = Mm(0)

    title_p1 = doc.add_paragraph()
    title_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p1.paragraph_format.first_line_indent = Mm(0)
    title_p1.paragraph_format.space_before = Pt(0)
    title_p1.paragraph_format.space_after = Pt(6)
    r = title_p1.add_run("ТЕХНИЧЕСКОЕ ЗАДАНИЕ")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    title_p2 = doc.add_paragraph()
    title_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p2.paragraph_format.first_line_indent = Mm(0)
    title_p2.paragraph_format.space_before = Pt(0)
    title_p2.paragraph_format.space_after = Pt(14)
    r = title_p2.add_run("на разработку веб-сервиса бронирования дорожек в боулинге\nи столов в бильярдном клубе «Strike & Pocket»")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    title_p3 = doc.add_paragraph()
    title_p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p3.paragraph_format.first_line_indent = Mm(0)
    title_p3.paragraph_format.space_before = Pt(0)
    title_p3.paragraph_format.space_after = Pt(30)
    r = title_p3.add_run("Вариант № 4")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    for _ in range(4):
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.first_line_indent = Mm(0)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.first_line_indent = Mm(0)
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(40)
    r = p_meta.add_run("Выполнил:\n"
                      "студент группы 4ИС-21\n"
                      "Вострокнутов Вадим Дмитриевич\n\n"
                      "Проверил:\n"
                      "руководитель практики от колледжа\n"
                      "Смирнов Алексей Владимирович\n"
                      "___________________ / ___________________ /\n\n"
                      "Оценка: ___________  Дата: «___» ________ 2026 г.")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)

    for _ in range(3):
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.first_line_indent = Mm(0)

    title_city = doc.add_paragraph()
    title_city.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_city.paragraph_format.first_line_indent = Mm(0)
    title_city.paragraph_format.space_before = Pt(0)
    title_city.paragraph_format.space_after = Pt(0)
    r = title_city.add_run("Москва, 2026 г.")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # ==================== СОДЕРЖАНИЕ ====================
    add_h1("СОДЕРЖАНИЕ")

    toc_lines = [
        ("1. Наименование и область применения", "3"),
        ("2. Основание для разработки", "4"),
        ("3. Назначение разработки", "5"),
        ("4. Требования к программе или программному изделию", "7"),
        ("   4.1. Требования к функциональным характеристикам", "7"),
        ("   4.2. Требования к надежности", "11"),
        ("   4.3. Условия эксплуатации", "12"),
        ("   4.4. Требования к составу и параметрам технических средств", "13"),
        ("   4.5. Требования к информационной и программной совместимости", "14"),
        ("5. Требования к программной документации", "16"),
        ("6. Стадии и этапы разработки", "17"),
        ("7. Порядок контроля и приемки", "20"),
        ("8. Анализ и управление проектными рисками (Раздел на максимальный балл)", "22"),
        ("Приложение А. Сводная матрица функциональных требований (FR-01 — FR-18)", "25"),
        ("Приложение Б. Матрица нефункциональных требований (NFR-01 — NFR-10)", "27"),
        ("Приложение В. Архитектурно-структурные схемы веб-сервиса «Strike & Pocket»", "28"),
        ("Список использованных источников", "31")
    ]

    tbl_toc = doc.add_table(rows=len(toc_lines), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_lines):
        r_toc = tbl_toc.rows[idx]
        c0, c1 = r_toc.cells[0], r_toc.cells[1]
        c0.width = Mm(150)
        c1.width = Mm(15)
        set_cell_margins(c0, top=25, bottom=25, left=15, right=15)
        set_cell_margins(c1, top=25, bottom=25, left=15, right=15)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.first_line_indent = Mm(0)
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(12)
        if not title.startswith("   "):
            r0.font.bold = True
        r0.font.color.rgb = RGBColor(0, 0, 0)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.first_line_indent = Mm(0)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # ==================== РАЗДЕЛ 1 ====================
    add_h1("1. НАИМЕНОВАНИЕ И ОБЛАСТЬ ПРИМЕНЕНИЯ")
    add_p("«Автоматизированный веб-сервис онлайн-бронирования дорожек в боулинге и столов в бильярдном клубе \"Strike & Pocket\"».", bold_prefix="1.1. Полное наименование разрабатываемой системы: ")
    add_p("Веб-сервис «Strike & Pocket» (в структуре серверного программного кода — Django-модуль `club_booking`).", bold_prefix="1.2. Краткое условное наименование: ")
    add_p("Программный продукт создается для внедрения в технологический и операционный процесс спортивно-развлекательных центров, совмещающих боулинг-клубы, залы профессионального и любительского бильярда (русская пирамида, американский пул, снукер) и сопутствующее ресторанно-барное обслуживание. Основная направленность — предприятия индустрии досуга, работающие по модели почасового тайм-слотового резервирования ресурсов (Time-slot reservation). В таких клубах ключевое значение имеют дифференцированная тарификация в зависимости от дня недели и времени суток (смена тарифа при переходе рубежа 18:00), физические ограничения вместимости дорожек (до 6 человек на одну дорожку боулинга) и необходимость строгого предотвращения овербукинга.", bold_prefix="1.3. Область применения: ")
    add_p("В рамках прохождения производственной практики на 4 курсе колледжа заказчиком проекта выступает отделение информационных технологий и телекоммуникаций ГБПОУ «Колледж связи № 54» имени П.М. Вострухина совместно с базовым развлекательным центром. Непосредственным разработчиком выступает студент 4 курса группы 4ИС-21 Вострокнутов Вадим Дмитриевич.", bold_prefix="1.4. Заказчик и разработчик: ")

    # ==================== РАЗДЕЛ 2 ====================
    add_h1("2. ОСНОВАНИЕ ДЛЯ РАЗРАБОТКИ")
    add_p("Разработка программного комплекса осуществляется на основании следующих документов и нормативных актов:")
    add_bullet("Федерального государственного образовательного стандарта среднего профессионального образования (ФГОС СПО) по специальности 09.02.07 «Информационные системы и программирование»;", bold_prefix="а) ")
    add_bullet("Рабочей программы производственной практики по профилю специальности (4 курс, 7-й семестр обучения, профессиональный модуль ПМ.01 «Разработка модулей программного обеспечения»);", bold_prefix="б) ")
    add_bullet("Индивидуального задания на практику № 4: «Бронирование дорожек в боулинге и столов в бильярдном клубе», выданного и утвержденного руководителем практики от колледжа;", bold_prefix="в) ")
    add_bullet("Материалов предпроектного обследования предметной области и сводки проблем ручного учета (Занятие № 1);", bold_prefix="г) ")
    add_bullet("Построенных моделей бизнес-процессов в нотации BPMN 2.0 (Занятие № 2, диаграммы текущего состояния AS-IS и целевого TO-BE);", bold_prefix="д) ")
    add_bullet("Аналитического отчета и сравнительной таблицы функционала 10 отечественных и международных систем-аналогов (Занятие № 3).", bold_prefix="е) ")
    add_p("с 10 ноября по 28 ноября 2026 г.", bold_prefix="2.2. Календарные сроки выполнения разработки: ")

    # ==================== РАЗДЕЛ 3 ====================
    add_h1("3. НАЗНАЧЕНИЕ РАЗРАБОТКИ")
    add_p("Основная задача разрабатываемого сервиса «Strike & Pocket» — убрать рутинный ручной барьер при согласовании бронирования дорожек боулинга и бильярдных столов между посетителями и администратором заведения. Система предоставляет клиенту визуальный интерактивный онлайн-визард, где он самостоятельно выбирает желаемый ресурс на схеме зала (дорожки боулинга Brunswick или столы пирамиды/пула), определяет дату и тайм-слот с мгновенным прозрачным расчетом стоимости. Одновременно сервис автоматически проверяет пересечение границ тарифов (переход через 18:00), контролирует лимит гостей (до 6 чел. на дорожку), принимает онлайн-депозит с фискализацией по 54-ФЗ и отображает подтвержденный наряд на интерактивной шахматке администратора клуба с формированием предзаказа для бара ко времени игры.", bold_prefix="3.1. Функциональное назначение системы: ")
    add_p("Внедрение веб-сервиса направлено на достижение конкретных практических показателей:")
    add_bullet("Сокращение длительности оформления индивидуальной заявки с 12–15 минут (телефонный звонок и ручные записи) до 2–3 минут благодаря тому, что клиент самостоятельно выбирает дорожку/стол, время и предзаказ напитков на сайте без ожидания на телефонной линии;", bold_prefix="1. ")
    add_bullet("Снижение нагрузки на дежурных администраторов и менеджеров клуба минимум на 70%;", bold_prefix="2. ")
    add_bullet("Полное устранение конфликтных ситуаций двойного бронирования (овербукинга) за счет применения строгих транзакционных блокировок на уровне базы данных;", bold_prefix="3. ")
    add_bullet("Исключение ошибок расчета стоимости при переходе дневного тарифа в вечерний пиковый тариф (18:00) благодаря встроенному математическому алгоритму раздельного расчета интервалов;", bold_prefix="4. ")
    add_bullet("Ежемесячная экономия трудозатрат персонала клуба в объеме 135 рабочих часов (согласно экономическому расчету отчета занятия 2).", bold_prefix="5. ")
    add_p("В системе предусмотрено четыре группы пользователей с раздельным доступом:")
    add_bullet("просмотр каталога игровых зон, выбор дорожки/стола на интерактивной схеме, онлайн-бронирование, предзаказ по меню бара, отслеживание статуса и электронных чеков в личном кабинете;", bold_prefix="— Гость / Клиент: ")
    add_bullet("работа с интерактивной шахматкой бронирований зала, оперативное ручное оформление визитов, фиксация явки клиентов, отметки No-Show и управление игровым временем;", bold_prefix="— Администратор зала / Оператор: ")
    add_bullet("прием предзаказов кухни и бара, привязанных к номеру дорожки/стола ко времени начала игры, изменение статусов приготовления («Принят», «Готовится», «Подан»);", bold_prefix="— Бармен / Официант: ")
    add_bullet("настройка тарифных сеток (будни/выходные, день/вечер), управление дисконтными картами постоянных гостей, системный аудит, создание учетных записей сотрудников и регулярные бэкапы.", bold_prefix="— Управляющий / Администратор системы: ")

    # ==================== РАЗДЕЛ 4 ====================
    add_h1("4. ТРЕБОВАНИЯ К ПРОГРАММЕ ИЛИ ПРОГРАММНОМУ ИЗДЕЛИЮ")
    
    add_h2("4.1. Требования к функциональным характеристикам")
    add_p("Функциональные требования разделены по основным блокам сервиса. Каждое требование имеет уникальный идентификатор (FR-01 — FR-18), формулировку строго по схеме «Система должна...», указание роли пользователя и приоритет по шкале MoSCoW (Must have — обязательно для ядра системы, Should have — важно для удобства, Could have — желательно при наличии времени).")
    add_p("В основу проектирования заложены математические формулы и производственные правила, зафиксированные в отчетах прошлых дней:")
    add_p("1. Формула итоговой стоимости сеанса бронирования:\n"
          "P = (T_до_18 * P_день) + (T_после_18 * P_вечер) + SUM(P_бар) + P_сопут - Discount,\n"
          "где T_до_18 — длительность игры в часах до 18:00; P_день — тариф дневного часа; T_после_18 — длительность игры после 18:00; P_вечер — тариф вечернего часа; SUM(P_бар) — сумма предзаказа блюд и напитков бара; P_сопут — аренда инвентаря и обуви; Discount — скидка по клубной карте постоянного гостя.")
    add_p("2. Физическое правило лимита игроков на одну дорожку боулинга:\n"
          "N_игроков <= 6 на 1 дорожку.\n"
          "При попытке указать N > 6 система принудительно требует добавления второй смежной дорожки с автоматическим расчетом требуемого числа дорожек K = ceil(N / 6) и соответствующим пересчетом стоимости.")
    add_p("3. Алгоритм проверки занятости ресурсов и защиты от овербукинга:\n"
          "Slot(Resource_id, T_start, T_end) INTERSECT ActiveBookings(Resource_id) == EMPTY,\n"
          "где при совпадении интервалов система блокирует занятые слоты на уровне атомарной транзакции с удержанием предварительной брони ровно 10 минут на время оплаты депозита.")
    add_p("4. Правило дифференцированного депозита в пиковые часы:\n"
          "Для вечерних сеансов (после 18:00) и в выходные дни размер обязательной онлайн-предоплаты составляет не менее 50% от расчетной стоимости игрового времени для минимизации риска неявки (No-Show).")

    p_tbl = doc.add_paragraph()
    p_tbl.paragraph_format.first_line_indent = Mm(0)
    p_tbl.paragraph_format.space_before = Pt(8)
    p_tbl.paragraph_format.space_after = Pt(2)
    p_tbl.paragraph_format.keep_with_next = True
    r = p_tbl.add_run("Таблица 4.1 — Ключевые функциональные требования к веб-сервису «Strike & Pocket» (фрагмент ядра)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    core_fr = [
        ("FR-01", "Система должна отображать постраничный каталог игровых ресурсов клуба с разделением на дорожки боулинга (1–12) и бильярдные столы (пирамида 12ft, пул 9ft, снукер 12ft) с фотографией, описанием и тарифами.", "Гость, Клиент", "Must have", "/catalog/"),
        ("FR-02", "Система должна обеспечивать фильтрацию каталога по типу игры (боулинг, русский бильярд, пул, снукер) и ценовому диапазону.", "Гость, Клиент", "Must have", "/catalog/?type=&price="),
        ("FR-03", "Система должна предоставлять интерактивный календарь тайм-слотов с шагом 30 и 60 минут с индикацией занятости в реальном времени.", "Клиент, Администратор", "Must have", "/booking/calendar/"),
        ("FR-05", "Система должна контролировать лимит игроков на дорожку боулинга (до 6 чел.) и блокировать оформление 1 дорожки при 7+ игроках с автопредложением 2 соседних дорожек.", "Покупатель, Система", "Must have", "/booking/wizard/"),
        ("FR-06", "Система должна производить динамический пересчет стоимости сеанса без перезагрузки страницы на основе почасовой сетки (будни/выходные, день/вечер).", "Клиент, Система", "Must have", "/api/calculate-price/"),
        ("FR-07", "Система должна выполнять автоматический раздельный расчет цены при переходе сеанса через границу тарифа 18:00 с выводом детализации в смету заказа.", "Клиент, Система", "Must have", "/api/calculate-price/"),
        ("FR-08", "Система должна предоставлять модуль предварительного заказа блюд и напитков из ресторанного меню к началу сеанса с привязкой заказа к номеру стола/дорожки.", "Клиент, Официант", "Should have", "/bar/preorder/"),
        ("FR-11", "Система должна атомарно сохранять бронирование и связанные позиции предзаказа в БД с блокировкой слота на 10 минут в единой транзакции (transaction.atomic).", "Система", "Must have", "/booking/create/"),
        ("FR-12", "Система должна обеспечивать онлайн-оплату депозита картами и через СБП с генерацией фискального электронного чека по 54-ФЗ.", "Клиент, Кассир", "Must have", "/payment/process/"),
        ("FR-15", "Система должна отображать для дежурного администратора клуба интерактивную шахматку занятости дорожек и столов в АРМ с отметкой явки и No-Show.", "Администратор клуба", "Must have", "/arm/schedule/")
    ]

    tbl_core = doc.add_table(rows=len(core_fr) + 1, cols=5)
    tbl_core.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_core, color="000000", sz="4", val="single")

    col_h_c = ["ID", "Формулировка функционального требования", "Роль", "Приоритет", "Модуль / URL"]
    for c_i, h in enumerate(col_h_c):
        cell = tbl_core.rows[0].cells[c_i]
        cell.text = h
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        for r_item in p.runs:
            r_item.font.name = 'Times New Roman'
            r_item.font.size = Pt(9.5)
            r_item.font.bold = True
            r_item.font.color.rgb = RGBColor(0, 0, 0)

    for r_i, r_data in enumerate(core_fr):
        row = tbl_core.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Mm(0)
            for r_item in p.runs:
                r_item.font.name = 'Times New Roman'
                r_item.font.size = Pt(9)
                r_item.font.color.rgb = RGBColor(0, 0, 0)
                if c_i in [0, 3]:
                    r_item.font.bold = True

    col_widths_c_mm = [14, 76, 26, 22, 28]
    for row in tbl_core.rows:
        for idx, w in enumerate(col_widths_c_mm):
            row.cells[idx].width = Mm(w)

    add_p("Полный перечень всех 18 требований с привязкой к тест-кейсам приведен в Приложении А настоящего ТЗ.")

    add_h2("4.2. Требования к надежности")
    add_p("4.2.1. Отказоустойчивость сервиса обеспечивается архитектурой Django и правильной настройкой СУБД. Программный комплекс должен работать в режиме 24/7. Допустимое суммарное время технологических окон для обновления версий не должно превышать 2 часов в месяц.")
    add_p("4.2.2. Защита от одновременных заказов на один слот (Race Conditions): Чтобы два покупателя не смогли в одну секунду занять один и тот же слот времени на популярную дорожку боулинга или стол бильярда в пятничный вечер, сохранение заказа оформляется атомарно с пессимистической блокировкой строк `select_for_update()` внутри блока `transaction.atomic()`. Это полностью защищает заведение от конфликтов и овербукинга.")
    add_p("4.2.3. Резервное копирование и восстановление: Предусмотрено ежесуточное создание полного дампа базы данных в 03:00 ночи. Архивы хранятся не менее 30 дней. Целевое время поднятия базы после сбоя сервера (RTO) составляет до 30 минут, максимальная потеря данных (RPO) — не более 24 часов.")

    add_h2("4.3. Условия эксплуатации")
    add_p("4.3.1. Климатические условия: Серверная часть работает в типовых условиях хостинга или серверной комнаты при температуре от +18 до +24 °C и влажности воздуха 40–60%.")
    add_p("4.3.2. Требования к рабочим местам и квалификации сотрудников:")
    add_bullet("не требуют инструктажа, работают через обычный браузер мобильного телефона или ПК;", bold_prefix="— Клиенты: ")
    add_bullet("моноблок или планшет с диагональю от 15 дюймов на стойке ресепшн, сенсорный ввод, управление бронированиями в шахматке АРМ;", bold_prefix="— Администраторы зала: ")
    add_bullet("терминал контактного бара с сенсорным экраном для приема нарядов предзаказа кухни и бара ко времени сеанса;", bold_prefix="— Бармены и официанты: ")
    add_bullet("уровень подготовки студента 4 курса специальности 09.02.07 (умение работать в терминале, запускать миграции `manage.py migrate` и управлять правами доступа).", bold_prefix="— Администратор системы: ")

    add_h2("4.4. Требования к составу и параметрам технических средств")
    add_p("4.4.1. Серверная платформа (минимальные системные требования):")
    add_bullet("процессор: x86-64, не менее 2 ядер с тактовой частотой от 2.0 ГГц;");
    add_bullet("оперативная память: от 4 ГБ DDR4 (желательно 8 ГБ для шустрой обработки статики и кэша);");
    add_bullet("накопитель: быстрый SSD объемом от 40 ГБ свободного места под проект, БД и фотографии залов;");
    add_bullet("сетевое подключение: канал от 100 Мбит/с со стабильным статическим IP-адресом.");
    add_p("4.4.2. Клиентские устройства:")
    add_bullet("терминал администратора клуба: дисплей от 15 дюймов, разрешение не ниже 1920x1080 px;");
    add_bullet("смартфоны клиентов: операционные системы Android 9+ или iOS 14+ с экраном от 360 px по ширине;");
    add_bullet("компьютеры управляющих: офисные рабочие станции с монитором от 19 дюймов.");

    add_h2("4.5. Требования к информационной и программной совместимости")
    add_p("По условиям практического задания в проекте жестко зафиксированы следующие технические ограничения:")
    add_bullet("Python версии 3.11 или выше, фреймворк Django версии 4.2 LTS или выше (в проекте взят актуальный Django 5.x);", bold_prefix="1. Серверный стек: ")
    add_bullet("SQLite версии 3.35+ на этапе локальной сборки и тестов, PostgreSQL 14+ для промышленной эксплуатации;", bold_prefix="2. База данных: ")
    add_bullet("чистый HTML5, стили CSS3, логика на чистом JavaScript (ES6+) строго БЕЗ применения тяжелых фронтенд-фреймворков вроде React, Vue или Angular;", bold_prefix="3. Клиентский стек: ")
    add_bullet("верстка на CSS Flexbox/Grid с контрольными точками брейкпоинтов: 360 px (телефоны), 768 px (планшеты), 1024 px (ноутбуки), 1440 px (широкие мониторы);", bold_prefix="4. Адаптивность: ")
    add_bullet("проект ведется в репозитории Git. Пароли, приватный ключ `SECRET_KEY` и база данных вынесены в локальный файл `.env` и обязательно внесены в `.gitignore`, чтобы секреты не попали в коммиты.", bold_prefix="5. Безопасность и Git: ")

    # ==================== РАЗДЕЛ 5 ====================
    add_h1("5. ТРЕБОВАНИЯ К ПРОГРАММНОЙ ДОКУМЕНТАЦИИ")
    add_p("Комплект создаваемых программных документов оформляется по Единой системе программной документации (ЕСПД) и включает:")
    add_bullet("Техническое задание (настоящий документ) — ГОСТ 19.201-78;", bold_prefix="1. ")
    add_bullet("Описание программы — ГОСТ 19.402-78 (структура приложения `club_booking`, схемы таблиц БД, логика калькулятора тарифов);", bold_prefix="2. ")
    add_bullet("Руководство оператора — ГОСТ 19.505-79 (инструкция по работе с интерактивной шахматкой броней для администратора и реестром предзаказов для бара);", bold_prefix="3. ")
    add_bullet("Руководство системного программиста — ГОСТ 19.503-79 (шаги по развертыванию, установка зависимостей `requirements.txt`, накатывание миграций и запуск dev-сервера);", bold_prefix="4. ")
    add_bullet("Программа и методика испытаний — ГОСТ 19.301-79 (набор сценариев проверок TC-01 — TC-18).", bold_prefix="5. ")

    # ==================== РАЗДЕЛ 6 ====================
    add_h1("6. СТАДИИ И ЭТАПЫ РАЗРАБОТКИ")
    add_p("Разработка веб-сервиса расписана по 13 практическим занятиям практики (с 5 по 17 занятие). Каждый этап завершается подготовкой конкретного документа или работающего модуля системы.")

    p_tbl_st = doc.add_paragraph()
    p_tbl_st.paragraph_format.first_line_indent = Mm(0)
    p_tbl_st.paragraph_format.space_before = Pt(8)
    p_tbl_st.paragraph_format.space_after = Pt(2)
    p_tbl_st.paragraph_format.keep_with_next = True
    r = p_tbl_st.add_run("Таблица 6.1 — Календарный план и стадии разработки веб-сервиса (Занятия 5–17)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    stages_13 = [
        ("5", "Проектирование базы данных", "Разработка структуры БД, описание связанных таблиц (Lanes, Tables, Bookings, Tariffs, BarOrders), внешних ключей, связей Many-to-Many и словаря атрибутов.", "ER-диаграмма Crow's Foot, SQL-дамп структуры"),
        ("6", "Проектирование интерфейса пользователя", "Создание wireframe-макетов экранов: витрина залов, интерактивная карта столов (SVG), календарь слотов, корзина предзаказа, шахматка АРМ.", "Макеты Figma / UI-пакет экранов"),
        ("7", "Инициализация репозитория и окружения", "Развертывание virtualenv, создание структуры Django-проекта `club_booking`, подключение статики, шаблонов, файлов .gitignore и .env.", "Репозиторий Git, отчет по настройке среды"),
        ("8", "Разработка ORM-моделей данных", "Написание классов моделей в models.py, настройка валидаторов лимита игроков и генерация первичных миграций Django.", "Листинг models.py, скриншоты миграций"),
        ("9", "Панель администратора и диспетчера", "Кастомизация админки Django, создание фильтров по броням, настройка сетки тарифов и справочника ресторанного меню.", "Скриншоты админ-панели с фикстурами"),
        ("10", "Реализация каталога и витрины ресурсов", "Создание Views, HTML-шаблонов, пагинации, карточек дорожек и столов, фильтрации по видам игр (боулинг, русский бильярд, пул, снукер).", "Рабочий каталог, скриншоты адаптивной верстки"),
        ("11", "Разработка интерактивного онлайн-визарда", "Написание скрипта booking_wizard.js, верстка пошагового бронирования, динамический пересчет тарифа (стык 18:00) и проверка лимита 6 чел.", "Скринкаст работы визарда, модуль wizard.js"),
        ("12", "Модуль оформления заказа и предзаказа бара", "Реализация корзины предзаказа кухни/бара, сохранение брони в транзакции, интеграция с платежным шлюзом и генерация чека 54-ФЗ.", "Тестовые заказы в БД, валидатор слотов"),
        ("13", "Рабочее место администратора и шахматка", "Создание интерактивной шахматки броней в АРМ, переключение статусов («Ожидает», «Подтвержден», «В игре», «Завершен»), фиксация явки.", "Шахматка броней, образец наряда-чека"),
        ("14", "Комплексное тестирование системы", "Написание unit-тестов и интеграционных проверок (TC-01 — TC-18), нагрузочные тесты и заполнение матрицы трассировки.", "Протокол испытаний, отчет coverage"),
        ("15", "Оптимизация и аудит безопасности", "Проверка защиты от XSS, CSRF, SQL-инъекций, оптимизация ORM-запросов (select_related), замеры скорости в Lighthouse.", "Отчет аудита безопасности, замеры TTFB"),
        ("16", "Оформление документации пользователя", "Подготовка руководств оператора, администратора зала и системного программиста по стандартам ЕСПД.", "Комплект руководств пользователя"),
        ("17", "Итоговая приемка и демонстрация проекта", "Сквозное демонстрационное испытание от выбора дорожки клиентом до фиксации явки в АРМ и распечатки фискального чека.", "Акт приемочных испытаний, итоговый отчет")
    ]

    tbl_s6 = doc.add_table(rows=len(stages_13) + 1, cols=4)
    tbl_s6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_s6, color="000000", sz="4", val="single")

    col_h_s = ["№ зан.", "Наименование этапа разработки", "Содержание выполняемых работ", "Отчетный документ / артефакт"]
    for c_i, h in enumerate(col_h_s):
        cell = tbl_s6.rows[0].cells[c_i]
        cell.text = h
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        for r_item in p.runs:
            r_item.font.name = 'Times New Roman'
            r_item.font.size = Pt(9.5)
            r_item.font.bold = True
            r_item.font.color.rgb = RGBColor(0, 0, 0)

    for r_i, r_data in enumerate(stages_13):
        row = tbl_s6.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Mm(0)
            for r_item in p.runs:
                r_item.font.name = 'Times New Roman'
                r_item.font.size = Pt(8.5)
                r_item.font.color.rgb = RGBColor(0, 0, 0)
                if c_i == 0:
                    r_item.font.bold = True

    col_widths_s_mm = [16, 44, 60, 46]
    for row in tbl_s6.rows:
        for idx, w in enumerate(col_widths_s_mm):
            row.cells[idx].width = Mm(w)

    # ==================== РАЗДЕЛ 7 ====================
    add_h1("7. ПОРЯДОК КОНТРОЛЯ И ПРИЕМКИ")
    add_p("Приемка проекта проводится в виде комплексного демонстрационного испытания в присутствии руководителя практики от колледжа. Программа включает три уровня проверки:")
    add_bullet("проверка математики калькулятора цен (стык 18:00) и блокировки превышения лимита 6 чел. на дорожку;", bold_prefix="1. Автономное тестирование отдельных функций: ")
    add_bullet("проверка взаимодействия JS-интерфейса карты зала с Django API и транзакциями базы данных;", bold_prefix="2. Интеграционное тестирование: ")
    add_bullet("проверка по чек-листу готовности из 10 пунктов.", bold_prefix="3. Итоговые приемо-сдаточные испытания: ")
    add_p("Проект считается успешно завершенным и допускается к защите практики только при выполнении каждого из 10 критериев:")

    p_tbl_chk = doc.add_paragraph()
    p_tbl_chk.paragraph_format.first_line_indent = Mm(0)
    p_tbl_chk.paragraph_format.space_before = Pt(8)
    p_tbl_chk.paragraph_format.space_after = Pt(2)
    p_tbl_chk.paragraph_format.keep_with_next = True
    r = p_tbl_chk.add_run("Таблица 7.1 — Чек-лист контроля и критериев приемо-сдаточных испытаний")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    chk_rows = [
        ("Критерий 1", "Запуск dev-сервера без ошибок", "Проект штатно стартует командой `python manage.py runserver`, в терминале нет предупреждений и критических ошибок."),
        ("Критерий 2", "Чистое применение миграций", "Все миграции Django накатываются без ошибок нарушения внешних ключей и конфликтов схемы базы данных."),
        ("Критерий 3", "Демонстрационные данные", "В базе есть тестовый набор: 12 дорожек боулинга, 10 бильярдных столов (русский, пул, снукер), сетка тарифов и меню бара."),
        ("Критерий 4", "Работа онлайн-калькулятора", "Клиент выбирает ресурс и интервал времени, смета моментально пересчитывается без перезагрузки страницы."),
        ("Критерий 5", "Валидация лимита игроков", "Визард физически запрещает выбрать 1 дорожку боулинга при числе гостей от 7 человек и предлагает забронировать 2 соседние дорожки."),
        ("Критерий 6", "Расчет границы тарифа 18:00", "Система корректно делит интервал (например, 17:00–19:00) на дневные и вечерние часы с раздельной калькуляцией в чеке."),
        ("Критерий 7", "Сквозное сохранение заказа", "Бронь без сбоев записывается в БД с блокировкой слота на 10 минут, получает номер, фиксирует депозит и статус «Ожидает оплаты»."),
        ("Критерий 8", "Шахматка АРМ Администратора", "Новая бронь сразу отображается в сетке занятости зала в АРМ, администратор может в клик подтвердить явку или сменить статус."),
        ("Критерий 9", "Фискальный чек и предзаказ", "Система формирует печатный наряд предзаказа бара и фискальный электронный чек онлайн-оплаты в соответствии с 54-ФЗ."),
        ("Критерий 10", "Безопасность и чистота Git", "В репозитории нет паролей и БД (`.env` внесен в `.gitignore`), все 18 тест-кейсов успешно пройдены.")
    ]

    tbl_chk = doc.add_table(rows=len(chk_rows) + 1, cols=3)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_chk, color="000000", sz="4", val="single")

    col_h_chk = ["Пункт", "Контролируемый параметр", "Критерий успешного прохождения проверки"]
    for c_i, h in enumerate(col_h_chk):
        cell = tbl_chk.rows[0].cells[c_i]
        cell.text = h
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        for r_item in p.runs:
            r_item.font.name = 'Times New Roman'
            r_item.font.size = Pt(9.5)
            r_item.font.bold = True
            r_item.font.color.rgb = RGBColor(0, 0, 0)

    for r_i, r_data in enumerate(chk_rows):
        row = tbl_chk.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Mm(0)
            for r_item in p.runs:
                r_item.font.name = 'Times New Roman'
                r_item.font.size = Pt(8.5)
                r_item.font.color.rgb = RGBColor(0, 0, 0)
                if c_i == 0:
                    r_item.font.bold = True

    col_widths_chk_mm = [22, 54, 90]
    for row in tbl_chk.rows:
        for idx, w in enumerate(col_widths_chk_mm):
            row.cells[idx].width = Mm(w)

    # ==================== РАЗДЕЛ 8 ====================
    add_h1("8. АНАЛИЗ И УПРАВЛЕНИЕ ПРОЕКТНЫМИ РИСКАМИ")
    add_p("Чтобы защитить проект от неожиданных проблем во время разработки и промышленной эксплуатации, мной был составлен превентивный реестр рисков по стандарту ГОСТ Р ИСО 31000-2019. Для каждой рисковой ситуации определена вероятность возникновения, потенциальная задержка сроков сдачи, симптом наступления и четкий порядок действий по предотвращению и устранению последствий.")

    p_tbl_rk = doc.add_paragraph()
    p_tbl_rk.paragraph_format.first_line_indent = Mm(0)
    p_tbl_rk.paragraph_format.space_before = Pt(8)
    p_tbl_rk.paragraph_format.space_after = Pt(2)
    p_tbl_rk.paragraph_format.keep_with_next = True
    r = p_tbl_rk.add_run("Таблица 8.1 — Реестр и план митигации рисков проекта веб-сервиса «Strike & Pocket»")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    rk_5 = [
        ("Риск 1", "Конкурентный овербукинг слотов времени", "Средняя (35%)", "+3 дня на доработку транзакционных блокировок", "Появление в БД двух пересекающихся броней на одну дорожку боулинга, жалобы гостей на стойке ресепшн.", "Предотвращение: Применение пессимистической блокировки строк `select_for_update()` на уровне ORM Django при резервировании слота; временное удержание слота на 10 минут в сессии клиента на этапе ввода контактов и оплаты.\nРеагирование: Автоматический перевод спорного заказа в статус «Требует согласования администратора», отправка уведомления дежурному для предложения клиенту соседней дорожки или бесплатного напитка из бара со скидкой 10%."),
        ("Риск 2", "Ошибки расчета на стыке дневного и вечернего тарифа 18:00", "Высокая (60%)", "+2 дня на ужесточение валидаторов и тестов", "Несовпадение расчетной суммы заказа в чеке при бронировании пограничных интервалов (например, с 17:00 до 19:00).", "Предотвращение: Изоляция алгоритма тарификации в отдельном модуле `TariffService`; написание комплекта из 12 параметризованных unit-тестов для граничных временных точек.\nРеагирование: Ручная корректировка позиций чека администратором в АРМ в 1 клик с сохранением аудиторского лога."),
        ("Риск 3", "Разрушение адаптивной верстки схемы зала на экранах 360 px", "Средняя (30%)", "+2 дня на переверстку SVG-карты", "Появление горизонтальной полосы прокрутки в Chrome DevTools на смартфонах, выпадение кнопок выбора столов.", "Предотвращение: Проектирование схемы в масштабируемом векторном формате SVG с относительными координатами `viewBox`; применение подхода Mobile First.\nРеагирование: Переключение интерфейса на мобильных экранах с графической схемы на текстовый список доступных ресурсов."),
        ("Риск 4", "Сбои вебхуков онлайн-эквайринга и чеков 54-ФЗ", "Средняя (25%)", "+2 дня на доработку polling-сервиса", "Зависание статуса брони в состоянии «Ожидает оплаты» после успешного списания денег с карты клиента.", "Предотвращение: Реализация фонового механизма периодического опроса статуса платежа (polling) по протоколу шлюза; отправка идемпотентных запросов.\nРеагирование: Возможность ручного перевода брони в статус «Оплачено» администратором по номеру банковской квитанции."),
        ("Риск 5", "Отставание от графика на этапах 8–11 практики", "Средняя (30%)", "Задержка контрольной сдачи этапа на 2–4 дня", "Незавершенные задачи спринта к началу занятия, непройденные интеграционные тесты модуля тарифов.", "Предотвращение: Следование приоритетам MoSCoW: сначала отладка базового ядра (Must have — выбор слота, лимит 6 чел., граница 18:00), второстепенные визуальные эффекты (Could have) переносятся на конец практики.\nРеагирование: Дробление сложных задач на простые подзадачи; задействование стандартных Django Generic Views вместо рукописных контроллеров.")
    ]

    tbl_rk = doc.add_table(rows=len(rk_5) + 1, cols=6)
    tbl_rk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_rk, color="000000", sz="4", val="single")

    col_h_rk = ["Код риска", "Наименование риска", "Вероят- ность", "Влияние на график", "Признак наступления", "План предотвращения и реагирования"]
    for c_i, h in enumerate(col_h_rk):
        cell = tbl_rk.rows[0].cells[c_i]
        cell.text = h
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        for r_item in p.runs:
            r_item.font.name = 'Times New Roman'
            r_item.font.size = Pt(9.5)
            r_item.font.bold = True
            r_item.font.color.rgb = RGBColor(0, 0, 0)

    for r_i, r_data in enumerate(rk_5):
        row = tbl_rk.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Mm(0)
            for r_item in p.runs:
                r_item.font.name = 'Times New Roman'
                r_item.font.size = Pt(8.5)
                r_item.font.color.rgb = RGBColor(0, 0, 0)
                if c_i in [0, 2, 3]:
                    r_item.font.bold = True

    col_widths_rk_mm = [16, 38, 16, 20, 32, 44]
    for row in tbl_rk.rows:
        for idx, w in enumerate(col_widths_rk_mm):
            row.cells[idx].width = Mm(w)

    doc.add_page_break()

    # ==================== ПРИЛОЖЕНИЕ А ====================
    add_h1("ПРИЛОЖЕНИЕ А. СВОДНАЯ МАТРИЦА ФУНКЦИОНАЛЬНЫХ ТРЕБОВАНИЙ (FR-01 — FR-18)")
    add_p("В данном приложении приведена полная таблица всех 18 функциональных требований системы, сформированных на основе анализа бизнес-процессов Занятия № 2 и функциональной матрицы Занятия № 3. Требования на 100% согласованы с файлом «Matritsa_trassirovki_Variant_4.xlsx».")

    p_tbl_a = doc.add_paragraph()
    p_tbl_a.paragraph_format.first_line_indent = Mm(0)
    p_tbl_a.paragraph_format.space_before = Pt(8)
    p_tbl_a.paragraph_format.space_after = Pt(2)
    p_tbl_a.paragraph_format.keep_with_next = True
    r = p_tbl_a.add_run("Таблица А.1 — Полная матрица функциональных требований к веб-сервису «Strike & Pocket»")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    app_a_rows = [
        ("FR-01", "Система должна отображать постраничный каталог игровых ресурсов клуба с разделением на дорожки боулинга (1–12) и бильярдные столы (пирамида 12ft, пул 9ft, снукер 12ft) с фотографией, описанием и тарифами.", "Гость, Клиент", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-01", "/catalog/", "TC-01"),
        ("FR-02", "Система должна обеспечивать текстовый поиск и фильтрацию каталога по типу игры (боулинг, русский бильярд, пул, снукер) и диапазону стоимости аренды.", "Гость, Клиент", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-02, Ф-12", "/catalog/?type=", "TC-02"),
        ("FR-03", "Система должна предоставлять интерактивный календарь тайм-слотов с дискретностью 30 и 60 минут с индикацией занятости ресурсов в реальном времени.", "Клиент, Администратор", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-03", "/booking/calendar/", "TC-03"),
        ("FR-04", "Система должна отображать интерактивную векторную SVG-схему залов заведения с возможностью визуального выбора конкретного стола бильярда или номера дорожки.", "Клиент", "Should have", "Занятие 3: Ф-04", "/booking/map/", "TC-04"),
        ("FR-05", "Система должна контролировать лимит игроков на дорожку боулинга (до 6 чел.) и при вводе 7+ гостей блокировать выбор 1 дорожки и предлагать две соседние.", "Покупатель, Система", "Must have", "Особое требование Варианта 4; Занятие 3: Ф-05", "/booking/wizard/", "TC-05"),
        ("FR-06", "Система должна производить динамический пересчет стоимости сеанса без перезагрузки страницы на основе почасовой сетки (будни/выходные, день/вечер).", "Клиент, Система", "Must have", "Занятие 1: Тарифы; Занятие 3: Ф-02", "/api/calculate-price/", "TC-06"),
        ("FR-07", "Система должна выполнять автоматический раздельный расчет цены при переходе сеанса через границу тарифа 18:00 с выводом детализации в смету заказа.", "Клиент, Система", "Must have", "Особое требование Варианта 4; Занятие 3: Ф-06", "/api/calculate-price/", "TC-07"),
        ("FR-08", "Система должна предоставлять модуль предварительного заказа блюд и напитков из ресторанного меню к началу сеанса с привязкой заказа к номеру стола/дорожки.", "Клиент, Официант", "Should have", "Занятие 2: Процесс 3; Занятие 3: Ф-07", "/bar/preorder/", "TC-08"),
        ("FR-09", "Система должна позволять клиенту выбирать сопутствующие услуги клуба (прокат профи-обуви, заказ клубного маркера, спарринг-партнера или тренера).", "Клиент", "Could have", "Занятие 1: Доп. услуги; Занятие 3: Ф-16", "/booking/extra/", "TC-09"),
        ("FR-10", "Система должна предоставлять форму бронирования с валидацией персональных данных (ФИО, формат мобильного номера телефона РФ +7-XXX-XXX-XX-XX, e-mail).", "Клиент", "Must have", "Занятие 2: Процесс 1", "/booking/checkout/", "TC-10"),
        ("FR-11", "Система должна атомарно сохранять заказ и связанные позиции в БД с блокировкой слота на 10 минут в единой транзакции (select_for_update, transaction.atomic).", "Система", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-03", "/booking/create/", "TC-11"),
        ("FR-12", "Система должна обеспечивать онлайн-оплату депозита картами и через СБП с генерацией фискального электронного чека по 54-ФЗ.", "Клиент, Кассир", "Must have", "Занятие 2: Процесс 2; Занятие 3: Ф-09, Ф-18", "/payment/process/", "TC-12"),
        ("FR-13", "Система должна автоматически формировать и отправлять сервисные уведомления (SMS / Telegram) клиенту с подтверждением брони и напоминанием за 2 часа.", "Система", "Should have", "Занятие 2: Процесс 1; Занятие 3: Ф-11", "club.services.notify", "TC-13"),
        ("FR-14", "Система должна предоставлять клиенту личный кабинет для просмотра истории броней, электронных чеков и самостоятельной отмены брони за 2 часа до сеанса.", "Клиент", "Should have", "Занятие 3: Ф-08, Ф-13", "/accounts/orders/", "TC-14"),
        ("FR-15", "Система должна отображать для дежурного администратора клуба интерактивную шахматку занятости дорожек и столов в АРМ с отметкой явки и No-Show.", "Администратор клуба", "Must have", "Занятие 1: Роли; Занятие 2: Процесс 1", "/arm/schedule/", "TC-15"),
        ("FR-16", "Система должна автоматически воспроизводить звуковой сигнал и отображать индикатор в АРМ Администратора при поступлении нового оплаченного заказа.", "Администратор клуба", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-15", "/arm/notifications/", "TC-16"),
        ("FR-17", "Система должна поддерживать применение клубных дисконтных карт постоянных гостей и промокодов со скидкой с автоматическим пересчетом депозита.", "Клиент, Менеджер", "Should have", "Занятие 2: Процесс 4; Занятие 3: Ф-10", "/manager/loyalty/", "TC-17"),
        ("FR-18", "Система должна поддерживать ролевую модель доступа (Клиент, Администратор зала, Официант/Бармен, Менеджер, Системный администратор) с защитой URL-маршрутов.", "Администратор", "Must have", "Занятие 2: Матрица RACI", "club.models.CustomUser", "TC-18")
    ]

    tbl_a = doc.add_table(rows=len(app_a_rows) + 1, cols=7)
    tbl_a.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_a, color="000000", sz="4", val="single")

    col_h_a = ["ID", "Формулировка требования", "Роль", "Приоритет", "Источник", "Модуль / URL", "Тест"]
    for c_i, h in enumerate(col_h_a):
        cell = tbl_a.rows[0].cells[c_i]
        cell.text = h
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        for r_item in p.runs:
            r_item.font.name = 'Times New Roman'
            r_item.font.size = Pt(9)
            r_item.font.bold = True
            r_item.font.color.rgb = RGBColor(0, 0, 0)

    for r_i, r_data in enumerate(app_a_rows):
        row = tbl_a.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 3, 6] else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Mm(0)
            for r_item in p.runs:
                r_item.font.name = 'Times New Roman'
                r_item.font.size = Pt(8.5)
                r_item.font.color.rgb = RGBColor(0, 0, 0)
                if c_i in [0, 3, 6]:
                    r_item.font.bold = True

    col_widths_a_mm = [12, 52, 22, 18, 28, 22, 12]
    for row in tbl_a.rows:
        for idx, w in enumerate(col_widths_a_mm):
            row.cells[idx].width = Mm(w)

    doc.add_page_break()

    # ==================== ПРИЛОЖЕНИЕ Б ====================
    add_h1("ПРИЛОЖЕНИЕ Б. МАТРИЦА НЕФУНКЦИОНАЛЬНЫХ ТРЕБОВАНИЙ (NFR-01 — NFR-10)")
    add_p("Каждое нефункциональное требование содержит точную измеримую числовую метрику, позволяющую однозначно проверить надежность, скорость отклика и безопасность сервиса при тестировании.")

    p_tbl_b = doc.add_paragraph()
    p_tbl_b.paragraph_format.first_line_indent = Mm(0)
    p_tbl_b.paragraph_format.space_before = Pt(8)
    p_tbl_b.paragraph_format.space_after = Pt(2)
    p_tbl_b.paragraph_format.keep_with_next = True
    r = p_tbl_b.add_run("Таблица Б.1 — Матрица нефункциональных требований с измеримыми метриками")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    app_b_rows = [
        ("NFR-01", "Производительность каталога", "Время полной загрузки и отрисовки страницы каталога готовых изделий не должно превышать 1.5 секунды при скорости подключения 10 Мбит/с (TTFB не более 300 мс).", "Время загрузки <= 1.5 с, TTFB <= 300 мс"),
        ("NFR-02", "Быстродействие калькулятора", "Время динамического пересчета сметы на стороне браузера (JS) должно составлять не более 50 мс; время валидационного ответа сервера через AJAX — не более 300 мс.", "Расчет JS <= 50 мс, ответ сервера <= 300 мс"),
        ("NFR-03", "Доступность и надежность (Uptime)", "Коэффициент готовности веб-сервиса должен составлять не менее 99.5% в режиме 24/7 (суммарный нерегламентный простой не более 3.6 часов в месяц).", "Коэффициент готовности Uptime >= 99.5%"),
        ("NFR-04", "Изоляция и целостность транзакций", "Процедура резервирования слота времени должна выполняться в атомарной транзакции с пессимистической блокировкой строк, исключая перезапись данных.", "0 коллизий при одновременных заказах"),
        ("NFR-05", "Безопасность хранения паролей и сессий", "Пароли пользователей должны хэшироваться с использованием стойкого алгоритма PBKDF2 с SHA-256 (не менее 390 000 итераций). Cookies сессий должны иметь флаги HttpOnly и SameSite=Lax.", "PBKDF2 SHA-256, HttpOnly=True"),
        ("NFR-06", "Ограничение загружаемых медиафайлов", "Максимальный объем загружаемых фотографий интерьеров и меню не должен превышать 5 МБ. Поддерживаемые форматы: JPEG, PNG, WebP с валидацией MIME-типа.", "Размер файла <= 5 МБ, форматы JPG/PNG/WebP"),
        ("NFR-07", "Глубина хранения аудиторских логов", "Системные журналы авторизации, изменений статусов заказов и финансовых транзакций должны гарантированно храниться не менее 30 дней.", "Срок хранения логов >= 30 календарных дней"),
        ("NFR-08", "Резервное копирование и восстановление", "Резервное копирование БД должно выполняться ежесуточно в 03:00. Целевое время восстановления (RTO) не более 30 минут, потеря данных (RPO) не более 24 часов.", "RTO <= 30 мин, RPO <= 24 ч, бэкап 1 раз в сутки"),
        ("NFR-09", "Нагрузочная способность (Конкурентность)", "Серверная часть должна стабильно обслуживать до 50 одновременно активных пользовательских сессий без сбоев и роста времени отклика выше 2.0 секунд.", "До 50 одновременных сессий, отклик <= 2.0 с"),
        ("NFR-10", "Адаптивность и кроссбраузерность", "Интерфейс должен обеспечивать 100% сохранение функционала на экранах от 360 до 1440+ px в браузерах Chrome 115+, Firefox 115+, Edge 115+, Safari 16+.", "Брейкпоинты 360, 768, 1024, 1440 px")
    ]

    tbl_b = doc.add_table(rows=len(app_b_rows) + 1, cols=4)
    tbl_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_b, color="000000", sz="4", val="single")

    col_h_b = ["ID", "Категория требования", "Формулировка нефункционального требования", "Измеримая метрика"]
    for c_i, h in enumerate(col_h_b):
        cell = tbl_b.rows[0].cells[c_i]
        cell.text = h
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Mm(0)
        for r_item in p.runs:
            r_item.font.name = 'Times New Roman'
            r_item.font.size = Pt(9.5)
            r_item.font.bold = True
            r_item.font.color.rgb = RGBColor(0, 0, 0)

    for r_i, r_data in enumerate(app_b_rows):
        row = tbl_b.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Mm(0)
            for r_item in p.runs:
                r_item.font.name = 'Times New Roman'
                r_item.font.size = Pt(8.5)
                r_item.font.color.rgb = RGBColor(0, 0, 0)
                if c_i == 0:
                    r_item.font.bold = True

    col_widths_b_mm = [16, 38, 64, 48]
    for row in tbl_b.rows:
        for idx, w in enumerate(col_widths_b_mm):
            row.cells[idx].width = Mm(w)

    doc.add_page_break()

    # ==================== ПРИЛОЖЕНИЕ В ====================
    add_h1("ПРИЛОЖЕНИЕ В. АРХИТЕКТУРНО-СТРУКТУРНЫЕ СХЕМЫ СИСТЕМЫ")
    add_p("В приложении представлены графические архитектурные схемы: карта маршрутов веб-сервиса и логика работы интерактивного онлайн-визарда бронирования дорожек и столов с привязкой к тарифным ставкам и АРМ Администратора.")

    add_image("fig_4_01_site_map.png", "Рисунок 1 — Структурная схема навигации и карты веб-сервиса «Strike & Pocket»", width=Inches(6.2))
    add_p("На приведенной структурной схеме (Рисунок 1) наглядно показано разделение потоков: клиентский контур (каталог игровых зон, пошаговое онлайн-бронирование, предзаказ кухни/бара, оформление и статус в личном кабинете) и производственный закрытый контур клуба (интерактивная шахматка броней АРМ дежурного администратора зала, наряды заказов для барменов и официантов, управление тарифными ставками управляющего и аналитические финансовые отчеты).")

    add_image("fig_4_02_architecture.png", "Рисунок 2 — Архитектурно-функциональная схема модуля онлайн-бронирования и валидации тарифов", width=Inches(6.2))
    add_p("Схема процесса бронирования (Рисунок 2) отражает трехшаговый клиентский сценарий: выбор ресурса и даты на интерактивной SVG-схеме; выбор тайм-слота с контролем лимита игроков (до 6 чел. на дорожку) и автоматическим предложением аренды двух смежных дорожек; предзаказ позиций бара; передача параметров в асинхронный обработчик `/api/calculate-price/`, раздельно рассчитывающий дневные и вечерние часы относительно границы 18:00; атомарное сохранение брони в БД с пессимистической блокировкой слота на 10 минут и автоматической отправкой push-оповещения в АРМ Администратора клуба.")

    doc.add_page_break()

    # ==================== СПИСОК ИСТОЧНИКОВ ====================
    add_h1("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ")
    sources = [
        "ГОСТ 19.201-78. Единая система программной документации. Техническое задание. Требования к содержанию и оформлению. — М.: Стандартинформ, 2010.",
        "ГОСТ 19.101-77. Единая система программной документации. Виды программ и программных документов. — М.: Стандартинформ, 2010.",
        "ГОСТ Р ИСО 31000-2019. Менеджмент риска. Принципы и руководство. — М.: Стандартинформ, 2020.",
        "ГОСТ Р 52872-2019. Интернет-ресурсы и другая информация, представленная в электронно-цифровой форме. Приложения для стационарных и мобильных устройств, иные пользовательские интерфейсы. Требования доступности для людей с инвалидностью и других лиц с ограничениями жизнедеятельности.",
        "ГОСТ Р ИСО/МЭК 25010-2015. Системная и программная инженерия. Требования и оценка качества систем и программного обеспечения (SQuaRE). Модели качества систем и программных продуктов. — М.: Стандартинформ, 2015.",
        "Федеральный закон «О применении контрольно-кассовой техники при осуществлении расчетов в Российской Федерации» от 22.05.2003 № 54-ФЗ (ред. от 08.08.2024).",
        "Документация по фреймворку Django 4.2 LTS / 5.1 [Электронный ресурс]. — URL: https://docs.djangoproject.com/ (дата обращения: 15.11.2024)."
    ]
    for s in sources:
        add_p(s, indent=True, space_after=2)

    output_doc = "TZ_Variant_4_Gost_19.201-78.docx"
    doc.save(output_doc)
    print(f"Техническое задание успешно сохранено в: {output_doc}")

if __name__ == '__main__':
    create_tz_document()
