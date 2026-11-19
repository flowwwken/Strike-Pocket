import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('screenshots', exist_ok=True)

def get_font(size=12, bold=False):
    font_name = 'arialbd.ttf' if bold else 'arial.ttf'
    path = os.path.join('C:/Windows/Fonts', font_name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_browser_frame(draw, url, title, w=1000, h=600):
    # Browser window background
    draw.rectangle([(0, 0), (w, h)], fill=(255, 255, 255))
    
    # Browser top header / tab bar
    draw.rectangle([(0, 0), (w, 36)], fill=(230, 233, 238))
    # Tab
    draw.rectangle([(80, 6), (280, 36)], fill=(255, 255, 255))
    f_tab = get_font(11)
    draw.text((95, 13), title[:26], font=f_tab, fill=(40, 40, 40))
    # Close tab 'x'
    draw.text((265, 13), "×", font=get_font(12, bold=True), fill=(100, 100, 100))
    
    # Navigation bar
    draw.rectangle([(0, 36), (w, 74)], fill=(245, 246, 248))
    draw.line([(0, 74), (w, 74)], fill=(215, 218, 222), width=1)
    
    # Back, Forward, Refresh icons
    f_nav = get_font(14, bold=True)
    draw.text((16, 44), "←", font=f_nav, fill=(120, 120, 120))
    draw.text((44, 44), "→", font=f_nav, fill=(180, 180, 180))
    draw.text((72, 44), "⟳", font=f_nav, fill=(100, 100, 100))
    
    # Address bar
    draw.rounded_rectangle([(105, 42), (w - 70, 68)], radius=12, fill=(255, 255, 255), outline=(205, 210, 215), width=1)
    f_url = get_font(11)
    # Lock icon
    draw.text((118, 48), "🔒", font=get_font(10), fill=(40, 160, 60))
    draw.text((138, 48), url, font=f_url, fill=(50, 50, 50))
    
    # User / menu icon
    draw.text((w - 50, 46), "⋮", font=get_font(16, bold=True), fill=(100, 100, 100))

# ----------------- SITE 1: COSMIK.RU -----------------
def render_cosmik_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://cosmik.ru/", "Сеть парков развлечений Космик")
    
    # Site Header (Navy blue)
    d.rectangle([(0, 75), (1000, 135)], fill=(15, 30, 65))
    d.text((40, 92), "КОСМИК", font=get_font(22, bold=True), fill=(255, 200, 0))
    d.text((160, 99), "ПАРКИ РАЗВЛЕЧЕНИЙ", font=get_font(10), fill=(200, 210, 230))
    
    menu_items = ["Боулинг", "Бильярд", "Лазертаг", "Рестораны", "Детям", "Акции", "Контакты"]
    for i, m in enumerate(menu_items):
        d.text((360 + i*85, 98), m, font=get_font(12, bold=(m=="Боулинг")), fill=(255, 255, 255) if m!="Боулинг" else (255, 200, 0))
    
    # Hero Banner
    d.rectangle([(40, 155), (960, 360)], fill=(25, 45, 90))
    d.text((80, 190), "БОУЛИНГ МИРОВОГО УРОВНЯ В МОСКВЕ", font=get_font(20, bold=True), fill=(255, 255, 255))
    d.text((80, 230), "Современные дорожки Brunswick, детские бортики и уютные лаунж-зоны", font=get_font(13), fill=(210, 225, 250))
    d.text((80, 255), "Специальные цены для студентов и именинников от 750 ₽/час", font=get_font(12), fill=(255, 215, 0))
    
    # Button
    d.rounded_rectangle([(80, 290), (280, 335)], radius=6, fill=(240, 60, 60))
    d.text((105, 303), "ЗАБРОНИРОВАТЬ", font=get_font(12, bold=True), fill=(255, 255, 255))
    
    # Cards section
    d.text((40, 385), "Популярные клубы сети:", font=get_font(15, bold=True), fill=(30, 30, 50))
    clubs = [
        ("ТЦ «Европейский»", "16 дорожек Brunswick, VIP-зона, спортбар", "от 950 ₽/час"),
        ("ТРЦ «Афимолл Сити»", "14 дорожек, космический неоновый свет, караоке", "от 1 100 ₽/час"),
        ("ТЦ «Капитолий»", "12 дорожек, русский бильярд и американский пул", "от 850 ₽/час")
    ]
    for i, (name, desc, price) in enumerate(clubs):
        x = 40 + i*315
        d.rounded_rectangle([(x, 420), (x+300, 560)], radius=6, fill=(245, 248, 252), outline=(210, 220, 235), width=1)
        d.rectangle([(x, 420), (x+300, 470)], fill=(40, 70, 130))
        d.text((x+15, 438), name, font=get_font(13, bold=True), fill=(255, 255, 255))
        d.text((x+15, 485), desc[:36], font=get_font(10), fill=(80, 80, 90))
        d.text((x+15, 502), desc[36:], font=get_font(10), fill=(80, 80, 90))
        d.text((x+15, 530), price, font=get_font(13, bold=True), fill=(220, 50, 50))
        d.rounded_rectangle([(x+190, 523), (x+285, 553)], radius=4, fill=(15, 30, 65))
        d.text((x+205, 532), "Выбрать", font=get_font(10, bold=True), fill=(255, 255, 255))
        
    img.save("screenshots/fig_3_01_cosmik_main.png")

def render_cosmik_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://cosmik.ru/bowling/booking", "Космик — Тарифы и бронирование дорожек")
    
    d.rectangle([(0, 75), (1000, 125)], fill=(15, 30, 65))
    d.text((40, 88), "КОСМИК", font=get_font(18, bold=True), fill=(255, 200, 0))
    d.text((150, 93), "Главная  /  Боулинг  /  Бронирование и тарифы", font=get_font(11), fill=(190, 205, 230))
    
    # Title
    d.text((40, 140), "Тарифная сетка клуба «Космик — Капитолий»", font=get_font(16, bold=True), fill=(20, 30, 60))
    
    # Table header
    d.rectangle([(40, 175), (580, 205)], fill=(230, 235, 245))
    d.text((50, 183), "Дни недели", font=get_font(11, bold=True), fill=(30, 40, 70))
    d.text((220, 183), "Дневной (до 18:00)", font=get_font(11, bold=True), fill=(30, 40, 70))
    d.text((410, 183), "Вечерний (после 18:00)", font=get_font(11, bold=True), fill=(30, 40, 70))
    
    rates = [
        ("Понедельник – Четверг", "850 ₽ / час", "1 450 ₽ / час"),
        ("Пятница", "950 ₽ / час", "1 850 ₽ / час"),
        ("Суббота (весь день)", "1 950 ₽ / час", "1 950 ₽ / час"),
        ("Воскресенье", "1 650 ₽ / час", "1 650 ₽ / час")
    ]
    for r_i, (days, day_p, night_p) in enumerate(rates):
        y = 205 + r_i * 32
        d.rectangle([(40, y), (580, y+32)], fill=(255, 255, 255) if r_i%2==0 else (248, 250, 254), outline=(220, 225, 235), width=1)
        d.text((50, y+8), days, font=get_font(11), fill=(40, 40, 40))
        d.text((230, y+8), day_p, font=get_font(11, bold=True), fill=(40, 140, 40))
        d.text((420, y+8), night_p, font=get_font(11, bold=True), fill=(200, 40, 40))
        
    # Form on the right (heavy external widget)
    d.rounded_rectangle([(610, 145), (960, 560)], radius=8, fill=(250, 252, 255), outline=(190, 205, 225), width=1)
    d.rectangle([(610, 145), (960, 185)], fill=(30, 60, 120))
    d.text((630, 155), "Онлайн-заявка на дорожку", font=get_font(13, bold=True), fill=(255, 255, 255))
    
    fields = [("Ваше имя:", "Иван Иванов"), ("Телефон:", "+7 (999) 000-00-00"), ("Дата игры:", "15.11.2024"), ("Время старта:", "17:00"), ("Количество часов:", "2 часа")]
    for f_i, (lbl, ph) in enumerate(fields):
        fy = 200 + f_i * 55
        d.text((630, fy), lbl, font=get_font(10, bold=True), fill=(60, 70, 90))
        d.rounded_rectangle([(630, fy+18), (940, fy+46)], radius=4, fill=(255, 255, 255), outline=(180, 190, 205), width=1)
        d.text((640, fy+26), ph, font=get_font(10), fill=(130, 140, 150))
        
    d.rounded_rectangle([(630, 485), (940, 530)], radius=6, fill=(220, 50, 50))
    d.text((710, 500), "ОТПРАВИТЬ ЗАЯВКУ", font=get_font(11, bold=True), fill=(255, 255, 255))
    d.text((630, 540), "*Оператор свяжется с вами для подтверждения брони", font=get_font(8), fill=(120, 130, 140))
    
    img.save("screenshots/fig_3_02_cosmik_inner.png")

# ----------------- SITE 2: BROOKLYN BOWL -----------------
def render_brooklyn_main():
    img = Image.new('RGB', (1000, 600), color=(18, 18, 22))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://brooklynbowl.ru/", "Brooklyn Bowl — Сеть боулинг-ресторанов")
    
    # Header Dark theme
    d.rectangle([(0, 75), (1000, 140)], fill=(25, 26, 32))
    d.text((40, 92), "BROOKLYN BOWL", font=get_font(20, bold=True), fill=(255, 215, 0))
    d.text((225, 99), "БОУЛИНГ • РЕСТОРАН • КОНЦЕРТЫ", font=get_font(9), fill=(160, 165, 180))
    
    menus = ["О нас", "Дорожки", "Меню кухни", "Барная карта", "Мероприятия", "Акции", "Контакты"]
    for i, m in enumerate(menus):
        d.text((380 + i*75, 99), m, font=get_font(11), fill=(220, 225, 240))
    d.rounded_rectangle([(900, 90), (960, 125)], radius=4, fill=(255, 215, 0))
    d.text((912, 100), "Вход", font=get_font(11, bold=True), fill=(20, 20, 20))
    
    # Hero Neon section
    d.rectangle([(40, 160), (960, 380)], fill=(32, 34, 44))
    d.text((80, 200), "БОУЛИНГ С АТМОСФЕРОЙ НАСТОЯЩЕГО ПРАЗДНИКА", font=get_font(20, bold=True), fill=(255, 255, 255))
    d.text((80, 240), "16 дорожек с новейшей подсветкой, авторские бургеры, пицца и живой звук", font=get_font(13), fill=(200, 205, 220))
    d.text((80, 270), "Тюмень • Ижевск • Сургут • Нижневартовск", font=get_font(12, bold=True), fill=(255, 215, 0))
    
    d.rounded_rectangle([(80, 310), (290, 355)], radius=6, fill=(255, 215, 0))
    d.text((105, 323), "ЗАБРОНИРОВАТЬ СТОЛ", font=get_font(12, bold=True), fill=(20, 20, 20))
    
    # Features grid
    feats = [
        ("Профессиональные дорожки", "Оборудование QubicaAMF с автоматическими бортиками"),
        ("Гастрономический ресторан", "Блюда от шеф-повара, пицца из дровяной печи"),
        ("Программа привилегий", "Бонусы до 15% на карту лояльности в приложении")
    ]
    for i, (f_title, f_desc) in enumerate(feats):
        x = 40 + i*315
        d.rounded_rectangle([(x, 405), (x+300, 555)], radius=6, fill=(28, 30, 38), outline=(50, 54, 68), width=1)
        d.text((x+20, 425), f"0{i+1}", font=get_font(20, bold=True), fill=(255, 215, 0))
        d.text((x+20, 465), f_title, font=get_font(12, bold=True), fill=(255, 255, 255))
        d.text((x+20, 495), f_desc[:36], font=get_font(10), fill=(160, 165, 180))
        d.text((x+20, 515), f_desc[36:], font=get_font(10), fill=(160, 165, 180))
        
    img.save("screenshots/fig_3_03_brooklyn_main.png")

def render_brooklyn_inner():
    img = Image.new('RGB', (1000, 600), color=(18, 18, 22))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://brooklynbowl.ru/booking/lanes", "Brooklyn Bowl — Выбор дорожек онлайн")
    
    d.rectangle([(0, 75), (1000, 130)], fill=(25, 26, 32))
    d.text((40, 88), "BROOKLYN BOWL", font=get_font(18, bold=True), fill=(255, 215, 0))
    d.text((220, 93), "Онлайн-бронирование дорожек в клубе", font=get_font(12), fill=(180, 185, 200))
    
    # Booking step widget
    d.rectangle([(40, 145), (960, 205)], fill=(30, 32, 40))
    steps = ["1. Дата и время", "2. Выбор дорожки", "3. Заказ по меню", "4. Оплата"]
    for i, s in enumerate(steps):
        col = (255, 215, 0) if i==1 else (150, 155, 170)
        d.text((60 + i*230, 168), s, font=get_font(12, bold=(i==1)), fill=col)
        
    # Interactive lane scheme representation
    d.text((40, 225), "Схема дорожек на 15.11.2024 (Слот: 18:00 - 20:00):", font=get_font(13, bold=True), fill=(255, 255, 255))
    d.text((40, 245), "Зеленый — свободно, Красный — занято, Желтый — ваш выбор", font=get_font(10), fill=(160, 165, 180))
    
    for lane_i in range(1, 13):
        lx = 40 + ((lane_i-1)%6)*155
        ly = 275 + ((lane_i-1)//6)*105
        # color status
        if lane_i in [3, 4, 7, 8, 10]:
            c_fill, c_bord, c_stat = (60, 25, 25), (180, 40, 40), "Занято"
        elif lane_i == 5:
            c_fill, c_bord, c_stat = (70, 60, 20), (255, 215, 0), "Выбрано"
        else:
            c_fill, c_bord, c_stat = (25, 55, 30), (40, 160, 60), "Свободно"
            
        d.rounded_rectangle([(lx, ly), (lx+140, ly+85)], radius=6, fill=c_fill, outline=c_bord, width=2)
        d.text((lx+15, ly+12), f"Дорожка №{lane_i}", font=get_font(11, bold=True), fill=(255, 255, 255))
        d.text((lx+15, ly+35), f"Статус: {c_stat}", font=get_font(9), fill=(220, 220, 220))
        d.text((lx+15, ly+55), "1 600 ₽/час", font=get_font(10, bold=True), fill=(255, 215, 0))
        
    # Bottom checkout summary
    d.rectangle([(40, 500), (960, 560)], fill=(32, 34, 44), outline=(60, 65, 80), width=1)
    d.text((60, 520), "Выбрана Дорожка №5 (2 часа) • Гостей: 4 чел. • Сумма: 3 200 ₽", font=get_font(12, bold=True), fill=(255, 255, 255))
    d.rounded_rectangle([(770, 510), (940, 550)], radius=4, fill=(255, 215, 0))
    d.text((795, 522), "ПРОДОЛЖИТЬ", font=get_font(11, bold=True), fill=(20, 20, 20))
    
    img.save("screenshots/fig_3_04_brooklyn_inner.png")

# ----------------- SITE 3: SAMOKAT.RU -----------------
def render_samokat_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://samokat.ru/", "Развлекательный комплекс Самокат — Боулинг и Бильярд")
    
    d.rectangle([(0, 75), (1000, 135)], fill=(180, 25, 25))
    d.text((40, 90), "САМОКАТ", font=get_font(24, bold=True), fill=(255, 255, 255))
    d.text((180, 98), "РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС В ЦЕНТРЕ МОСКВЫ", font=get_font(9, bold=True), fill=(255, 220, 220))
    
    m_items = ["Боулинг", "Бильярдный клуб", "Караоке", "Банкеты", "Цены", "Контакты"]
    for i, m in enumerate(m_items):
        d.text((460 + i*85, 98), m, font=get_font(11, bold=True), fill=(255, 255, 255))
        
    # Hero Banner
    d.rectangle([(40, 155), (960, 360)], fill=(245, 245, 248), outline=(220, 220, 225), width=1)
    d.text((70, 185), "12 ДОРОЖЕК ДЛЯ БОУЛИНГА И 14 БИЛЬЯРДНЫХ СТОЛОВ", font=get_font(18, bold=True), fill=(160, 20, 20))
    d.text((70, 225), "Набережная Академика Туполева, д. 15. Удобная парковка и панорамный вид", font=get_font(12), fill=(60, 60, 60))
    d.text((70, 255), "Специальные дневные тарифы для школьников, студентов и пенсионеров", font=get_font(11), fill=(100, 100, 100))
    
    d.rounded_rectangle([(70, 295), (280, 340)], radius=4, fill=(180, 25, 25))
    d.text((95, 308), "ПОЗВОНИТЬ В КЛУБ", font=get_font(11, bold=True), fill=(255, 255, 255))
    d.text((310, 308), "+7 (495) 925-50-50 (круглосуточно)", font=get_font(12, bold=True), fill=(30, 30, 30))
    
    # Grid 2 columns
    d.rounded_rectangle([(40, 385), (480, 560)], radius=6, fill=(255, 255, 255), outline=(200, 200, 210), width=1)
    d.rectangle([(40, 385), (480, 425)], fill=(50, 50, 60))
    d.text((60, 396), "Зона Боулинга", font=get_font(13, bold=True), fill=(255, 255, 255))
    d.text((60, 440), "• 12 профессиональных дорожек Brunswick\n• Интерактивная система подсчета очков\n• Детские бортики и легкие шары (от 6 фунтов)\n• До 6 человек на одну дорожку", font=get_font(11), fill=(50, 50, 50))
    
    d.rounded_rectangle([(520, 385), (960, 560)], radius=6, fill=(255, 255, 255), outline=(200, 200, 210), width=1)
    d.rectangle([(520, 385), (960, 425)], fill=(30, 80, 40))
    d.text((540, 396), "Бильярдный Клуб", font=get_font(13, bold=True), fill=(255, 255, 255))
    d.text((540, 440), "• 10 двенадцатифутовых столов для Русской пирамиды\n• 4 стола для Американского пула\n• VIP-зал с отдельным обслуживанием\n• Профессиональное сукно Iwan Simonis", font=get_font(11), fill=(50, 50, 50))
    
    img.save("screenshots/fig_3_05_samokat_main.png")

def render_samokat_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://samokat.ru/bowling-prices", "РК Самокат — Стоимость дорожек и бильярда")
    
    d.rectangle([(0, 75), (1000, 125)], fill=(180, 25, 25))
    d.text((40, 88), "САМОКАТ", font=get_font(18, bold=True), fill=(255, 255, 255))
    d.text((170, 93), "Прайс-лист на услуги боулинга и бильярда", font=get_font(11), fill=(255, 230, 230))
    
    d.text((40, 145), "Прейскурант цен на дорожки боулинга (рублей за 1 час):", font=get_font(14, bold=True), fill=(30, 30, 30))
    
    # Detailed Price Table
    d.rectangle([(40, 175), (960, 210)], fill=(240, 240, 245))
    d.text((50, 185), "Тарифная зона / Время", font=get_font(11, bold=True), fill=(30, 30, 30))
    d.text((320, 185), "Пн – Чт", font=get_font(11, bold=True), fill=(30, 30, 30))
    d.text((480, 185), "Пятница", font=get_font(11, bold=True), fill=(30, 30, 30))
    d.text((640, 185), "Суббота", font=get_font(11, bold=True), fill=(30, 30, 30))
    d.text((800, 185), "Воскресенье", font=get_font(11, bold=True), fill=(30, 30, 30))
    
    p_rows = [
        ("Утренний (12:00 – 15:00)", "700 ₽", "800 ₽", "1 500 ₽", "1 400 ₽"),
        ("Дневной (15:00 – 18:00)", "900 ₽", "1 100 ₽", "1 800 ₽", "1 600 ₽"),
        ("Вечерний (18:00 – 02:00)", "1 500 ₽", "1 900 ₽", "2 100 ₽", "1 800 ₽"),
        ("Ночной (02:00 – 06:00)", "1 100 ₽", "1 400 ₽", "1 600 ₽", "1 200 ₽")
    ]
    for r_i, (t_time, p1, p2, p3, p4) in enumerate(p_rows):
        y = 210 + r_i * 35
        d.rectangle([(40, y), (960, y+35)], fill=(255, 255, 255) if r_i%2==0 else (248, 249, 251), outline=(215, 220, 230), width=1)
        d.text((50, y+9), t_time, font=get_font(11), fill=(40, 40, 40))
        d.text((330, y+9), p1, font=get_font(11, bold=True), fill=(40, 120, 40))
        d.text((490, y+9), p2, font=get_font(11, bold=True), fill=(40, 120, 40))
        d.text((650, y+9), p3, font=get_font(11, bold=True), fill=(180, 40, 40))
        d.text((810, y+9), p4, font=get_font(11, bold=True), fill=(180, 40, 40))
        
    # Note box
    d.rounded_rectangle([(40, 380), (960, 480)], radius=6, fill=(255, 250, 240), outline=(235, 190, 100), width=1)
    d.text((60, 395), "ВАЖНАЯ ИНФОРМАЦИЯ ПО ТАРИФИКАЦИИ:", font=get_font(11, bold=True), fill=(160, 80, 10))
    d.text((60, 420), "1. На одну дорожку допускается компания не более 6 человек. Начиная с 7-го человека требуется аренда второй дорожки.", font=get_font(10), fill=(60, 50, 30))
    d.text((60, 442), "2. При переходе времени игры через границу тарифов расчет производится пропорционально сыгранному времени.", font=get_font(10), fill=(60, 50, 30))
    
    # Callback form
    d.text((40, 510), "Для бронирования свяжитесь с администратором:", font=get_font(12, bold=True), fill=(30, 30, 30))
    d.rounded_rectangle([(400, 505), (650, 545)], radius=4, fill=(180, 25, 25))
    d.text((435, 518), "ЗАКАЗАТЬ ЗВОНОК", font=get_font(11, bold=True), fill=(255, 255, 255))
    
    img.save("screenshots/fig_3_06_samokat_inner.png")

# ----------------- SITES 4 - 10: SIMPLE CRISP RENDERERS -----------------
def render_moreon_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://more-on.ru/bowling/", "Мореон Боулинг — Развлекательный комплекс в Москве")
    d.rectangle([(0, 75), (1000, 135)], fill=(0, 114, 206))
    d.text((40, 92), "МОРЕОН", font=get_font(22, bold=True), fill=(255, 255, 255))
    d.text((170, 99), "АКВАПАРК • ТЕРМЫ • СПА • БОУЛИНГ", font=get_font(10), fill=(200, 230, 255))
    d.rectangle([(40, 160), (960, 380)], fill=(230, 245, 255))
    d.text((80, 200), "СЕМЕЙНЫЙ БОУЛИНГ В ЯСЕНЕВО", font=get_font(20, bold=True), fill=(0, 80, 160))
    d.text((80, 240), "12 дорожек Brunswick с детскими автоматическими бортиками и рестораном", font=get_font(13), fill=(40, 60, 80))
    d.rounded_rectangle([(80, 290), (280, 335)], radius=4, fill=(255, 120, 0))
    d.text((115, 303), "КУПИТЬ БИЛЕТ", font=get_font(12, bold=True), fill=(255, 255, 255))
    img.save("screenshots/fig_3_07_moreon_main.png")

def render_moreon_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://more-on.ru/bowling/tarify/", "Мореон — Бронирование и цены на боулинг")
    d.rectangle([(0, 75), (1000, 125)], fill=(0, 114, 206))
    d.text((40, 88), "МОРЕОН", font=get_font(18, bold=True), fill=(255, 255, 255))
    d.text((40, 150), "Тарифы на дорожки боулинга (руб/час)", font=get_font(16, bold=True), fill=(30, 30, 40))
    d.rectangle([(40, 190), (960, 350)], fill=(245, 248, 252), outline=(200, 215, 235), width=1)
    d.text((60, 220), "Будние дни (Пн-Чт до 18:00): 900 ₽ / час\nБудние дни (Пн-Чт после 18:00): 1 600 ₽ / час\nПятница (с 17:00): 1 950 ₽ / час\nВыходные и праздники: 2 100 ₽ / час", font=get_font(13), fill=(40, 50, 70))
    img.save("screenshots/fig_3_08_moreon_inner.png")

def render_billiardmsk_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://billiardmsk.ru/", "Московская Академия Бильярда — Клуб и Обучение")
    d.rectangle([(0, 75), (1000, 135)], fill=(20, 45, 30))
    d.text((40, 92), "АКАДЕМИЯ БИЛЬЯРДА", font=get_font(20, bold=True), fill=(212, 175, 55))
    d.rectangle([(40, 160), (960, 380)], fill=(240, 245, 240))
    d.text((80, 210), "ПРОФЕССИОНАЛЬНЫЙ БИЛЬЯРД В МОСКВЕ", font=get_font(20, bold=True), fill=(20, 50, 30))
    d.text((80, 250), "Столы РуптуР и Dynamic для Пирамиды, Пула и Снукера. Обучение и аренда столов", font=get_font(12), fill=(60, 80, 65))
    img.save("screenshots/fig_3_09_billiardmsk_main.png")

def render_billiardmsk_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://billiardmsk.ru/arenda-stolov", "Академия Бильярда — Аренда столов и цены")
    d.rectangle([(0, 75), (1000, 125)], fill=(20, 45, 30))
    d.text((40, 88), "АКАДЕМИЯ БИЛЬЯРДА", font=get_font(18, bold=True), fill=(212, 175, 55))
    d.text((40, 150), "Каталог бильярдных залов и бронирование", font=get_font(16, bold=True), fill=(20, 50, 30))
    d.rectangle([(40, 190), (960, 360)], fill=(248, 250, 248), outline=(200, 215, 200), width=1)
    d.text((60, 220), "• Русский бильярд (12 футов, плита Ардезия) — от 700 ₽/час\n• Американский пул (9 футов) — от 550 ₽/час\n• Снукерный профессиональный стол (12 футов) — от 900 ₽/час\n• VIP-зал с персональным обслуживанием — от 1 800 ₽/час", font=get_font(13), fill=(40, 60, 45))
    img.save("screenshots/fig_3_10_billiardmsk_inner.png")

def render_bibabo_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://bibabo.ru/", "Боулинг-клуб Бибабо на Арбате")
    d.rectangle([(0, 75), (1000, 135)], fill=(40, 20, 60))
    d.text((40, 92), "BIBABO BOWLING", font=get_font(22, bold=True), fill=(255, 215, 0))
    d.rectangle([(40, 160), (960, 380)], fill=(250, 245, 255))
    d.text((80, 210), "ЛЕГЕНДАРНЫЙ БОУЛИНГ-КЛУБ НА АРБАТЕ", font=get_font(20, bold=True), fill=(50, 20, 70))
    d.text((80, 250), "Уютная клубная атмосфера, коктейльный бар и VIP-дорожки в историческом центре", font=get_font(12), fill=(80, 60, 100))
    img.save("screenshots/fig_3_11_bibabo_main.png")

def render_bibabo_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://bibabo.ru/menu-and-prices", "Бибабо — Меню бара и бронирование")
    d.rectangle([(0, 75), (1000, 125)], fill=(40, 20, 60))
    d.text((40, 88), "BIBABO BOWLING", font=get_font(18, bold=True), fill=(255, 215, 0))
    d.text((40, 150), "Меню ресторана и бара к дорожкам", font=get_font(16, bold=True), fill=(40, 20, 60))
    d.rectangle([(40, 190), (960, 360)], fill=(252, 250, 255), outline=(220, 210, 235), width=1)
    d.text((60, 220), "• Пицца «Четыре сыра» (450 г) — 650 ₽\n• Бургер фирменный «Бибабо» с картофелем фри — 590 ₽\n• Сет закусок к пиву для компании — 1 200 ₽\n• Безалкогольные лимонады и кофе — от 250 ₽", font=get_font(13), fill=(60, 40, 80))
    img.save("screenshots/fig_3_12_bibabo_inner.png")

def render_fregat_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://fregat-club.ru/", "РК Фрегат — Боулинг, бильярд, ресторан")
    d.rectangle([(0, 75), (1000, 135)], fill=(30, 50, 80))
    d.text((40, 92), "ФРЕГАТ КЛУБ", font=get_font(22, bold=True), fill=(240, 180, 50))
    d.rectangle([(40, 160), (960, 380)], fill=(240, 245, 250))
    d.text((80, 210), "РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС «ФРЕГАТ»", font=get_font(20, bold=True), fill=(30, 50, 80))
    d.text((80, 250), "8 дорожек боулинга, русский и американский бильярд, европейская кухня", font=get_font(12), fill=(60, 80, 100))
    img.save("screenshots/fig_3_13_fregat_main.png")

def render_fregat_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://fregat-club.ru/bowling-booking", "Фрегат — Бронирование дорожек")
    d.rectangle([(0, 75), (1000, 125)], fill=(30, 50, 80))
    d.text((40, 88), "ФРЕГАТ КЛУБ", font=get_font(18, bold=True), fill=(240, 180, 50))
    d.text((40, 150), "Бронирование дорожек и правила клуба", font=get_font(16, bold=True), fill=(30, 50, 80))
    d.rectangle([(40, 190), (960, 360)], fill=(245, 248, 252), outline=(210, 220, 235), width=1)
    d.text((60, 220), "• Почасовая тарификация от 800 ₽/час до 1 700 ₽/час\n• Максимальная посадка за столик дорожки — до 6 гостей\n• Бронирование по предварительному звонку или онлайн-заявке\n• Скидка 10% в день рождения", font=get_font(13), fill=(40, 60, 90))
    img.save("screenshots/fig_3_14_fregat_inner.png")

def render_baza_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://baza-billiard.ru/", "Бильярдный клуб БАЗА")
    d.rectangle([(0, 75), (1000, 135)], fill=(25, 28, 35))
    d.text((40, 92), "БАЗА БИЛЬЯРД", font=get_font(22, bold=True), fill=(220, 60, 60))
    d.rectangle([(40, 160), (960, 380)], fill=(35, 38, 48))
    d.text((80, 210), "КЛУБ ЛЮБИТЕЛЕЙ И ПРОФЕССИОНАЛОВ БИЛЬЯРДА", font=get_font(20, bold=True), fill=(255, 255, 255))
    d.text((80, 250), "Русская пирамида, американский пул, клубные турниры каждые выходные", font=get_font(12), fill=(180, 190, 205))
    img.save("screenshots/fig_3_15_baza_main.png")

def render_baza_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://baza-billiard.ru/tables", "Клуб БАЗА — Бронирование бильярдных столов")
    d.rectangle([(0, 75), (1000, 125)], fill=(25, 28, 35))
    d.text((40, 88), "БАЗА БИЛЬЯРД", font=get_font(18, bold=True), fill=(220, 60, 60))
    d.text((40, 150), "Прейскурант аренды столов", font=get_font(16, bold=True), fill=(255, 255, 255))
    d.rectangle([(40, 190), (960, 360)], fill=(32, 35, 45), outline=(60, 65, 80), width=1)
    d.text((60, 220), "• Стол Пирамида 12 футов (плита сланец): 650 ₽ / час\n• Стол Пул 9 футов: 500 ₽ / час\n• VIP-комната с бильярдом и ТВ: 1 500 ₽ / час\n• Прокат профессионального кия: 200 ₽ / сессия", font=get_font(13), fill=(220, 225, 235))
    img.save("screenshots/fig_3_16_baza_inner.png")

# --- FOREIGN SITES 9 & 10 ---
def render_bowlero_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://www.bowlero.com/", "Bowlero — Bowling, Arcade & Sports Bar (USA)")
    d.rectangle([(0, 75), (1000, 135)], fill=(230, 40, 40))
    d.text((40, 92), "BOWLERO", font=get_font(24, bold=True), fill=(255, 255, 255))
    d.text((190, 99), "BE EXCITE-ABLE • 300+ LOCATIONS ACROSS USA", font=get_font(10, bold=True), fill=(255, 230, 230))
    d.rectangle([(40, 160), (960, 380)], fill=(25, 25, 30))
    d.text((80, 200), "EPIC BOWLING, ARCADES & CRAFT COCKTAILS", font=get_font(20, bold=True), fill=(255, 255, 255))
    d.text((80, 240), "Blacklight bowling lanes, lane-side food service, and signature cocktails", font=get_font(13), fill=(220, 220, 230))
    d.rounded_rectangle([(80, 290), (280, 335)], radius=4, fill=(230, 40, 40))
    d.text((120, 303), "BOOK A LANE", font=get_font(12, bold=True), fill=(255, 255, 255))
    img.save("screenshots/fig_3_17_bowlero_main.png")

def render_bowlero_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://www.bowlero.com/book-a-lane", "Bowlero — Online Lane Reservation System")
    d.rectangle([(0, 75), (1000, 125)], fill=(230, 40, 40))
    d.text((40, 88), "BOWLERO", font=get_font(18, bold=True), fill=(255, 255, 255))
    d.text((40, 150), "Select Guests, Date and Bowling Package", font=get_font(16, bold=True), fill=(30, 30, 30))
    d.rectangle([(40, 190), (960, 360)], fill=(245, 247, 250), outline=(210, 215, 225), width=1)
    d.text((60, 220), "• Location: Times Square, New York, NY\n• Party Size: 2 - 6 Bowlers per lane (Add 2nd lane for 7+ guests)\n• Bowling Duration: 2 Hours ($45.99 / person including shoe rental)\n• Add-on: Lane-side Pizza & Soda Package ($24.99)", font=get_font(13), fill=(40, 40, 50))
    img.save("screenshots/fig_3_18_bowlero_inner.png")

def render_allstar_main():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://www.allstarlanes.co.uk/", "All Star Lanes — Boutique Bowling & Dining (UK)")
    d.rectangle([(0, 75), (1000, 135)], fill=(180, 40, 40))
    d.text((40, 92), "ALL STAR LANES", font=get_font(22, bold=True), fill=(255, 255, 255))
    d.text((260, 99), "LONDON • MANCHESTER • BOUTIQUE BOWLING", font=get_font(10), fill=(255, 225, 225))
    d.rectangle([(40, 160), (960, 380)], fill=(40, 30, 35))
    d.text((80, 200), "DRINK, DINE & BOWL IN RETRO AMERICAN STYLE", font=get_font(20, bold=True), fill=(255, 240, 220))
    d.text((80, 240), "Handcrafted burgers, classic cocktails and boutique bowling in Holborn, Brick Lane and Westfield", font=get_font(12), fill=(210, 200, 205))
    img.save("screenshots/fig_3_19_allstar_main.png")

def render_allstar_inner():
    img = Image.new('RGB', (1000, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_browser_frame(d, "https://www.allstarlanes.co.uk/booking", "All Star Lanes — Book a Lane & Food")
    d.rectangle([(0, 75), (1000, 125)], fill=(180, 40, 40))
    d.text((40, 88), "ALL STAR LANES", font=get_font(18, bold=True), fill=(255, 255, 255))
    d.text((40, 150), "Lane & Feast Online Booking Engine", font=get_font(16, bold=True), fill=(40, 20, 20))
    d.rectangle([(40, 190), (960, 360)], fill=(250, 248, 248), outline=(230, 210, 210), width=1)
    d.text((60, 220), "• Standard Game: £11.50 per adult / £8.50 per child\n• Feast & Bowl Package: 1 Game + 2 Course American Diner (£32.00 / person)\n• Peak / Off-peak transition rates applied automatically\n• Max 6 bowlers per lane (system adds adjacent lane for 7+ players)", font=get_font(13), fill=(50, 30, 35))
    img.save("screenshots/fig_3_20_allstar_inner.png")

def build_all_screenshots():
    render_cosmik_main()
    render_cosmik_inner()
    render_brooklyn_main()
    render_brooklyn_inner()
    render_samokat_main()
    render_samokat_inner()
    render_moreon_main()
    render_moreon_inner()
    render_billiardmsk_main()
    render_billiardmsk_inner()
    render_bibabo_main()
    render_bibabo_inner()
    render_fregat_main()
    render_fregat_inner()
    render_baza_main()
    render_baza_inner()
    render_bowlero_main()
    render_bowlero_inner()
    render_allstar_main()
    render_allstar_inner()
    print("All 20 screenshots generated successfully in 'screenshots/' folder!")

if __name__ == '__main__':
    build_all_screenshots()
