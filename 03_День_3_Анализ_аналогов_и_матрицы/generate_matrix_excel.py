import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Матрица функций"

# Title
ws.merge_cells("A1:O1")
title_cell = ws["A1"]
title_cell.value = "Матрица анализа функций 10 сайтов-аналогов (Вариант №4: Боулинг и бильярд)"
title_cell.font = Font(name="Times New Roman", size=14, bold=True, color="1F497D")
title_cell.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 30

headers = [
    "№", "Наименование функции системы", 
    "cosmik.ru", "brooklyn\nbowl.ru", "samokat.ru", "more-on.ru", "billiard\nmsk.ru", 
    "bibabo.ru", "fregat-\nclub.ru", "baza-\nbilliard.ru", "bowlero.com\n(США)", "allstarlanes\n.co.uk (UK)", 
    "Всего есть", "% внедрения", "Статус в нашем проекте"
]

ws.append([]) # row 2
ws.row_dimensions[3].height = 40

for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=3, column=col_idx, value=h)
    cell.font = Font(name="Times New Roman", size=10, bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

matrix_data = [
    (1, "Каталог игровых зон (дорожки боулинга, столы бильярда)", "+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "Обязательная"),
    (2, "Отображение почасовой сетки тарифов (будни / выходные)", "+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "Обязательная"),
    (3, "Онлайн-проверка доступности слотов в реальном времени", "-", "+", "-", "+/-", "-", "-", "-", "-", "+", "+", "Обязательная"),
    (4, "Интерактивная схема залов с выбором конкретного номера дорожки", "-", "+", "-", "-", "-", "-", "+/-", "-", "-", "-", "Отличие (наше УТП)"),
    (5, "Автоматический расчет цены на стыке дневного и вечернего тарифов", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+/-", "Отличие (наше УТП)"),
    (6, "Контроль лимита 6 гостей с требованием второй дорожки", "-", "-", "-", "-", "-", "-", "-", "-", "+/-", "+/-", "Отличие (наше УТП)"),
    (7, "Предварительный заказ блюд и напитков бара к дорожке", "-", "-", "-", "-", "-", "-", "-", "-", "+/-", "+", "Отличие (наше УТП)"),
    (8, "Онлайн-оплата банковской картой / предоплата", "+/-", "+", "-", "-", "-", "-", "-", "-", "+", "+", "Обязательная (эмуляция)"),
    (9, "Личный кабинет пользователя с историей бронирований", "-", "+", "-", "-", "-", "-", "-", "-", "+", "+", "Обязательная"),
    (10, "Привязка клубной дисконтной карты в личном кабинете", "+/-", "-", "-", "-", "-", "-", "-", "-", "-", "+/-", "Отличие (наше УТП)"),
    (11, "Накопительная система скидок (автоповышение уровня)", "-", "-", "-", "-", "-", "-", "-", "-", "+", "+", "Отличие (наше УТП)"),
    (12, "Полнотекстовый поиск по меню бара и услугам залов", "+", "+", "-", "+", "-", "-", "+", "-", "+", "+", "Обязательная"),
    (13, "Фильтрация каталога (по типу игры, цене, VIP-статусу)", "-", "+", "-", "+", "+", "-", "-", "+", "+", "+", "Обязательная"),
    (14, "Сортировка каталога (по названию, цене, популярности)", "-", "+", "-", "-", "-", "-", "-", "-", "+", "+", "Обязательная"),
    (15, "Формирование печатного талона брони с реквизитами / QR", "-", "-", "-", "-", "-", "-", "-", "-", "+", "+", "Обязательная"),
    (16, "Отправка email-уведомлений при бронировании и смене статуса", "+", "+", "-", "+", "-", "-", "-", "-", "+", "+", "Обязательная"),
    (17, "Панель оператора зала для отметки визита гостей в 1 клик", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "Обязательная"),
    (18, "Экспорт журнала бронирований смены в CSV-формат", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "Обязательная")
]

thin_border = Border(
    left=Side(style='thin', color='D0D0D0'),
    right=Side(style='thin', color='D0D0D0'),
    top=Side(style='thin', color='D0D0D0'),
    bottom=Side(style='thin', color='D0D0D0')
)

for row_i, row_data in enumerate(matrix_data, 4):
    num, name, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, status = row_data
    # calculate counts
    sites = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
    total_has = sum(1 for s in sites if s == "+") + sum(0.5 for s in sites if s == "+/-")
    pct = (total_has / 10.0) * 100
    
    ws.cell(row=row_i, column=1, value=num)
    ws.cell(row=row_i, column=2, value=name)
    for c_idx, val in enumerate(sites, 3):
        cell = ws.cell(row=row_i, column=c_idx, value=val)
        if val == "+":
            cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
            cell.font = Font(name="Times New Roman", size=10, bold=True, color="375623")
        elif val == "+/-":
            cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
            cell.font = Font(name="Times New Roman", size=10, bold=True, color="7F6000")
        else:
            cell.fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
            cell.font = Font(name="Times New Roman", size=10, color="C65911")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    c_tot = ws.cell(row=row_i, column=13, value=f"{total_has:g} из 10")
    c_tot.alignment = Alignment(horizontal="center", vertical="center")
    c_tot.font = Font(name="Times New Roman", size=10, bold=True)
    c_tot.border = thin_border
    
    c_pct = ws.cell(row=row_i, column=14, value=f"{pct:.0f}%")
    c_pct.alignment = Alignment(horizontal="center", vertical="center")
    c_pct.font = Font(name="Times New Roman", size=10, bold=True)
    c_pct.border = thin_border
    
    c_stat = ws.cell(row=row_i, column=15, value=status)
    if "Отличие" in status:
        c_stat.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        c_stat.font = Font(name="Times New Roman", size=9, bold=True, color="203764")
    else:
        c_stat.font = Font(name="Times New Roman", size=9)
    c_stat.border = thin_border
    
    ws.cell(row=row_i, column=1).alignment = Alignment(horizontal="center", vertical="center")
    ws.cell(row=row_i, column=1).border = thin_border
    ws.cell(row=row_i, column=1).font = Font(name="Times New Roman", size=10)
    
    ws.cell(row=row_i, column=2).alignment = Alignment(horizontal="left", vertical="center")
    ws.cell(row=row_i, column=2).border = thin_border
    ws.cell(row=row_i, column=2).font = Font(name="Times New Roman", size=10)
    ws.row_dimensions[row_i].height = 22

# Column widths
ws.column_dimensions['A'].width = 5
ws.column_dimensions['B'].width = 46
for col_char in ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:
    ws.column_dimensions[col_char].width = 11
ws.column_dimensions['M'].width = 12
ws.column_dimensions['N'].width = 12
ws.column_dimensions['O'].width = 24

wb.save("Matritsa_funktsiy_Variant_4.xlsx")
print("Saved Matritsa_funktsiy_Variant_4.xlsx successfully!")
