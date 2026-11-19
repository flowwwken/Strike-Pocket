"""
Генератор полного набора из 6 векторных фреймов Figma (SVG) для проекта Strike & Pocket
Каждый фрейм оформлен в стандартном формате 1440x960 px и готов к Drag-and-Drop импорту в Figma.
"""

import os

out_dir = os.path.join("06_День_6_Проектирование_интерфейса", "figma_svg_frames")
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# 01. UI-Kit & Design System (уже частично есть, сохраним полный)
# -------------------------------------------------------------
svg_01 = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#0A0E17"/>
  <text x="60" y="60" fill="#00E5FF" font-family="Montserrat, Inter, sans-serif" font-size="28" font-weight="800" letter-spacing="1">STRIKE &amp; POCKET — ДИЗАЙН-СИСТЕМА И UI-KIT</text>
  <text x="60" y="85" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="14">Тема Dark Neon Lounge • Базовый модуль 8-pt Grid • Гарнитуры Montserrat / Inter</text>
  <line x1="60" y1="105" x2="1380" y2="105" stroke="#374151" stroke-width="1"/>

  <g transform="translate(60, 130)">
    <rect width="400" height="780" rx="12" fill="#111827" stroke="#00E5FF" stroke-opacity="0.3"/>
    <text x="24" y="36" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">1. ЦВЕТОВАЯ ПАЛИТРА</text>
    <line x1="24" y1="48" x2="376" y2="48" stroke="#374151" stroke-width="1"/>
    <g transform="translate(24, 65)">
      <rect y="0" width="352" height="48" rx="8" fill="#00E5FF"/>
      <text x="16" y="30" fill="#050B14" font-family="Inter, sans-serif" font-size="13" font-weight="700">Primary Cyan</text>
      <text x="270" y="30" fill="#050B14" font-family="monospace" font-size="12">#00E5FF</text>

      <rect y="56" width="352" height="48" rx="8" fill="#FFB300"/>
      <text x="16" y="86" fill="#050B14" font-family="Inter, sans-serif" font-size="13" font-weight="700">Secondary Amber</text>
      <text x="270" y="86" fill="#050B14" font-family="monospace" font-size="12">#FFB300</text>

      <rect y="112" width="352" height="48" rx="8" fill="#10B981"/>
      <text x="16" y="142" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700">Success Green</text>
      <text x="270" y="142" fill="#FFFFFF" font-family="monospace" font-size="12">#10B981</text>

      <rect y="168" width="352" height="48" rx="8" fill="#EF4444"/>
      <text x="16" y="198" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700">Danger / Error</text>
      <text x="270" y="198" fill="#FFFFFF" font-family="monospace" font-size="12">#EF4444</text>

      <rect y="224" width="352" height="48" rx="8" fill="#A855F7"/>
      <text x="16" y="254" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700">VIP Purple (Snooker)</text>
      <text x="270" y="254" fill="#FFFFFF" font-family="monospace" font-size="12">#A855F7</text>

      <rect y="280" width="352" height="48" rx="8" fill="#111827" stroke="#374151"/>
      <text x="16" y="310" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="13" font-weight="700">Surface Card</text>
      <text x="270" y="310" fill="#CBD5E1" font-family="monospace" font-size="12">#111827</text>

      <rect y="336" width="352" height="48" rx="8" fill="#0A0E17" stroke="#374151"/>
      <text x="16" y="366" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="13" font-weight="700">Background Dark</text>
      <text x="270" y="366" fill="#CBD5E1" font-family="monospace" font-size="12">#0A0E17</text>

      <rect y="392" width="352" height="48" rx="8" fill="#CBD5E1"/>
      <text x="16" y="422" fill="#0F172A" font-family="Inter, sans-serif" font-size="13" font-weight="700">Text Muted (Hi-Contrast)</text>
      <text x="270" y="422" fill="#0F172A" font-family="monospace" font-size="12">#CBD5E1</text>
    </g>
  </g>

  <g transform="translate(500, 130)">
    <rect width="440" height="780" rx="12" fill="#111827" stroke="#00E5FF" stroke-opacity="0.3"/>
    <text x="24" y="36" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">2. ТИПОГРАФИКА И СЕТКА</text>
    <line x1="24" y1="48" x2="416" y2="48" stroke="#374151" stroke-width="1"/>
    <g transform="translate(24, 70)">
      <text y="0" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">H1 MONTSERRAT BOLD (36px / 44px)</text>
      <text y="32" fill="#FFFFFF" font-size="28" font-family="Montserrat, sans-serif" font-weight="700">STRIKE &amp; POCKET</text>

      <text y="80" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">H2 MONTSERRAT SEMIBOLD (28px / 36px)</text>
      <text y="108" fill="#FFFFFF" font-size="22" font-family="Montserrat, sans-serif" font-weight="600">Бронирование дорожек</text>

      <text y="150" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">H3 MONTSERRAT MEDIUM (22px / 28px)</text>
      <text y="176" fill="#FFFFFF" font-size="18" font-family="Montserrat, sans-serif" font-weight="500">Русская пирамида 12ft</text>

      <text y="220" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">BODY INTER REGULAR (15px / 22px)</text>
      <text y="244" fill="#CBD5E1" font-size="14" font-family="Inter, sans-serif">Тарифы день/вечер со сменой ставки в 18:00 и скидками по картам.</text>

      <line x1="0" y1="280" x2="390" y2="280" stroke="#374151" stroke-dasharray="4 4"/>
      <text y="310" fill="#00E5FF" font-size="14" font-family="Montserrat, sans-serif" font-weight="700">8-POINT GRID SYSTEM</text>
      <text y="335" fill="#CBD5E1" font-size="13" font-family="Inter, sans-serif">Базовый шаг: 8 px (микромодуль 4 px)</text>
      <text y="360" fill="#CBD5E1" font-size="13" font-family="Inter, sans-serif">Отступы: 4, 8, 16, 24, 32, 48, 64 px</text>
      <text y="385" fill="#38BDF8" font-size="13" font-family="Inter, sans-serif">Desktop 1440: 12 колонок (контейнер 1280 px)</text>
      <text y="410" fill="#38BDF8" font-size="13" font-family="Inter, sans-serif">Mobile 375: 4 колонки (контейнер 343 px)</text>
    </g>
  </g>

  <g transform="translate(980, 130)">
    <rect width="400" height="780" rx="12" fill="#111827" stroke="#00E5FF" stroke-opacity="0.3"/>
    <text x="24" y="36" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">3. КОМПОНЕНТЫ (5 СОСТОЯНИЙ)</text>
    <line x1="24" y1="48" x2="376" y2="48" stroke="#374151" stroke-width="1"/>
    <g transform="translate(24, 65)">
      <text y="15" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">КНОПКА PRIMARY (CYAN):</text>
      <rect y="25" width="165" height="38" rx="8" fill="#00E5FF"/>
      <text x="22" y="49" fill="#050B14" font-size="13" font-weight="700" font-family="Inter, sans-serif">Default</text>

      <rect x="180" y="25" width="165" height="38" rx="8" fill="#33EBFF"/>
      <text x="202" y="49" fill="#000000" font-size="13" font-weight="700" font-family="Inter, sans-serif">Hover</text>

      <rect y="72" width="165" height="38" rx="8" fill="#00B4D8"/>
      <text x="22" y="96" fill="#000000" font-size="13" font-weight="700" font-family="Inter, sans-serif">Pressed</text>

      <rect x="180" y="72" width="165" height="38" rx="8" fill="#374151"/>
      <text x="202" y="96" fill="#9CA3AF" font-size="13" font-weight="700" font-family="Inter, sans-serif">Disabled</text>

      <text y="140" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">ПОЛЯ ВВОДА (INPUT STATES):</text>
      <rect y="150" width="345" height="38" rx="6" fill="#0A0E17" stroke="#374151"/>
      <text x="12" y="174" fill="#CBD5E1" font-size="12" font-family="Inter, sans-serif">+7 (927) 800-00-00 [Default]</text>

      <rect y="196" width="345" height="38" rx="6" fill="#0A0E17" stroke="#00E5FF" stroke-width="1.8"/>
      <text x="12" y="220" fill="#FFFFFF" font-size="12" font-family="Inter, sans-serif">2026-11-20 [Focused]</text>

      <rect y="242" width="345" height="38" rx="6" fill="#261014" stroke="#EF4444" stroke-width="1.8"/>
      <text x="12" y="266" fill="#FFFFFF" font-size="12" font-family="Inter, sans-serif">+7 (927) [Error]</text>
      <text x="4" y="295" fill="#EF4444" font-size="10" font-family="Inter, sans-serif">&times; Введите телефон в формате +7 (900) 000-00-00</text>

      <text y="325" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">СТАТУСНЫЕ АЛЕРТЫ:</text>
      <rect y="335" width="345" height="36" rx="6" fill="#10B981" fill-opacity="0.2" stroke="#10B981"/>
      <text x="12" y="358" fill="#34D399" font-size="12" font-family="Inter, sans-serif">&check; Бронирование успешно подтверждено</text>

      <rect y="380" width="345" height="36" rx="6" fill="#F59E0B" fill-opacity="0.2" stroke="#F59E0B"/>
      <text x="12" y="403" fill="#FBBF24" font-size="12" font-family="Inter, sans-serif">! Внимание: лимит 6 игроков на дорожку</text>
    </g>
  </g>
</svg>"""

with open(os.path.join(out_dir, "01_UI_Kit_Design_System.svg"), "w", encoding="utf-8") as f:
    f.write(svg_01)

# -------------------------------------------------------------
# 02. Site Map Architecture (1440x960)
# -------------------------------------------------------------
svg_02 = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#0A0E17"/>
  <text x="60" y="60" fill="#00E5FF" font-family="Montserrat, Inter, sans-serif" font-size="28" font-weight="800" letter-spacing="1">СТРУКТУРНАЯ СХЕМА САЙТА (SITE MAP &amp; НАВИГАЦИЯ)</text>
  <text x="60" y="85" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="14">Иерархическая структура разделов, маршруты URL и матрица ролевого доступа RBAC</text>
  <line x1="60" y1="105" x2="1380" y2="105" stroke="#374151" stroke-width="1"/>

  <!-- Level 0: Корневой узел -->
  <g transform="translate(560, 130)">
    <rect width="320" height="60" rx="10" fill="#1E293B" stroke="#00E5FF" stroke-width="2"/>
    <text x="160" y="28" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="15" font-weight="700" text-anchor="middle">Главная страница [L0]</text>
    <text x="160" y="48" fill="#94A3B8" font-family="monospace" font-size="11" text-anchor="middle">URL: / (Гость, Посетитель)</text>
  </g>

  <!-- Линии от L0 к L1 -->
  <line x1="720" y1="190" x2="720" y2="230" stroke="#00E5FF" stroke-width="2"/>
  <line x1="200" y1="230" x2="1240" y2="230" stroke="#00E5FF" stroke-width="2"/>
  <line x1="200" y1="230" x2="200" y2="260" stroke="#00E5FF" stroke-width="2"/>
  <line x1="460" y1="230" x2="460" y2="260" stroke="#00E5FF" stroke-width="2"/>
  <line x1="720" y1="230" x2="720" y2="260" stroke="#00E5FF" stroke-width="2"/>
  <line x1="980" y1="230" x2="980" y2="260" stroke="#00E5FF" stroke-width="2"/>
  <line x1="1240" y1="230" x2="1240" y2="260" stroke="#00E5FF" stroke-width="2"/>

  <!-- Level 1: Основные разделы -->
  <!-- 1.1 Залы и дорожки -->
  <g transform="translate(80, 260)">
    <rect width="240" height="70" rx="8" fill="#111827" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="120" y="28" fill="#38BDF8" font-family="Montserrat, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Каталог зон и дорожек</text>
    <text x="120" y="46" fill="#94A3B8" font-family="monospace" font-size="10" text-anchor="middle">/zones/ (Боулинг/Бильярд)</text>
    <text x="120" y="60" fill="#10B981" font-family="Inter, sans-serif" font-size="10" text-anchor="middle">Доступ: Всем</text>
  </g>

  <!-- 1.2 Интерактивная карта -->
  <g transform="translate(340, 260)">
    <rect width="240" height="70" rx="8" fill="#111827" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="120" y="28" fill="#38BDF8" font-family="Montserrat, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Интерактивная карта</text>
    <text x="120" y="46" fill="#94A3B8" font-family="monospace" font-size="10" text-anchor="middle">/map/ (SVG схема зала)</text>
    <text x="120" y="60" fill="#10B981" font-family="Inter, sans-serif" font-size="10" text-anchor="middle">Доступ: Всем</text>
  </g>

  <!-- 1.3 Визард бронирования -->
  <g transform="translate(600, 260)">
    <rect width="240" height="70" rx="8" fill="#111827" stroke="#00E5FF" stroke-width="2"/>
    <text x="120" y="28" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Онлайн-бронирование</text>
    <text x="120" y="46" fill="#94A3B8" font-family="monospace" font-size="10" text-anchor="middle">/booking/wizard/ (Шаги 1-4)</text>
    <text x="120" y="60" fill="#10B981" font-family="Inter, sans-serif" font-size="10" text-anchor="middle">Доступ: Гость/Клиент</text>
  </g>

  <!-- 1.4 Меню бара & Клуб -->
  <g transform="translate(860, 260)">
    <rect width="240" height="70" rx="8" fill="#111827" stroke="#38BDF8" stroke-width="1.5"/>
    <text x="120" y="28" fill="#38BDF8" font-family="Montserrat, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Меню бара &amp; Клуб</text>
    <text x="120" y="46" fill="#94A3B8" font-family="monospace" font-size="10" text-anchor="middle">/bar/ &amp; /loyalty/</text>
    <text x="120" y="60" fill="#10B981" font-family="Inter, sans-serif" font-size="10" text-anchor="middle">Доступ: Всем</text>
  </g>

  <!-- 1.5 ЛК / Проверка брони -->
  <g transform="translate(1120, 260)">
    <rect width="240" height="70" rx="8" fill="#111827" stroke="#F59E0B" stroke-width="1.5"/>
    <text x="120" y="28" fill="#F59E0B" font-family="Montserrat, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Проверка брони / ЛК</text>
    <text x="120" y="46" fill="#94A3B8" font-family="monospace" font-size="10" text-anchor="middle">/check-booking/ &amp; /profile/</text>
    <text x="120" y="60" fill="#38BDF8" font-family="Inter, sans-serif" font-size="10" text-anchor="middle">По номеру брони / PIN</text>
  </g>

  <!-- Level 2: Подразделы визарда (Шаги 1-4) -->
  <line x1="720" y1="330" x2="720" y2="400" stroke="#00E5FF" stroke-width="2"/>
  <line x1="430" y1="400" x2="1010" y2="400" stroke="#00E5FF" stroke-width="1.5"/>

  <g transform="translate(340, 420)">
    <rect width="180" height="56" rx="6" fill="#0A0E17" stroke="#374151"/>
    <text x="90" y="24" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="600" text-anchor="middle">Шаг 1: Выбор зоны</text>
    <text x="90" y="42" fill="#94A3B8" font-size="10" text-anchor="middle">Дата, время, гости</text>
  </g>

  <g transform="translate(530, 420)">
    <rect width="180" height="56" rx="6" fill="#0A0E17" stroke="#374151"/>
    <text x="90" y="24" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="600" text-anchor="middle">Шаг 2: Выбор дорожки</text>
    <text x="90" y="42" fill="#00E5FF" font-size="10" text-anchor="middle">Слот на схеме зала</text>
  </g>

  <g transform="translate(720, 420)">
    <rect width="180" height="56" rx="6" fill="#0A0E17" stroke="#374151"/>
    <text x="90" y="24" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="600" text-anchor="middle">Шаг 3: Предзаказ бара</text>
    <text x="90" y="42" fill="#94A3B8" font-size="10" text-anchor="middle">Закуски, пицца, напитки</text>
  </g>

  <g transform="translate(910, 420)">
    <rect width="180" height="56" rx="6" fill="#0A0E17" stroke="#374151"/>
    <text x="90" y="24" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="11" font-weight="600" text-anchor="middle">Шаг 4: Расчет &amp; Оплата</text>
    <text x="90" y="42" fill="#10B981" font-size="10" text-anchor="middle">Тариф 18:00 + Скидка</text>
  </g>

  <!-- Level 3: Служебный блок (АРМ Оператора, Бармена, Админа) -->
  <rect x="60" y="530" width="1320" height="380" rx="12" fill="#111827" stroke="#A855F7" stroke-width="1.5"/>
  <text x="84" y="565" fill="#A855F7" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">СЛУЖЕБНЫЙ РАЗДЕЛ: АРМ СОТРУДНИКОВ КЛУБА (RBAC ЗАЩИТА)</text>
  <text x="84" y="585" fill="#94A3B8" font-family="Inter, sans-serif" font-size="12">Доступ строго по учетным записям персонала (/arm/login/)</text>

  <!-- 3.1 АРМ Оператора -->
  <g transform="translate(84, 610)">
    <rect width="380" height="260" rx="8" fill="#0A0E17" stroke="#374151"/>
    <text x="20" y="32" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="14" font-weight="700">АРМ Оператора зала</text>
    <text x="20" y="52" fill="#CBD5E1" font-family="monospace" font-size="11">/arm/operator/grid/</text>
    <line x1="20" y1="65" x2="360" y2="65" stroke="#374151"/>
    <text x="20" y="90" fill="#CBD5E1" font-size="12">• Тайм-сетка дорожек 1-12 и столов 1-10</text>
    <text x="20" y="115" fill="#CBD5E1" font-size="12">• Ручная посадка гостей от стойки</text>
    <text x="20" y="140" fill="#CBD5E1" font-size="12">• Продление игры на лету (+30 / +60 мин)</text>
    <text x="20" y="165" fill="#EF4444" font-size="12">• Фиксация No-Show (неявка >15 мин)</text>
    <text x="20" y="190" fill="#10B981" font-size="12">• Прием оплаты наличными / картой</text>
    <text x="20" y="215" fill="#38BDF8" font-size="12">• Фискализация чека по 54-ФЗ</text>
  </g>

  <!-- 3.2 АРМ Менеджера бара -->
  <g transform="translate(494, 610)">
    <rect width="380" height="260" rx="8" fill="#0A0E17" stroke="#374151"/>
    <text x="20" y="32" fill="#FFB300" font-family="Montserrat, sans-serif" font-size="14" font-weight="700">АРМ Менеджера бара</text>
    <text x="20" y="52" fill="#CBD5E1" font-family="monospace" font-size="11">/arm/bar/orders/</text>
    <line x1="20" y1="65" x2="360" y2="65" stroke="#374151"/>
    <text x="20" y="90" fill="#CBD5E1" font-size="12">• Очередь предзаказов к дорожкам</text>
    <text x="20" y="115" fill="#CBD5E1" font-size="12">• Статусы: Принят → Готовится → Подан</text>
    <text x="20" y="140" fill="#CBD5E1" font-size="12">• Управление стоп-листом кухни и бара</text>
    <text x="20" y="165" fill="#CBD5E1" font-size="12">• Дозаказ напитков во время игры</text>
    <text x="20" y="190" fill="#10B981" font-size="12">• Привязка к общему счету брони</text>
  </g>

  <!-- 3.3 Административная панель -->
  <g transform="translate(904, 610)">
    <rect width="450" height="260" rx="8" fill="#0A0E17" stroke="#374151"/>
    <text x="20" y="32" fill="#A855F7" font-family="Montserrat, sans-serif" font-size="14" font-weight="700">Панель Управляющего (Admin)</text>
    <text x="20" y="52" fill="#CBD5E1" font-family="monospace" font-size="11">/admin/ (Управляющий, Бухгалтер)</text>
    <line x1="20" y1="65" x2="430" y2="65" stroke="#374151"/>
    <text x="20" y="90" fill="#CBD5E1" font-size="12">• Управление тарифами (день: 1200₽, вечер: 1800₽)</text>
    <text x="20" y="115" fill="#CBD5E1" font-size="12">• База клубных карт (Silver 5%, Gold 10%, Platinum 15%)</text>
    <text x="20" y="140" fill="#CBD5E1" font-size="12">• Аналитические отчеты выручки и загрузки</text>
    <text x="20" y="165" fill="#CBD5E1" font-size="12">• Учет рабочего времени операторов и барменов</text>
    <text x="20" y="190" fill="#10B981" font-size="12">• Экспорт данных в 1С и налоговую отчетность</text>
  </g>
</svg>"""

with open(os.path.join(out_dir, "02_Site_Map_Architecture.svg"), "w", encoding="utf-8") as f:
    f.write(svg_02)

# -------------------------------------------------------------
# 03. User Flows 3 Scenarios (1440x960)
# -------------------------------------------------------------
svg_03 = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#0A0E17"/>
  <text x="60" y="60" fill="#00E5FF" font-family="Montserrat, Inter, sans-serif" font-size="28" font-weight="800" letter-spacing="1">ПОЛЬЗОВАТЕЛЬСКИЕ СЦЕНАРИИ (USER FLOWS &amp; ВЕТВЛЕНИЯ)</text>
  <text x="60" y="85" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="14">3 ключевых сценария: Бронирование со спецтребованиями, Отмена брони в ЛК, АРМ Оператора</text>
  <line x1="60" y1="105" x2="1380" y2="105" stroke="#374151" stroke-width="1"/>

  <!-- Сценарий 1: Онлайн-бронирование -->
  <g transform="translate(60, 125)">
    <rect width="1320" height="235" rx="10" fill="#111827" stroke="#00E5FF" stroke-opacity="0.3"/>
    <text x="20" y="28" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="15" font-weight="700">СЦЕНАРИЙ 1: БРОНИРОВАНИЕ ДОРОЖКИ КЛИЕНТОМ (ПРОВЕРКИ FR-05, ТАРИФ 18:00, БАР)</text>
    
    <!-- Шаги -->
    <g transform="translate(20, 50)">
      <rect width="130" height="60" rx="6" fill="#1E293B" stroke="#00E5FF"/>
      <text x="65" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Вход на сайт</text>
      <text x="65" y="44" fill="#00E5FF" font-size="10" text-anchor="middle">Выбор даты/времени</text>

      <line x1="130" y1="30" x2="160" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <rect x="160" width="140" height="60" rx="6" fill="#1E293B" stroke="#00E5FF"/>
      <text x="230" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Кол-во гостей</text>
      <text x="230" y="44" fill="#FBBF24" font-size="10" text-anchor="middle">Проверка &gt; 6 чел?</text>

      <line x1="300" y1="30" x2="330" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <!-- Ветвление: > 6 гостей -->
      <rect x="330" width="160" height="60" rx="6" fill="#2E1065" stroke="#A855F7"/>
      <text x="410" y="24" fill="#E9D5FF" font-size="11" font-weight="600" text-anchor="middle">&gt; 6 игроков?</text>
      <text x="410" y="42" fill="#F472B6" font-size="10" text-anchor="middle">Требование 2-й дорожки</text>

      <line x1="490" y1="30" x2="520" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <!-- Расчет тарифа со сменой в 18:00 -->
      <rect x="520" width="170" height="60" rx="6" fill="#1E293B" stroke="#00E5FF"/>
      <text x="605" y="24" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Авторасчет тарифа</text>
      <text x="605" y="42" fill="#38BDF8" font-size="10" text-anchor="middle">Стык 18:00 (День+Вечер)</text>

      <line x1="690" y1="30" x2="720" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <!-- Предзаказ бара -->
      <rect x="720" width="150" height="60" rx="6" fill="#1E293B" stroke="#FFB300"/>
      <text x="795" y="24" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Предзаказ бара</text>
      <text x="795" y="42" fill="#FFB300" font-size="10" text-anchor="middle">Пицца, напитки (+0₽)</text>

      <line x1="870" y1="30" x2="900" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <!-- Клубная карта -->
      <rect x="900" width="150" height="60" rx="6" fill="#1E293B" stroke="#00E5FF"/>
      <text x="975" y="24" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Клубная карта</text>
      <text x="975" y="42" fill="#34D399" font-size="10" text-anchor="middle">Валидация скидки %</text>

      <line x1="1050" y1="30" x2="1080" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <!-- Оплата и SMS -->
      <rect x="1080" width="180" height="60" rx="6" fill="#064E3B" stroke="#10B981" stroke-width="2"/>
      <text x="1170" y="24" fill="#A7F3D0" font-size="11" font-weight="700" text-anchor="middle">Оплата СБП / Карта</text>
      <text x="1170" y="42" fill="#FFFFFF" font-size="10" text-anchor="middle">PIN-код брони в SMS/Email</text>
    </g>

    <!-- Подпись условий ошибки -->
    <text x="20" y="145" fill="#EF4444" font-size="11">Ветвление ошибки: Если дорожка уже занята другим клиентом &rarr; Модальное окно "Слот перехвачен", мгновенный откат без списания средств</text>
    <text x="20" y="165" fill="#38BDF8" font-size="11">Бизнес-правило 18:00: Сеанс 17:00–19:00 разбивается на 1ч по 1200₽ + 1ч по 1800₽ = 3000₽ (минус персональная скидка карты)</text>
  </g>

  <!-- Сценарий 2: Отмена бронирования -->
  <g transform="translate(60, 385)">
    <rect width="1320" height="235" rx="10" fill="#111827" stroke="#F59E0B" stroke-opacity="0.3"/>
    <text x="20" y="28" fill="#F59E0B" font-family="Montserrat, sans-serif" font-size="15" font-weight="700">СЦЕНАРИЙ 2: ПРОВЕРКА И ОТМЕНА БРОНИ В ЛИЧНОМ КАБИНЕТЕ (ПРАВИЛО 2 ЧАСОВ)</text>

    <g transform="translate(20, 50)">
      <rect width="180" height="60" rx="6" fill="#1E293B" stroke="#F59E0B"/>
      <text x="90" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Ввод № брони + PIN</text>
      <text x="90" y="44" fill="#CBD5E1" font-size="10" text-anchor="middle">Поиск брони в БД</text>

      <line x1="180" y1="30" x2="220" y2="30" stroke="#F59E0B" stroke-width="2"/>

      <rect x="220" width="200" height="60" rx="6" fill="#1E293B" stroke="#F59E0B"/>
      <text x="320" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Экран статуса брони</text>
      <text x="320" y="44" fill="#38BDF8" font-size="10" text-anchor="middle">Кнопка "Отменить бронь"</text>

      <line x1="420" y1="30" x2="460" y2="30" stroke="#F59E0B" stroke-width="2"/>

      <rect x="460" width="220" height="60" rx="6" fill="#1E293B" stroke="#F59E0B"/>
      <text x="570" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Проверка времени до игры</text>
      <text x="570" y="44" fill="#FBBF24" font-size="10" text-anchor="middle">Разница &gt; 2 часов?</text>

      <line x1="680" y1="30" x2="720" y2="30" stroke="#10B981" stroke-width="2"/>

      <!-- Успешная отмена -->
      <rect x="720" width="250" height="60" rx="6" fill="#064E3B" stroke="#10B981"/>
      <text x="845" y="24" fill="#A7F3D0" font-size="11" font-weight="700" text-anchor="middle">ДА (&gt; 2ч): Полный возврат</text>
      <text x="845" y="42" fill="#FFFFFF" font-size="10" text-anchor="middle">Статус: CANCELLED, автовозврат 100%</text>

      <!-- Отказ в отмене -->
      <g transform="translate(1000, 0)">
        <rect width="260" height="60" rx="6" fill="#7F1D1D" stroke="#EF4444"/>
        <text x="130" y="24" fill="#FECACA" font-size="11" font-weight="700" text-anchor="middle">НЕТ (&lt; 2ч): Запрет автоотмены</text>
        <text x="130" y="42" fill="#FFFFFF" font-size="10" text-anchor="middle">Алерт: Обратитесь к администратору</text>
      </g>
    </g>

    <text x="20" y="145" fill="#10B981" font-size="11">&check; При успешной отмене слот на интерактивной карте мгновенно освобождается для повторного бронирования.</text>
    <text x="20" y="165" fill="#EF4444" font-size="11">&times; Защита от спама и пустых простоев оборудования: при отказе менее чем за 2 часа предоплата не возвращается онлайн.</text>
  </g>

  <!-- Сценарий 3: АРМ Оператора -->
  <g transform="translate(60, 645)">
    <rect width="1320" height="235" rx="10" fill="#111827" stroke="#A855F7" stroke-opacity="0.3"/>
    <text x="20" y="28" fill="#A855F7" font-family="Montserrat, sans-serif" font-size="15" font-weight="700">СЦЕНАРИЙ 3: ОПЕРАТИВНОЕ УПРАВЛЕНИЕ ЗАЛОМ В АРМ ОПЕРАТОРА (NO-SHOW, 54-ФЗ)</text>

    <g transform="translate(20, 50)">
      <rect width="170" height="60" rx="6" fill="#1E293B" stroke="#A855F7"/>
      <text x="85" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Тайм-сетка АРМ</text>
      <text x="85" y="44" fill="#CBD5E1" font-size="10" text-anchor="middle">Мониторинг 22 дорожек</text>

      <line x1="170" y1="30" x2="210" y2="30" stroke="#A855F7" stroke-width="2"/>

      <rect x="210" width="190" height="60" rx="6" fill="#1E293B" stroke="#A855F7"/>
      <text x="305" y="26" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Прибытие гостей</text>
      <text x="305" y="44" fill="#FBBF24" font-size="10" text-anchor="middle">Опоздание &gt; 15 минут?</text>

      <line x1="400" y1="30" x2="440" y2="30" stroke="#A855F7" stroke-width="2"/>

      <!-- Опоздание / Явка -->
      <rect x="440" width="220" height="60" rx="6" fill="#1E293B" stroke="#00E5FF"/>
      <text x="550" y="24" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Явка: Чек-ин гостей</text>
      <text x="550" y="42" fill="#00E5FF" font-size="10" text-anchor="middle">Активация пинспоттера</text>

      <line x1="660" y1="30" x2="700" y2="30" stroke="#00E5FF" stroke-width="2"/>

      <!-- Дозаказ и продление -->
      <rect x="700" width="240" height="60" rx="6" fill="#1E293B" stroke="#FFB300"/>
      <text x="820" y="24" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Продление / Бар меню</text>
      <text x="820" y="42" fill="#FFB300" font-size="10" text-anchor="middle">Авторасчет доплаты</text>

      <line x1="940" y1="30" x2="980" y2="30" stroke="#10B981" stroke-width="2"/>

      <!-- Закрытие смены 54-ФЗ -->
      <rect x="980" width="280" height="60" rx="6" fill="#064E3B" stroke="#10B981"/>
      <text x="1120" y="24" fill="#A7F3D0" font-size="11" font-weight="700" text-anchor="middle">Окончательный расчет</text>
      <text x="1120" y="42" fill="#FFFFFF" font-size="10" text-anchor="middle">Печать чека ККТ по 54-ФЗ</text>
    </g>

    <text x="20" y="145" fill="#EF4444" font-size="11">&times; Ветка No-Show: Если гость не явился в течение 15 минут, система подсвечивает бронь красным и позволяет аннулировать слот.</text>
    <text x="20" y="165" fill="#38BDF8" font-size="11">&check; Интеграция с ККТ АТОЛ: автоматическая фискализация чека, раздельные товарные позиции на услуги боулинга и кухню бара.</text>
  </g>
</svg>"""

with open(os.path.join(out_dir, "03_User_Flows_3_Scenarios.svg"), "w", encoding="utf-8") as f:
    f.write(svg_03)

# -------------------------------------------------------------
# 04. Monochrome Wireframes (1440x960)
# -------------------------------------------------------------
svg_04 = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#F8FAFC"/>
  <text x="60" y="60" fill="#0F172A" font-family="Montserrat, Inter, sans-serif" font-size="28" font-weight="800" letter-spacing="1">МОНОХРОМНЫЕ ВАЙРФРЕЙМЫ (8 ЭКРАНОВ СИСТЕМЫ)</text>
  <text x="60" y="85" fill="#64748B" font-family="Inter, sans-serif" font-size="14">Скелетные схемы экранов без цветового шума: компоновка блоков, F-паттерн и иерархия</text>
  <line x1="60" y1="105" x2="1380" y2="105" stroke="#CBD5E1" stroke-width="1.5"/>

  <!-- Сетка 4x2 экранов -->
  <!-- Ряд 1: Экраны 1-4 -->
  <!-- 1. Главная -->
  <g transform="translate(60, 130)">
    <rect width="300" height="360" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="300" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">1. Главная (Desktop 1440)</text>
    <!-- Header -->
    <rect x="12" y="38" width="276" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Hero Banner -->
    <rect x="12" y="66" width="276" height="80" fill="#E2E8F0"/>
    <line x1="12" y1="66" x2="288" y2="146" stroke="#CBD5E1"/>
    <line x1="288" y1="66" x2="12" y2="146" stroke="#CBD5E1"/>
    <text x="150" y="110" fill="#475569" font-size="11" font-weight="600" text-anchor="middle">[Hero Заголовок &amp; CTA]</text>
    <!-- Виджет быстрого расчета -->
    <rect x="12" y="156" width="276" height="70" rx="4" fill="#F8FAFC" stroke="#94A3B8"/>
    <text x="24" y="176" fill="#1E293B" font-size="10" font-weight="600">Быстрый расчет сеанса</text>
    <rect x="24" y="186" width="115" height="16" fill="#E2E8F0"/>
    <rect x="149" y="186" width="115" height="16" fill="#E2E8F0"/>
    <rect x="24" y="206" width="240" height="14" fill="#0F172A"/>
    <!-- Карточки залов -->
    <rect x="12" y="236" width="85" height="110" fill="#F1F5F9" stroke="#CBD5E1"/>
    <rect x="107" y="236" width="85" height="110" fill="#F1F5F9" stroke="#CBD5E1"/>
    <rect x="202" y="236" width="86" height="110" fill="#F1F5F9" stroke="#CBD5E1"/>
  </g>

  <!-- 2. Каталог залов и тарифов -->
  <g transform="translate(390, 130)">
    <rect width="300" height="360" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="300" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">2. Каталог зон и тарифов</text>
    <rect x="12" y="38" width="276" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Табы фильтров -->
    <rect x="12" y="66" width="60" height="18" fill="#0F172A"/>
    <rect x="76" y="66" width="60" height="18" fill="#E2E8F0"/>
    <rect x="140" y="66" width="60" height="18" fill="#E2E8F0"/>
    <!-- Карточки тарифов -->
    <rect x="12" y="94" width="276" height="75" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="115" fill="#0F172A" font-size="11" font-weight="600">Боулинг Brunswick (12 дорожек)</text>
    <text x="24" y="132" fill="#64748B" font-size="9">Дневной: 1200 ₽/ч | Вечерний: 1800 ₽/ч</text>
    <rect x="24" y="142" width="100" height="18" fill="#334155"/>

    <rect x="12" y="178" width="276" height="75" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="199" fill="#0F172A" font-size="11" font-weight="600">Русская пирамида 12ft (6 столов)</text>
    <text x="24" y="216" fill="#64748B" font-size="9">Дневной: 700 ₽/ч | Вечерний: 1000 ₽/ч</text>
    <rect x="24" y="226" width="100" height="18" fill="#334155"/>

    <rect x="12" y="262" width="276" height="85" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="283" fill="#0F172A" font-size="11" font-weight="600">Пул 9ft &amp; Снукер VIP</text>
    <text x="24" y="300" fill="#64748B" font-size="9">От 600 до 1200 ₽/ч</text>
    <rect x="24" y="312" width="100" height="18" fill="#334155"/>
  </g>

  <!-- 3. Интерактивная карта залов -->
  <g transform="translate(720, 130)">
    <rect width="300" height="360" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="300" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">3. Интерактивная карта залов</text>
    <rect x="12" y="38" width="276" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Схема дорожек и столов -->
    <rect x="12" y="66" width="190" height="280" fill="#F8FAFC" stroke="#94A3B8"/>
    <!-- 12 дорожек -->
    <g transform="translate(20, 75)">
      <rect width="10" height="120" fill="#CBD5E1"/>
      <rect x="14" width="10" height="120" fill="#CBD5E1"/>
      <rect x="28" width="10" height="120" fill="#0F172A"/>
      <rect x="42" width="10" height="120" fill="#CBD5E1"/>
      <rect x="56" width="10" height="120" fill="#CBD5E1"/>
      <rect x="70" width="10" height="120" fill="#CBD5E1"/>
      <text x="45" y="135" fill="#475569" font-size="8" text-anchor="middle">Боулинг 1-12</text>
    </g>
    <!-- Столы -->
    <g transform="translate(110, 75)">
      <rect width="32" height="20" rx="2" fill="#CBD5E1"/>
      <rect y="26" width="32" height="20" rx="2" fill="#0F172A"/>
      <rect y="52" width="32" height="20" rx="2" fill="#CBD5E1"/>
      <text x="16" y="86" fill="#475569" font-size="8" text-anchor="middle">Бильярд</text>
    </g>
    <!-- Боковая панель деталей слота -->
    <rect x="208" y="66" width="80" height="280" fill="#F1F5F9" stroke="#CBD5E1"/>
    <text x="214" y="86" fill="#0F172A" font-size="9" font-weight="700">Дорожка #03</text>
    <text x="214" y="102" fill="#16A34A" font-size="8">Свободна</text>
    <text x="214" y="125" fill="#475569" font-size="8">До 6 чел.</text>
    <rect x="214" y="315" width="68" height="22" fill="#0F172A"/>
  </g>

  <!-- 4. Визард бронирования -->
  <g transform="translate(1050, 130)">
    <rect width="330" height="360" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="330" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">4. Шаги визарда (Wizard 1-4)</text>
    <rect x="12" y="38" width="306" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Степпер -->
    <g transform="translate(24, 68)">
      <circle cx="10" cy="10" r="10" fill="#0F172A"/>
      <text x="10" y="14" fill="#FFFFFF" font-size="10" text-anchor="middle">1</text>
      <line x1="22" y1="10" x2="60" y2="10" stroke="#CBD5E1"/>
      <circle cx="72" cy="10" r="10" fill="#CBD5E1"/>
      <text x="72" y="14" fill="#475569" font-size="10" text-anchor="middle">2</text>
      <line x1="84" y1="10" x2="122" y2="10" stroke="#CBD5E1"/>
      <circle cx="134" cy="10" r="10" fill="#CBD5E1"/>
      <line x1="146" y1="10" x2="184" y2="10" stroke="#CBD5E1"/>
      <circle cx="196" cy="10" r="10" fill="#CBD5E1"/>
    </g>
    <!-- Форма -->
    <rect x="20" y="100" width="290" height="26" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="30" y="117" fill="#64748B" font-size="9">Дата игры: 20.11.2026</text>
    <rect x="20" y="134" width="140" height="26" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="30" y="151" fill="#64748B" font-size="9">Время: 17:00</text>
    <rect x="170" y="134" width="140" height="26" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="180" y="151" fill="#64748B" font-size="9">Длительность: 2ч</text>
    <rect x="20" y="168" width="290" height="26" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="30" y="185" fill="#64748B" font-size="9">Гости: 4 человека (≤ 6)</text>
    <!-- Итог расчета -->
    <rect x="20" y="206" width="290" height="90" rx="4" fill="#F1F5F9" stroke="#94A3B8"/>
    <text x="30" y="226" fill="#0F172A" font-size="10" font-weight="700">Расчет с переходом 18:00:</text>
    <text x="30" y="244" fill="#334155" font-size="9">17:00-18:00 (1ч дневной) = 1 200 ₽</text>
    <text x="30" y="258" fill="#334155" font-size="9">18:00-19:00 (1ч вечерний) = 1 800 ₽</text>
    <text x="30" y="278" fill="#0F172A" font-size="11" font-weight="800">Итого: 3 000 ₽</text>
    <rect x="20" y="306" width="290" height="36" rx="4" fill="#0F172A"/>
    <text x="165" y="328" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">Перейти к предзаказу бара &rarr;</text>
  </g>

  <!-- Ряд 2: Экраны 5-8 -->
  <!-- 5. Меню бара предзаказ -->
  <g transform="translate(60, 520)">
    <rect width="300" height="380" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="300" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">5. Меню бара (Предзаказ к дорожке)</text>
    <rect x="12" y="38" width="276" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Категории меню -->
    <rect x="12" y="66" width="276" height="85" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="86" fill="#0F172A" font-size="10" font-weight="700">Пицца Пепперони 35см</text>
    <text x="24" y="102" fill="#64748B" font-size="9">Томатный соус, моцарелла, колбаски</text>
    <text x="24" y="124" fill="#0F172A" font-size="11" font-weight="700">650 ₽</text>
    <rect x="220" y="108" width="58" height="22" fill="#334155"/>

    <rect x="12" y="160" width="276" height="85" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="180" fill="#0F172A" font-size="10" font-weight="700">Бургер Strike Deluxe</text>
    <text x="24" y="196" fill="#64748B" font-size="9">Говядина Black Angus, чеддер, фри</text>
    <text x="24" y="218" fill="#0F172A" font-size="11" font-weight="700">550 ₽</text>
    <rect x="220" y="202" width="58" height="22" fill="#334155"/>

    <rect x="12" y="254" width="276" height="60" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="274" fill="#0F172A" font-size="10" font-weight="700">Морс клюквенный 1л — 300 ₽</text>
    <rect x="220" y="268" width="58" height="22" fill="#334155"/>

    <!-- Подвал заказа -->
    <rect x="12" y="324" width="276" height="42" rx="4" fill="#0F172A"/>
    <text x="150" y="350" fill="#FFFFFF" font-size="11" font-weight="600" text-anchor="middle">В корзине 2 поз. на 1 200 ₽</text>
  </g>

  <!-- 6. Проверка статуса брони -->
  <g transform="translate(390, 520)">
    <rect width="300" height="380" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="300" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">6. Проверка брони &amp; Отмена</text>
    <rect x="12" y="38" width="276" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Поле поиска -->
    <rect x="12" y="66" width="276" height="30" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="85" fill="#64748B" font-size="10">Введите код брони (SP-84920)</text>
    <!-- Карточка найденной брони -->
    <rect x="12" y="106" width="276" height="190" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="24" y="128" fill="#0F172A" font-size="12" font-weight="700">Бронь #SP-84920 [CONFIRMED]</text>
    <text x="24" y="148" fill="#475569" font-size="10">Зона: Боулинг, Дорожка #03</text>
    <text x="24" y="166" fill="#475569" font-size="10">Время: 20.11.2026, 17:00 – 19:00</text>
    <text x="24" y="184" fill="#475569" font-size="10">Гости: 4 человека</text>
    <text x="24" y="202" fill="#475569" font-size="10">Сумма: 3 000 ₽ (Оплачено 100%)</text>
    <text x="24" y="222" fill="#16A34A" font-size="10">Предзаказ бара: Пицца + Напитки</text>

    <!-- Кнопки управления -->
    <rect x="12" y="306" width="276" height="30" rx="4" fill="#DC2626"/>
    <text x="150" y="325" fill="#FFFFFF" font-size="10" font-weight="600" text-anchor="middle">Отменить бронирование (&gt; 2ч)</text>
    <rect x="12" y="342" width="276" height="28" rx="4" fill="#E2E8F0"/>
    <text x="150" y="360" fill="#334155" font-size="10" text-anchor="middle">Скачать квитанцию PDF</text>
  </g>

  <!-- 7. Личный кабинет и клубная карта -->
  <g transform="translate(720, 520)">
    <rect width="300" height="380" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="300" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">7. Личный кабинет &amp; Клубная карта</text>
    <rect x="12" y="38" width="276" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Виртуальная клубная карта -->
    <rect x="12" y="66" width="276" height="130" rx="8" fill="#0F172A"/>
    <text x="28" y="94" fill="#38BDF8" font-size="13" font-weight="800">STRIKE &amp; POCKET CLUB</text>
    <text x="28" y="118" fill="#FBBF24" font-size="12" font-weight="700">GOLD STATUS • СКИДКА 10%</text>
    <text x="28" y="146" fill="#FFFFFF" font-size="11">Владелец: Вадим Верин</text>
    <text x="28" y="168" fill="#94A3B8" font-size="10">Карта №: SP-GOLD-8492</text>
    <rect x="210" y="130" width="60" height="50" fill="#FFFFFF"/>
    <text x="240" y="158" fill="#000000" font-size="8" text-anchor="middle">[QR-код]</text>

    <!-- История бронирований -->
    <rect x="12" y="206" width="276" height="48" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="20" y="226" fill="#0F172A" font-size="10" font-weight="600">14.11.2026 • Русский бильярд</text>
    <text x="20" y="242" fill="#64748B" font-size="9">2 часа • Стол #02 • Завершен</text>

    <rect x="12" y="260" width="276" height="48" rx="4" fill="#F8FAFC" stroke="#CBD5E1"/>
    <text x="20" y="280" fill="#0F172A" font-size="10" font-weight="600">02.11.2026 • Боулинг Brunswick</text>
    <text x="20" y="296" fill="#64748B" font-size="9">3 часа • Дорожка #05 • Завершен</text>

    <rect x="12" y="324" width="276" height="36" rx="4" fill="#0F172A"/>
    <text x="150" y="346" fill="#FFFFFF" font-size="10" font-weight="600" text-anchor="middle">Забронировать со скидкой 10%</text>
  </g>

  <!-- 8. АРМ Оператора зала -->
  <g transform="translate(1050, 520)">
    <rect width="330" height="380" rx="8" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
    <rect width="330" height="28" rx="8" fill="#E2E8F0"/>
    <text x="14" y="18" fill="#334155" font-size="11" font-weight="700">8. АРМ Оператора (Тайм-сетка)</text>
    <rect x="12" y="38" width="306" height="20" fill="#F1F5F9" stroke="#CBD5E1"/>
    <!-- Таблица тайм-сетки -->
    <rect x="12" y="66" width="306" height="240" fill="#F8FAFC" stroke="#94A3B8"/>
    <!-- Временная шкала 16:00 - 21:00 -->
    <text x="20" y="84" fill="#475569" font-size="8" font-weight="700">ДОРОЖКА</text>
    <text x="90" y="84" fill="#475569" font-size="8">16:00</text>
    <text x="140" y="84" fill="#475569" font-size="8">17:00</text>
    <text x="190" y="84" fill="#475569" font-size="8">18:00</text>
    <text x="240" y="84" fill="#475569" font-size="8">19:00</text>
    <line x1="12" y1="92" x2="318" y2="92" stroke="#CBD5E1"/>

    <text x="20" y="112" fill="#0F172A" font-size="9" font-weight="700">#01</text>
    <rect x="90" y="100" width="95" height="18" rx="2" fill="#0F172A"/>
    <text x="137" y="112" fill="#FFFFFF" font-size="7" text-anchor="middle">Бронь #102</text>

    <text x="20" y="138" fill="#0F172A" font-size="9" font-weight="700">#02</text>
    <rect x="140" y="126" width="145" height="18" rx="2" fill="#334155"/>
    <text x="212" y="138" fill="#FFFFFF" font-size="7" text-anchor="middle">Бронь #108</text>

    <text x="20" y="164" fill="#0F172A" font-size="9" font-weight="700">#03</text>
    <rect x="140" y="152" width="95" height="18" rx="2" fill="#DC2626"/>
    <text x="187" y="164" fill="#FFFFFF" font-size="7" text-anchor="middle">No-Show (+15м)</text>

    <text x="20" y="190" fill="#0F172A" font-size="9" font-weight="700">#04</text>
    <rect x="190" y="178" width="95" height="18" rx="2" fill="#0F172A"/>

    <!-- Кнопки быстрых действий -->
    <rect x="12" y="318" width="145" height="42" rx="4" fill="#0F172A"/>
    <text x="84" y="342" fill="#FFFFFF" font-size="9" font-weight="600" text-anchor="middle">+ Новая бронь стойки</text>

    <rect x="167" y="318" width="151" height="42" rx="4" fill="#16A34A"/>
    <text x="242" y="342" fill="#FFFFFF" font-size="9" font-weight="600" text-anchor="middle">Печать чека 54-ФЗ</text>
  </g>
</svg>"""

with open(os.path.join(out_dir, "04_Wireframes_Monochrome.svg"), "w", encoding="utf-8") as f:
    f.write(svg_04)

# -------------------------------------------------------------
# 05. Desktop 1440 Home & Booking Wizard (1440x960)
# -------------------------------------------------------------
svg_05 = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#0A0E17"/>
  
  <!-- Хедер -->
  <rect width="1440" height="72" fill="#111827" stroke="#1F2937" stroke-width="1"/>
  <text x="60" y="44" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="20" font-weight="800" letter-spacing="1">STRIKE &amp; POCKET</text>
  
  <g transform="translate(360, 44)" font-family="Inter, sans-serif" font-size="14">
    <text x="0" fill="#00E5FF" font-weight="600">Главная</text>
    <text x="90" fill="#CBD5E1">Залы и дорожки</text>
    <text x="240" fill="#CBD5E1">Интерактивная карта</text>
    <text x="430" fill="#CBD5E1">Меню бара</text>
    <text x="540" fill="#CBD5E1">Проверить бронь</text>
  </g>

  <rect x="1220" y="16" width="160" height="40" rx="8" fill="#00E5FF"/>
  <text x="1300" y="41" fill="#050B14" font-family="Inter, sans-serif" font-size="13" font-weight="700" text-anchor="middle">Быстрая бронь</text>

  <!-- Hero Section -->
  <g transform="translate(60, 110)">
    <!-- Левая колонка: Hero текст -->
    <rect width="700" height="34" rx="17" fill="#00E5FF" fill-opacity="0.1" stroke="#00E5FF" stroke-opacity="0.3"/>
    <text x="20" y="22" fill="#00E5FF" font-family="Inter, sans-serif" font-size="12" font-weight="600">ПРЕМИАЛЬНЫЙ СПОРТИВНО-РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС В УЛЬЯНОВСКЕ</text>

    <text y="90" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="44" font-weight="800" letter-spacing="-1">
      <tspan x="0" dy="0">ИГРАЙ НА ПИКЕ</tspan>
      <tspan x="0" dy="54">ЭМОЦИЙ В STRIKE &amp; POCKET</tspan>
    </text>

    <text y="230" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="15" line-height="24">
      <tspan x="0" dy="0">12 профессиональных дорожек Brunswick GS-X, 10 турнирных столов русской</tspan>
      <tspan x="0" dy="24">пирамиды, американского пула и снукера. Авторская кухня бара и мгновенное</tspan>
      <tspan x="0" dy="24">онлайн-бронирование дорожек без очередей и ожидания.</tspan>
    </text>

    <!-- Кнопки Hero -->
    <g transform="translate(0, 310)">
      <rect width="230" height="52" rx="10" fill="#00E5FF"/>
      <text x="115" y="32" fill="#050B14" font-family="Inter, sans-serif" font-size="14" font-weight="700" text-anchor="middle">Забронировать слот &rarr;</text>

      <rect x="250" width="230" height="52" rx="10" fill="#111827" stroke="#374151"/>
      <text x="365" y="32" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="14" font-weight="600" text-anchor="middle">Схема зала и слоты</text>
    </g>

    <!-- Счетчики -->
    <g transform="translate(0, 400)">
      <text x="0" y="28" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="28" font-weight="800">12</text>
      <text x="0" y="48" fill="#94A3B8" font-family="Inter, sans-serif" font-size="11">Дорожек Brunswick</text>

      <text x="160" y="28" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="28" font-weight="800">10</text>
      <text x="160" y="48" fill="#94A3B8" font-family="Inter, sans-serif" font-size="11">Турнирных столов</text>

      <text x="320" y="28" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="28" font-weight="800">18:00</text>
      <text x="320" y="48" fill="#94A3B8" font-family="Inter, sans-serif" font-size="11">Смена тарифа день/вечер</text>

      <text x="480" y="28" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="28" font-weight="800">100%</text>
      <text x="480" y="48" fill="#94A3B8" font-family="Inter, sans-serif" font-size="11">Гарантия брони 54-ФЗ</text>
    </g>
  </g>

  <!-- Правая колонка: Интерактивный виджет бронирования -->
  <g transform="translate(820, 110)">
    <rect width="560" height="460" rx="16" fill="#111827" stroke="#00E5FF" stroke-opacity="0.4" stroke-width="2"/>
    <text x="36" y="48" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="18" font-weight="700">ОНЛАЙН-РАСЧЕТ И БРОНИРОВАНИЕ</text>
    <text x="36" y="70" fill="#94A3B8" font-family="Inter, sans-serif" font-size="12">Автоматический расчет тарифа день/вечер и валидация 6 игроков</text>

    <!-- Форма виджета -->
    <g transform="translate(36, 95)">
      <!-- Выбор зоны -->
      <text y="14" fill="#CBD5E1" font-size="11" font-family="Inter, sans-serif">Игровая зона:</text>
      <rect y="22" width="235" height="44" rx="8" fill="#0A0E17" stroke="#374151"/>
      <text x="14" y="48" fill="#FFFFFF" font-size="13" font-family="Inter, sans-serif">Боулинг (12 дорожек)</text>

      <!-- Дата -->
      <g transform="translate(255, 0)">
        <text y="14" fill="#CBD5E1" font-size="11" font-family="Inter, sans-serif">Дата игры:</text>
        <rect y="22" width="235" height="44" rx="8" fill="#0A0E17" stroke="#374151"/>
        <text x="14" y="48" fill="#FFFFFF" font-size="13" font-family="Inter, sans-serif">20.11.2026</text>
      </g>

      <!-- Время начала -->
      <g transform="translate(0, 80)">
        <text y="14" fill="#CBD5E1" font-size="11" font-family="Inter, sans-serif">Время начала:</text>
        <rect y="22" width="235" height="44" rx="8" fill="#0A0E17" stroke="#00E5FF"/>
        <text x="14" y="48" fill="#00E5FF" font-size="13" font-family="Inter, sans-serif">17:00 (стык тарифов)</text>
      </g>

      <!-- Длительность -->
      <g transform="translate(255, 80)">
        <text y="14" fill="#CBD5E1" font-size="11" font-family="Inter, sans-serif">Длительность:</text>
        <rect y="22" width="235" height="44" rx="8" fill="#0A0E17" stroke="#374151"/>
        <text x="14" y="48" fill="#FFFFFF" font-size="13" font-family="Inter, sans-serif">2 часа (до 19:00)</text>
      </g>

      <!-- Количество гостей -->
      <g transform="translate(0, 160)">
        <text y="14" fill="#CBD5E1" font-size="11" font-family="Inter, sans-serif">Количество гостей (макс. 6 на дорожку):</text>
        <rect y="22" width="490" height="44" rx="8" fill="#0A0E17" stroke="#374151"/>
        <text x="14" y="48" fill="#FFFFFF" font-size="13" font-family="Inter, sans-serif">5 человек (&le; 6 чел. &mdash; одна дорожка)</text>
      </g>

      <!-- Расчет стоимости -->
      <g transform="translate(0, 245)">
        <rect width="490" height="50" rx="8" fill="#1E293B" stroke="#374151"/>
        <text x="14" y="24" fill="#94A3B8" font-size="11">Расчет: 1ч день (1200₽) + 1ч вечер (1800₽)</text>
        <text x="14" y="40" fill="#34D399" font-size="11">Клубная карта Gold (-10%): -300 ₽</text>
        <text x="476" y="32" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="18" font-weight="800" text-anchor="end">2 700 ₽</text>
      </g>

      <!-- Кнопка перехода к дорожке -->
      <rect y="310" width="490" height="50" rx="10" fill="#FFB300"/>
      <text x="245" y="341" fill="#050B14" font-family="Inter, sans-serif" font-size="14" font-weight="700" text-anchor="middle">Выбрать дорожку на схеме зала &rarr;</text>
    </g>
  </g>

  <!-- Интерактивная карта залов (Нижний блок) -->
  <g transform="translate(60, 600)">
    <rect width="1320" height="320" rx="14" fill="#111827" stroke="#374151"/>
    <text x="28" y="36" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">ИНТЕРАКТИВНАЯ СХЕМА ОБОРУДОВАНИЯ (22 ИГРОВЫХ МЕСТА)</text>
    <text x="28" y="54" fill="#94A3B8" font-size="12">Зеленый — свободен, Красный — занят, Синий — выбран вами</text>

    <!-- Дорожки боулинга 1-12 -->
    <g transform="translate(28, 75)">
      <!-- 1-12 -->
      <rect width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="18" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#1</text>

      <rect x="44" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="62" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#2</text>

      <!-- Выбранная #3 -->
      <rect x="88" width="36" height="210" rx="4" fill="#00E5FF" fill-opacity="0.8" stroke="#00E5FF" stroke-width="2"/>
      <text x="106" y="195" fill="#050B14" font-size="10" font-weight="700" text-anchor="middle">#3</text>

      <rect x="132" width="36" height="210" rx="4" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444"/>
      <text x="150" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#4</text>

      <rect x="176" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="194" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#5</text>

      <rect x="220" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="238" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#6</text>

      <rect x="264" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="282" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#7</text>

      <rect x="308" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="326" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#8</text>

      <rect x="352" width="36" height="210" rx="4" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444"/>
      <text x="370" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#9</text>

      <rect x="396" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="414" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#10</text>

      <rect x="440" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="458" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#11</text>

      <rect x="484" width="36" height="210" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="502" y="195" fill="#FFFFFF" font-size="10" text-anchor="middle">#12</text>
    </g>

    <!-- Бильярдный зал: Пирамида, Пул, Снукер -->
    <g transform="translate(580, 75)">
      <rect width="450" height="210" rx="8" fill="#0A0E17" stroke="#374151"/>
      <text x="20" y="24" fill="#38BDF8" font-size="12" font-weight="700">БИЛЬЯРДНЫЙ КЛУБ (СТОЛЫ 1-10)</text>

      <!-- 6 столов пирамиды -->
      <rect x="20" y="40" width="60" height="40" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="50" y="64" fill="#FFFFFF" font-size="9" text-anchor="middle">П-1 (12ft)</text>

      <rect x="90" y="40" width="60" height="40" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="120" y="64" fill="#FFFFFF" font-size="9" text-anchor="middle">П-2 (12ft)</text>

      <rect x="160" y="40" width="60" height="40" rx="4" fill="#EF4444" fill-opacity="0.3" stroke="#EF4444"/>
      <text x="190" y="64" fill="#FFFFFF" font-size="9" text-anchor="middle">П-3 (12ft)</text>

      <rect x="20" y="95" width="60" height="40" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="50" y="119" fill="#FFFFFF" font-size="9" text-anchor="middle">П-4 (12ft)</text>

      <rect x="90" y="95" width="60" height="40" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="120" y="119" fill="#FFFFFF" font-size="9" text-anchor="middle">П-5 (12ft)</text>

      <rect x="160" y="95" width="60" height="40" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="190" y="119" fill="#FFFFFF" font-size="9" text-anchor="middle">П-6 (12ft)</text>

      <!-- Пул 3 стола -->
      <rect x="240" y="40" width="55" height="35" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="267" y="62" fill="#FFFFFF" font-size="9" text-anchor="middle">Пул-7</text>

      <rect x="305" y="40" width="55" height="35" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="332" y="62" fill="#FFFFFF" font-size="9" text-anchor="middle">Пул-8</text>

      <rect x="240" y="95" width="55" height="35" rx="4" fill="#10B981" fill-opacity="0.3" stroke="#10B981"/>
      <text x="267" y="117" fill="#FFFFFF" font-size="9" text-anchor="middle">Пул-9</text>

      <!-- Снукер VIP -->
      <rect x="375" y="40" width="60" height="95" rx="4" fill="#A855F7" fill-opacity="0.3" stroke="#A855F7"/>
      <text x="405" y="85" fill="#FFFFFF" font-size="9" font-weight="700" text-anchor="middle">VIP #10</text>
      <text x="405" y="100" fill="#E9D5FF" font-size="8" text-anchor="middle">Снукер</text>
    </g>

    <!-- Справка выбранного слота -->
    <g transform="translate(1060, 75)">
      <rect width="230" height="210" rx="8" fill="#0A0E17" stroke="#00E5FF"/>
      <text x="18" y="30" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="14" font-weight="700">ДОРОЖКА БОУЛИНГА #03</text>
      <text x="18" y="52" fill="#CBD5E1" font-size="11">Brunswick GS-X Pro</text>
      <line x1="18" y1="64" x2="212" y2="64" stroke="#374151"/>
      <text x="18" y="86" fill="#94A3B8" font-size="11">Вместимость: до 6 чел.</text>
      <text x="18" y="106" fill="#94A3B8" font-size="11">Бортики для детей: Есть</text>
      <text x="18" y="126" fill="#94A3B8" font-size="11">Статус на 17:00: Свободна</text>
      <text x="18" y="152" fill="#10B981" font-size="12" font-weight="700">Итого за 2ч: 2 700 ₽</text>

      <rect x="18" y="165" width="194" height="34" rx="6" fill="#00E5FF"/>
      <text x="115" y="187" fill="#050B14" font-size="12" font-weight="700" text-anchor="middle">Подтвердить выбор &rarr;</text>
    </g>
  </g>
</svg>"""

with open(os.path.join(out_dir, "05_Desktop_1440_Home_and_Wizard.svg"), "w", encoding="utf-8") as f:
    f.write(svg_05)

# -------------------------------------------------------------
# 06. Mobile 375 Adaptive Screens (1440x960)
# -------------------------------------------------------------
svg_06 = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#0A0E17"/>
  <text x="60" y="60" fill="#00E5FF" font-family="Montserrat, Inter, sans-serif" font-size="28" font-weight="800" letter-spacing="1">АДАПТИВНЫЕ ЭКРАНЫ ДЛЯ MOBILE (375 PX, 4-КОЛОНОЧНАЯ СЕТКА)</text>
  <text x="60" y="85" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="14">Поведение компонентов при переходе на малые экраны: бургер-меню, Bottom Sheets и мобильный визард</text>
  <line x1="60" y1="105" x2="1380" y2="105" stroke="#374151" stroke-width="1"/>

  <!-- 3 смартфона рядом (300 x 650) -->
  <!-- Смартфон 1: Главная мобильная -->
  <g transform="translate(100, 140)">
    <!-- Рамка смартфона -->
    <rect width="340" height="740" rx="36" fill="#111827" stroke="#374151" stroke-width="3"/>
    <!-- Островок Dynamic Island -->
    <rect x="110" y="12" width="120" height="24" rx="12" fill="#000000"/>

    <!-- Мобильный экран -->
    <g transform="translate(16, 48)">
      <!-- Хедер -->
      <text x="12" y="24" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="16" font-weight="800">STRIKE &amp; POCKET</text>
      <rect x="260" y="8" width="36" height="24" rx="4" fill="#1E293B"/>
      <line x1="268" y1="15" x2="288" y2="15" stroke="#FFFFFF" stroke-width="2"/>
      <line x1="268" y1="20" x2="288" y2="20" stroke="#FFFFFF" stroke-width="2"/>
      <line x1="268" y1="25" x2="288" y2="25" stroke="#FFFFFF" stroke-width="2"/>

      <!-- Hero Banner -->
      <g transform="translate(0, 48)">
        <text y="24" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="20" font-weight="800">
          <tspan x="12" dy="0">ИГРАЙ НА ПИКЕ</tspan>
          <tspan x="12" dy="26">ЭМОЦИЙ В КЛУБЕ</tspan>
        </text>
        <text x="12" y="82" fill="#CBD5E1" font-size="11">12 дорожек боулинга и 10 столов бильярда с онлайн-бронированием.</text>

        <!-- CTA Кнопка -->
        <rect x="12" y="105" width="284" height="44" rx="8" fill="#00E5FF"/>
        <text x="154" y="132" fill="#050B14" font-size="13" font-weight="700" text-anchor="middle">Забронировать сейчас</text>
      </g>

      <!-- Карточка быстрого выбора -->
      <g transform="translate(12, 220)">
        <rect width="284" height="150" rx="10" fill="#0A0E17" stroke="#374151"/>
        <text x="14" y="24" fill="#FFFFFF" font-size="12" font-weight="700">Боулинг Brunswick GS-X</text>
        <text x="14" y="42" fill="#94A3B8" font-size="10">От 1 200 ₽/час • До 6 гостей</text>
        
        <rect x="14" y="58" width="120" height="32" rx="6" fill="#1E293B"/>
        <text x="74" y="78" fill="#CBD5E1" font-size="10" text-anchor="middle">20 Ноября</text>

        <rect x="150" y="58" width="120" height="32" rx="6" fill="#1E293B"/>
        <text x="210" y="78" fill="#00E5FF" font-size="10" text-anchor="middle">17:00 (2 часа)</text>

        <rect x="14" y="102" width="256" height="34" rx="6" fill="#FFB300"/>
        <text x="142" y="123" fill="#050B14" font-size="11" font-weight="700" text-anchor="middle">Выбрать дорожку &rarr;</text>
      </g>

      <!-- Карточка бильярда -->
      <g transform="translate(12, 385)">
        <rect width="284" height="130" rx="10" fill="#0A0E17" stroke="#374151"/>
        <text x="14" y="24" fill="#FFFFFF" font-size="12" font-weight="700">Бильярдный зал (10 столов)</text>
        <text x="14" y="42" fill="#94A3B8" font-size="10">Русская пирамида, Пул, Снукер</text>
        <text x="14" y="65" fill="#34D399" font-size="11">От 600 до 1 200 ₽/час</text>

        <rect x="14" y="82" width="256" height="34" rx="6" fill="#1E293B" stroke="#00E5FF"/>
        <text x="142" y="103" fill="#00E5FF" font-size="11" font-weight="600" text-anchor="middle">Смотреть свободные столы</text>
      </g>

      <!-- Bottom Nav Bar -->
      <g transform="translate(0, 620)">
        <rect width="308" height="52" fill="#0A0E17" stroke="#374151"/>
        <text x="36" y="30" fill="#00E5FF" font-size="10" text-anchor="middle">Главная</text>
        <text x="110" y="30" fill="#94A3B8" font-size="10" text-anchor="middle">Залы</text>
        <text x="190" y="30" fill="#94A3B8" font-size="10" text-anchor="middle">Бронь</text>
        <text x="270" y="30" fill="#94A3B8" font-size="10" text-anchor="middle">ЛК / Карта</text>
      </g>
    </g>
  </g>

  <!-- Смартфон 2: Мобильный визард и Bottom Sheet деталей слота -->
  <g transform="translate(550, 140)">
    <rect width="340" height="740" rx="36" fill="#111827" stroke="#374151" stroke-width="3"/>
    <rect x="110" y="12" width="120" height="24" rx="12" fill="#000000"/>

    <g transform="translate(16, 48)">
      <text x="12" y="24" fill="#FFFFFF" font-family="Montserrat, sans-serif" font-size="14" font-weight="700">&larr; Выбор дорожки</text>
      <text x="290" y="24" fill="#94A3B8" font-size="11" text-anchor="end">Шаг 2/4</text>

      <!-- Мобильная схема зала (горизонтальный скролл) -->
      <rect x="12" y="44" width="284" height="240" rx="8" fill="#0A0E17" stroke="#374151"/>
      <text x="24" y="68" fill="#38BDF8" font-size="11" font-weight="600">СХЕМА БОУЛИНГА (12 ДОРОЖЕК)</text>

      <g transform="translate(24, 85)">
        <rect width="18" height="130" rx="2" fill="#10B981"/>
        <rect x="23" width="18" height="130" rx="2" fill="#10B981"/>
        <!-- Выбрана #3 -->
        <rect x="46" width="18" height="130" rx="2" fill="#00E5FF" stroke="#FFFFFF" stroke-width="1.5"/>
        <rect x="69" width="18" height="130" rx="2" fill="#EF4444"/>
        <rect x="92" width="18" height="130" rx="2" fill="#10B981"/>
        <rect x="115" width="18" height="130" rx="2" fill="#10B981"/>
        <rect x="138" width="18" height="130" rx="2" fill="#10B981"/>
        <rect x="161" width="18" height="130" rx="2" fill="#10B981"/>
        <rect x="184" width="18" height="130" rx="2" fill="#EF4444"/>
        <rect x="207" width="18" height="130" rx="2" fill="#10B981"/>
        <rect x="230" width="18" height="130" rx="2" fill="#10B981"/>
      </g>

      <!-- Мобильный Bottom Sheet (всплывающая шторка) -->
      <g transform="translate(0, 310)">
        <rect width="308" height="360" rx="20" fill="#1E293B" stroke="#00E5FF" stroke-width="1.5"/>
        <!-- Хэндл шторки -->
        <rect x="134" y="10" width="40" height="4" rx="2" fill="#94A3B8"/>

        <text x="20" y="44" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="15" font-weight="700">Дорожка #03 (Brunswick)</text>
        <text x="20" y="66" fill="#CBD5E1" font-size="11">Сеанс: 20 Ноября, 17:00 &mdash; 19:00 (2 часа)</text>
        
        <rect x="20" y="80" width="268" height="85" rx="8" fill="#0A0E17"/>
        <text x="32" y="104" fill="#94A3B8" font-size="10">17:00-18:00 (Дневной): 1 200 ₽</text>
        <text x="32" y="122" fill="#94A3B8" font-size="10">18:00-19:00 (Вечерний): 1 800 ₽</text>
        <text x="32" y="140" fill="#34D399" font-size="10">Скидка Gold (-10%): -300 ₽</text>
        <text x="32" y="158" fill="#FFFFFF" font-size="12" font-weight="800">Итого: 2 700 ₽</text>

        <!-- Поле ввода клубной карты -->
        <rect x="20" y="180" width="268" height="38" rx="6" fill="#0A0E17" stroke="#374151"/>
        <text x="32" y="204" fill="#CBD5E1" font-size="11">Карта: SP-GOLD-8492 &check;</text>

        <!-- Кнопка "Далее: предзаказ бара" -->
        <rect x="20" y="235" width="268" height="46" rx="8" fill="#00E5FF"/>
        <text x="154" y="263" fill="#050B14" font-size="12" font-weight="700" text-anchor="middle">Далее: меню бара &rarr;</text>
      </g>
    </g>
  </g>

  <!-- Смартфон 3: Мобильное подтверждение и QR квитанция -->
  <g transform="translate(1000, 140)">
    <rect width="340" height="740" rx="36" fill="#111827" stroke="#374151" stroke-width="3"/>
    <rect x="110" y="12" width="120" height="24" rx="12" fill="#000000"/>

    <g transform="translate(16, 48)">
      <text x="12" y="24" fill="#10B981" font-family="Montserrat, sans-serif" font-size="15" font-weight="800">&check; БРОНЬ ПОДТВЕРЖДЕНА!</text>
      <text x="12" y="44" fill="#94A3B8" font-size="11">Код бронирования: #SP-84920</text>

      <!-- Карточка билета с перфорацией -->
      <g transform="translate(12, 60)">
        <rect width="284" height="460" rx="12" fill="#1E293B" stroke="#374151"/>
        <text x="20" y="32" fill="#FFFFFF" font-size="13" font-weight="700">Strike &amp; Pocket Ульяновск</text>
        <text x="20" y="50" fill="#94A3B8" font-size="10">ул. Гончарова, д. 25</text>
        <line x1="20" y1="62" x2="264" y2="62" stroke="#374151" stroke-dasharray="4 4"/>

        <text x="20" y="86" fill="#94A3B8" font-size="10">Игровая зона:</text>
        <text x="20" y="104" fill="#FFFFFF" font-size="12" font-weight="600">Боулинг Brunswick, Дорожка #03</text>

        <text x="20" y="130" fill="#94A3B8" font-size="10">Дата и время:</text>
        <text x="20" y="148" fill="#FFFFFF" font-size="12" font-weight="600">20.11.2026, 17:00 &mdash; 19:00</text>

        <text x="20" y="174" fill="#94A3B8" font-size="10">Количество игроков:</text>
        <text x="20" y="192" fill="#FFFFFF" font-size="12" font-weight="600">5 человек (&le; 6 чел)</text>

        <text x="20" y="218" fill="#94A3B8" font-size="10">Предзаказ к дорожке:</text>
        <text x="20" y="236" fill="#FFFFFF" font-size="11">Пицца Пепперони 35см, Морс 1л</text>

        <line x1="20" y1="254" x2="264" y2="254" stroke="#374151" stroke-dasharray="4 4"/>
        <text x="20" y="278" fill="#94A3B8" font-size="10">Оплачено онлайн (СБП):</text>
        <text x="20" y="300" fill="#00E5FF" font-size="16" font-weight="800">3 650 ₽ (Чек 54-ФЗ выслан)</text>

        <!-- QR код для турникета / оператора -->
        <rect x="82" y="325" width="120" height="110" rx="6" fill="#FFFFFF"/>
        <text x="142" y="385" fill="#000000" font-size="11" font-weight="700" text-anchor="middle">[QR БРОНИ]</text>
      </g>

      <!-- Кнопка "В личный кабинет" -->
      <rect x="12" y="540" width="284" height="44" rx="8" fill="#00E5FF"/>
      <text x="154" y="567" fill="#050B14" font-size="12" font-weight="700" text-anchor="middle">Мои бронирования в ЛК</text>
    </g>
  </g>
</svg>"""

with open(os.path.join(out_dir, "06_Mobile_375_Adaptive_Screens.svg"), "w", encoding="utf-8") as f:
    f.write(svg_06)

print("Успешно созданы все 6 векторных фреймов для Figma:")
for fname in sorted(os.listdir(out_dir)):
    p = os.path.join(out_dir, fname)
    print(f" - {fname} ({os.path.getsize(p)} байт)")
