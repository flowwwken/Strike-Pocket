import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size=11, bold=False):
    font_name = 'arialbd.ttf' if bold else 'arial.ttf'
    path = os.path.join('C:/Windows/Fonts', font_name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_pool_and_lanes(draw, pool_title, lanes, width=1280, height=650):
    # Background
    draw.rectangle([(0, 0), (width, height)], fill=(255, 255, 255))
    
    # Pool border
    draw.rectangle([(15, 15), (width - 15, height - 15)], outline=(60, 60, 60), width=2)
    
    # Pool Header
    f_pool = get_font(12, bold=True)
    draw.rectangle([(15, 15), (55, height - 15)], fill=(225, 232, 245), outline=(60, 60, 60), width=2)
    
    # Render vertically stacked pool title
    y_text = 30
    for char in pool_title:
        draw.text((32, y_text), char, font=f_pool, fill=(20, 30, 60))
        y_text += 15
        if y_text > height - 35: break

    # Lanes
    num_lanes = len(lanes)
    lane_h = (height - 30) / num_lanes
    f_lane = get_font(11, bold=True)
    
    lane_coords = []
    for i, lane_title in enumerate(lanes):
        top_y = 15 + i * lane_h
        bot_y = top_y + lane_h
        lane_coords.append((top_y, bot_y))
        
        # Lane divider line
        if i > 0:
            draw.line([(55, top_y), (width - 15, top_y)], fill=(130, 130, 130), width=1)
            
        # Lane header box
        draw.rectangle([(55, top_y), (95, bot_y)], fill=(245, 248, 253), outline=(140, 140, 140), width=1)
        y_t = top_y + (lane_h - len(lane_title)*13)/2
        if y_t < top_y + 10: y_t = top_y + 10
        for char in lane_title:
            draw.text((72, y_t), char, font=f_lane, fill=(40, 50, 70))
            y_t += 13
            if y_t > bot_y - 13: break
            
    return lane_coords

def draw_arrow(draw, points, color=(60, 60, 60), width=2, arrow_size=6):
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    if x1 == x2: # vertical
        if y2 > y1:
            draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size*1.5), (x2 + arrow_size, y2 - arrow_size*1.5)], fill=color)
        else:
            draw.polygon([(x2, y2), (x2 - arrow_size, y2 + arrow_size*1.5), (x2 + arrow_size, y2 + arrow_size*1.5)], fill=color)
    else: # horizontal
        if x2 > x1:
            draw.polygon([(x2, y2), (x2 - arrow_size*1.5, y2 - arrow_size), (x2 - arrow_size*1.5, y2 + arrow_size)], fill=color)
        else:
            draw.polygon([(x2, y2), (x2 + arrow_size*1.5, y2 - arrow_size), (x2 + arrow_size*1.5, y2 + arrow_size)], fill=color)

def draw_multiline_text(draw, text, box, font, fill=(0, 0, 0), align='center'):
    x1, y1, x2, y2 = box
    box_w = x2 - x1
    box_h = y2 - y1
    words = text.split()
    lines = []
    curr_line = []
    for w in words:
        test_line = ' '.join(curr_line + [w])
        bbox = font.getbbox(test_line)
        if (bbox[2] - bbox[0]) <= box_w - 6:
            curr_line.append(w)
        else:
            if curr_line:
                lines.append(' '.join(curr_line))
            curr_line = [w]
    if curr_line:
        lines.append(' '.join(curr_line))
    
    total_h = len(lines) * (font.size + 3)
    start_y = y1 + (box_h - total_h) / 2
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        line_x = x1 + (box_w - w) / 2 if align == 'center' else x1 + 4
        line_y = start_y + i * (font.size + 3)
        draw.text((line_x, line_y), line, font=font, fill=fill)

def draw_task(draw, box, text, font, fill_color=(235, 245, 255), border_color=(40, 100, 180)):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=7, fill=fill_color, outline=border_color, width=2)
    draw_multiline_text(draw, text, box, font, fill=(15, 20, 30))

def draw_gateway(draw, center, label_top, font, fill_color=(255, 250, 220), border_color=(200, 140, 20)):
    cx, cy = center
    size = 19
    diamond = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(diamond, fill=fill_color, outline=border_color)
    draw.line([(cx - 6, cy - 6), (cx + 6, cy + 6)], fill=border_color, width=2)
    draw.line([(cx - 6, cy + 6), (cx + 6, cy - 6)], fill=border_color, width=2)
    if label_top:
        words = label_top.split()
        mid = len(words)//2 + 1 if len(words) > 2 else len(words)
        l1 = ' '.join(words[:mid])
        l2 = ' '.join(words[mid:])
        y_off = cy - size - font.size*2 - 2
        if l2:
            bbox1 = font.getbbox(l1)
            bbox2 = font.getbbox(l2)
            draw.text((cx - (bbox1[2]-bbox1[0])/2, y_off), l1, font=font, fill=(70, 50, 10))
            draw.text((cx - (bbox2[2]-bbox2[0])/2, y_off + font.size + 2), l2, font=font, fill=(70, 50, 10))
        else:
            bbox = font.getbbox(label_top)
            draw.text((cx - (bbox[2]-bbox[0])/2, y_off + font.size), label_top, font=font, fill=(70, 50, 10))

def draw_event(draw, center, text, font, event_type='start'):
    cx, cy = center
    r = 16
    if event_type == 'start':
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(230, 255, 230), outline=(40, 160, 40), width=2)
    elif event_type == 'end':
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(255, 230, 230), outline=(180, 40, 40), width=3)
    elif event_type == 'timer':
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(255, 255, 230), outline=(180, 140, 30), width=2)
        draw.ellipse([(cx - r + 3, cy - r + 3), (cx + r - 3, cy + r - 3)], outline=(180, 140, 30), width=1)
    
    words = text.split()
    lines = []
    cur = []
    for w in words:
        if len(' '.join(cur + [w])) <= 13: cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur = [w]
    if cur: lines.append(' '.join(cur))
    for i, l in enumerate(lines):
        bbox = font.getbbox(l)
        w = bbox[2] - bbox[0]
        draw.text((cx - w/2, cy + r + 3 + i*(font.size+2)), l, font=font, fill=(30, 30, 30))

def draw_condition_label(draw, pos, text, font, fill=(160, 40, 40)):
    draw.text(pos, text, font=font, fill=fill)

# ================= DIAGRAM 1: AS IS =================
def build_diagram_1():
    img = Image.new('RGB', (1280, 650), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_task = get_font(10)
    f_bold = get_font(10, bold=True)
    f_cond = get_font(9, bold=True)
    
    lanes = ["Посетитель (клиент)", "Оператор / Администратор зала", "Кассир / Ресепшен"]
    draw_pool_and_lanes(draw, "Боулинг-клуб (Традиционный процесс «Как есть» - AS IS)", lanes, 1280, 650)
    
    # Elements in Lane 1 (Client, y: 15..218, mid ~ 116)
    draw_event(draw, (130, 116), "Потребность в брони", f_task, 'start')
    draw_task(draw, (180, 88, 290, 144), "Позвонить в клуб по телефону", f_task)
    draw_task(draw, (640, 88, 750, 144), "Прибыть в клуб к дорожке", f_task)
    draw_task(draw, (980, 88, 1090, 144), "Отыграть сессию боулинга", f_task)
    
    # Elements in Lane 2 (Operator, y: 218..421, mid ~ 320)
    draw_task(draw, (180, 292, 290, 348), "Принять входящий телефонный звонок", f_task)
    draw_task(draw, (320, 292, 430, 348), "Проверить свободные дорожки в журнале", f_task)
    draw_gateway(draw, (470, 320), "Свободно?", f_bold)
    
    # Rejection branch
    draw_task(draw, (420, 230, 520, 275), "Сообщить об отсутствии мест", f_task, fill_color=(255, 240, 240), border_color=(200, 80, 80))
    draw_event(draw, (560, 252), "Отказ в бронировании", f_task, 'end')
    
    # Booking confirmed
    draw_task(draw, (530, 292, 640, 348), "Записать имя и телефон в журнал", f_task)
    draw_event(draw, (680, 320), "Ожидание дня визита", f_task, 'timer')
    draw_task(draw, (730, 292, 840, 348), "Уточнить число гостей в компании", f_task)
    draw_gateway(draw, (880, 320), "> 6 гостей?", f_bold)
    
    # Split branches for capacity
    draw_task(draw, (940, 235, 1060, 285), "Искать вторую свободную дорожку", f_task, fill_color=(255, 245, 230), border_color=(210, 130, 20))
    draw_task(draw, (940, 345, 1060, 395), "Включить одну дорожку в зале", f_task)
    
    # Elements in Lane 3 (Cashier, y: 421..625, mid ~ 523)
    draw_task(draw, (730, 495, 850, 551), "Рассчитать часы на стыке тарифов вручную", f_task, fill_color=(255, 240, 230), border_color=(210, 100, 30))
    draw_gateway(draw, (900, 523), "Спор по цене?", f_bold)
    draw_task(draw, (840, 565, 960, 615), "Урегулировать переплату с гостем", f_task, fill_color=(255, 235, 235), border_color=(190, 60, 60))
    draw_task(draw, (980, 495, 1090, 551), "Принять оплату и выбить чек", f_task)
    draw_task(draw, (1120, 88, 1230, 144), "Оплатить заказ на кассе", f_task)
    draw_event(draw, (1190, 523), "Сессия оплачена и закрыта", f_task, 'end')

    # Arrows Diagram 1
    draw_arrow(draw, [(146, 116), (180, 116)])
    draw_arrow(draw, [(235, 144), (235, 292)])
    draw_arrow(draw, [(290, 320), (320, 320)])
    draw_arrow(draw, [(430, 320), (451, 320)])
    
    # Gateway 1 branches
    draw_arrow(draw, [(470, 301), (470, 275)])
    draw_condition_label(draw, (475, 280), "Нет", f_cond)
    draw_arrow(draw, [(520, 252), (544, 252)])
    
    draw_arrow(draw, [(489, 320), (530, 320)])
    draw_condition_label(draw, (495, 305), "Да", f_cond)
    draw_arrow(draw, [(640, 320), (664, 320)])
    draw_arrow(draw, [(696, 320), (730, 320)])
    
    # Meeting at lane
    draw_arrow(draw, [(695, 144), (695, 200), (785, 200), (785, 292)])
    draw_arrow(draw, [(840, 320), (861, 320)])
    
    # Gateway 2 branches (>6 guests)
    draw_arrow(draw, [(880, 301), (880, 260), (940, 260)])
    draw_condition_label(draw, (885, 265), "> 6 чел.", f_cond)
    draw_arrow(draw, [(880, 339), (880, 370), (940, 370)])
    draw_condition_label(draw, (885, 350), "<= 6 чел.", f_cond)
    
    draw_arrow(draw, [(1060, 260), (1075, 260), (1075, 144)])
    draw_arrow(draw, [(1060, 370), (1075, 370), (1075, 144)])
    
    # Play session
    draw_arrow(draw, [(1035, 144), (1035, 460), (790, 460), (790, 495)])
    draw_arrow(draw, [(850, 523), (881, 523)])
    
    # Gateway 3 branches (Dispute)
    draw_arrow(draw, [(900, 542), (900, 565)])
    draw_condition_label(draw, (905, 545), "Да", f_cond)
    draw_arrow(draw, [(960, 590), (1035, 590), (1035, 551)])
    
    draw_arrow(draw, [(919, 523), (980, 523)])
    draw_condition_label(draw, (935, 508), "Нет", f_cond)
    
    draw_arrow(draw, [(1035, 495), (1035, 200), (1175, 200), (1175, 144)])
    draw_arrow(draw, [(1175, 144), (1175, 507)])

    img.save("diagram_1_as_is.png")
    print("Saved diagram_1_as_is.png")

# ================= DIAGRAM 2: TO BE =================
def build_diagram_2():
    img = Image.new('RGB', (1280, 650), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_task = get_font(10)
    f_bold = get_font(10, bold=True)
    f_cond = get_font(9, bold=True)
    
    lanes = ["Посетитель (пользователь сайта)", "Серверная часть сайта (Django)", "Оператор игрового зала"]
    draw_pool_and_lanes(draw, "Информационная веб-система боулинга и бильярда («Как будет» - TO BE)", lanes, 1280, 650)
    
    # Lane 1 (Client, y: 15..218, mid ~ 116)
    draw_event(draw, (120, 116), "Потребность в брони", f_task, 'start')
    draw_task(draw, (170, 88, 280, 144), "Выбрать дату, время и тип игры на сайте", f_task)
    draw_task(draw, (320, 88, 430, 144), "Указать количество гостей в форме брони", f_task)
    draw_task(draw, (580, 45, 700, 100), "Выбрать две смежные дорожки на схеме", f_task, fill_color=(255, 245, 230), border_color=(220, 130, 20))
    draw_task(draw, (580, 125, 700, 180), "Выбрать одну дорожку на схеме", f_task)
    draw_task(draw, (890, 88, 1010, 144), "Подтвердить бронь и получить талон", f_task)
    draw_task(draw, (1040, 88, 1150, 144), "Отыграть сессию боулинга", f_task)
    
    # Lane 2 (Django Server, y: 218..421, mid ~ 320)
    draw_task(draw, (170, 292, 280, 348), "Проверить слоты в БД через Fetch API (JSON)", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_gateway(draw, (470, 320), "> 6 гостей?", f_bold)
    draw_task(draw, (440, 235, 560, 285), "Заблокировать 1 дорожку, потребовать две", f_task, fill_color=(255, 240, 240), border_color=(210, 70, 70))
    draw_task(draw, (730, 292, 850, 348), "Автоматически рассчитать стык тарифов", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (890, 292, 1010, 348), "Зафиксировать бронь (transaction.atomic)", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (1040, 292, 1150, 348), "Сформировать талон и отправить email", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    
    # Lane 3 (Operator, y: 421..625, mid ~ 523)
    draw_event(draw, (800, 523), "Наступление времени сессии", f_task, 'timer')
    draw_task(draw, (860, 495, 980, 551), "Отметить визит гостей в панели оператора", f_task)
    draw_event(draw, (1200, 523), "Бронирование успешно закрыто", f_task, 'end')

    # Arrows Diagram 2
    draw_arrow(draw, [(136, 116), (170, 116)])
    draw_arrow(draw, [(225, 144), (225, 292)])
    draw_arrow(draw, [(280, 320), (375, 320), (375, 144)])
    draw_arrow(draw, [(430, 116), (470, 116), (470, 301)])
    
    # Gateway branches
    draw_arrow(draw, [(470, 301), (470, 260), (440, 260)])
    draw_condition_label(draw, (400, 245), "Да (>6)", f_cond)
    draw_arrow(draw, [(500, 235), (500, 72), (580, 72)])
    
    draw_arrow(draw, [(489, 320), (540, 320), (540, 152), (580, 152)])
    draw_condition_label(draw, (495, 325), "Нет (<=6)", f_cond)
    
    draw_arrow(draw, [(700, 72), (715, 72), (715, 320), (730, 320)])
    draw_arrow(draw, [(700, 152), (715, 152), (715, 320), (730, 320)])
    
    draw_arrow(draw, [(850, 320), (890, 320)])
    draw_arrow(draw, [(950, 292), (950, 144)])
    draw_arrow(draw, [(950, 144), (950, 220), (1095, 220), (1095, 292)])
    
    draw_arrow(draw, [(1095, 292), (1095, 144)])
    draw_arrow(draw, [(1040, 116), (1000, 116)]) # visual connect
    
    # Timer & Visit
    draw_arrow(draw, [(816, 523), (860, 523)])
    draw_arrow(draw, [(980, 523), (1095, 523), (1095, 144)])
    draw_arrow(draw, [(1095, 144), (1095, 450), (1200, 450), (1200, 507)])

    img.save("diagram_2_to_be.png")
    print("Saved diagram_2_to_be.png")

# ================= DIAGRAM 3: BAR PREORDER =================
def build_diagram_3():
    img = Image.new('RGB', (1280, 650), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_task = get_font(10)
    f_bold = get_font(10, bold=True)
    f_cond = get_font(9, bold=True)
    
    lanes = ["Посетитель", "Серверная часть сайта (Django)", "Бармен / Повар кухни"]
    draw_pool_and_lanes(draw, "Процесс предзаказа блюд и напитков бара к дорожке", lanes, 1280, 650)
    
    # Lane 1 (Client)
    draw_event(draw, (120, 116), "Оформление брони", f_task, 'start')
    draw_task(draw, (170, 88, 280, 144), "Открыть онлайн-каталог бара", f_task)
    draw_task(draw, (310, 88, 420, 144), "Выбрать позиции закусок и напитков", f_task)
    draw_task(draw, (550, 50, 670, 105), "Скорректировать позиции в заказе", f_task, fill_color=(255, 245, 230), border_color=(220, 130, 20))
    draw_task(draw, (730, 88, 850, 144), "Подтвердить состав предзаказа", f_task)
    draw_task(draw, (1110, 88, 1220, 144), "Получить блюда на столик дорожки", f_task)
    
    # Lane 2 (Django Server)
    draw_task(draw, (310, 292, 430, 348), "Проверить доступность позиций на складе", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_gateway(draw, (480, 320), "Все в наличии?", f_bold)
    draw_task(draw, (430, 235, 540, 285), "Предупредить о нехватке блюда", f_task, fill_color=(255, 240, 240), border_color=(210, 70, 70))
    draw_task(draw, (560, 292, 680, 348), "Рассчитать сумму предзаказа", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (730, 292, 850, 348), "Сохранить позиции (PreOrderItem) в БД", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (890, 292, 1010, 348), "Сформировать чек-лист с таймером подачи", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    
    # Lane 3 (Kitchen / Bar)
    draw_event(draw, (850, 523), "За 15 мин до старта игры", f_task, 'timer')
    draw_task(draw, (910, 495, 1030, 551), "Приготовить блюда и разлить напитки", f_task)
    draw_task(draw, (1060, 495, 1180, 551), "Подать предзаказ к игровой дорожке", f_task)
    draw_event(draw, (1230, 523), "Предзаказ выдан клиентам", f_task, 'end')

    # Arrows Diagram 3
    draw_arrow(draw, [(136, 116), (170, 116)])
    draw_arrow(draw, [(280, 116), (310, 116)])
    draw_arrow(draw, [(365, 144), (365, 292)])
    draw_arrow(draw, [(430, 320), (461, 320)])
    
    # Gateway branches
    draw_arrow(draw, [(480, 301), (480, 285)])
    draw_condition_label(draw, (485, 288), "Нет", f_cond)
    draw_arrow(draw, [(485, 235), (485, 78), (550, 78)])
    draw_arrow(draw, [(610, 105), (610, 144), (365, 144)])
    
    draw_arrow(draw, [(499, 320), (560, 320)])
    draw_condition_label(draw, (515, 305), "Да", f_cond)
    
    draw_arrow(draw, [(620, 292), (620, 116), (730, 116)])
    draw_arrow(draw, [(790, 144), (790, 292)])
    draw_arrow(draw, [(850, 320), (890, 320)])
    
    draw_arrow(draw, [(950, 348), (950, 440), (850, 440), (850, 507)])
    draw_arrow(draw, [(866, 523), (910, 523)])
    draw_arrow(draw, [(1030, 523), (1060, 523)])
    draw_arrow(draw, [(1120, 495), (1120, 200), (1165, 200), (1165, 144)])
    draw_arrow(draw, [(1180, 523), (1214, 523)])

    img.save("diagram_3_bar_preorder.png")
    print("Saved diagram_3_bar_preorder.png")

# ================= DIAGRAM 4: CLUB CARD =================
def build_diagram_4():
    img = Image.new('RGB', (1280, 650), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    f_task = get_font(10)
    f_bold = get_font(10, bold=True)
    f_cond = get_font(9, bold=True)
    
    lanes = ["Посетитель", "Серверная часть сайта (Django)", "Администратор клуба"]
    draw_pool_and_lanes(draw, "Процесс применения клубной карты и расчета скидки", lanes, 1280, 650)
    
    # Lane 1 (Client)
    draw_event(draw, (120, 116), "Старт оформления", f_task, 'start')
    draw_task(draw, (170, 88, 280, 144), "Ввести номер клубной карты в кабинете", f_task)
    draw_task(draw, (590, 88, 700, 144), "Ознакомиться с рассчитанной скидкой", f_task)
    draw_task(draw, (1100, 88, 1210, 144), "Получить уведомление о бонусах", f_task)
    
    # Lane 2 (Django Server)
    draw_task(draw, (170, 292, 280, 348), "Проверить номер и статус карты в БД", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_gateway(draw, (330, 320), "Карта активна?", f_bold)
    draw_task(draw, (330, 235, 450, 285), "Вывести ошибку валидации карты", f_task, fill_color=(255, 240, 240), border_color=(210, 70, 70))
    draw_task(draw, (440, 292, 560, 348), "Определить % скидки (5/10/15%)", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (590, 292, 710, 348), "Вычесть скидку из базовой цены брони", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (820, 292, 940, 348), "Обновить сумму накоплений в БД", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_gateway(draw, (990, 320), "Новый статус?", f_bold)
    draw_task(draw, (1050, 250, 1160, 305), "Повысить категорию клубной карты", f_task, fill_color=(230, 250, 240), border_color=(30, 140, 80))
    draw_task(draw, (1050, 335, 1160, 390), "Сохранить текущую категорию карты", f_task)
    
    # Lane 3 (Administrator)
    draw_task(draw, (330, 495, 450, 551), "Проверить выдачу карты в реестре", f_task)
    draw_event(draw, (770, 320), "Оплата бронирования", f_task, 'timer')
    draw_event(draw, (1220, 320), "Баланс карты успешно обновлен", f_task, 'end')

    # Arrows Diagram 4
    draw_arrow(draw, [(136, 116), (170, 116)])
    draw_arrow(draw, [(225, 144), (225, 292)])
    draw_arrow(draw, [(280, 320), (311, 320)])
    
    # Gateway 1
    draw_arrow(draw, [(330, 301), (330, 285)])
    draw_condition_label(draw, (335, 288), "Нет", f_cond)
    draw_arrow(draw, [(390, 285), (390, 495)])
    draw_arrow(draw, [(390, 495), (390, 370), (225, 370), (225, 348)])
    
    draw_arrow(draw, [(349, 320), (440, 320)])
    draw_condition_label(draw, (375, 305), "Да", f_cond)
    
    draw_arrow(draw, [(560, 320), (590, 320)])
    draw_arrow(draw, [(650, 292), (650, 144)])
    draw_arrow(draw, [(650, 144), (650, 220), (770, 220), (770, 304)])
    draw_arrow(draw, [(786, 320), (820, 320)])
    draw_arrow(draw, [(940, 320), (971, 320)])
    
    # Gateway 2 (Level up)
    draw_arrow(draw, [(990, 301), (990, 278), (1050, 278)])
    draw_condition_label(draw, (995, 265), "Да", f_cond)
    draw_arrow(draw, [(990, 339), (990, 362), (1050, 362)])
    draw_condition_label(draw, (995, 350), "Нет", f_cond)
    
    draw_arrow(draw, [(1105, 250), (1105, 144)])
    draw_arrow(draw, [(1160, 278), (1220, 278), (1220, 304)])
    draw_arrow(draw, [(1160, 362), (1220, 362), (1220, 336)])

    img.save("diagram_4_club_card.png")
    print("Saved diagram_4_club_card.png")

if __name__ == '__main__':
    build_diagram_1()
    build_diagram_2()
    build_diagram_3()
    build_diagram_4()
    print("All 4 BPMN diagrams generated successfully!")
