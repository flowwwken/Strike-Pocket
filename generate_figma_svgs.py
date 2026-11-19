"""
Генератор чистых векторных файлов SVG, оптимизированных для прямого импорта в Figma (Drag-and-Drop)
Создает готовые фреймы с векторными объектами и редактируемым текстом.
"""

import os

out_dir = os.path.join("06_День_6_Проектирование_интерфейса", "figma_svg_frames")
os.makedirs(out_dir, exist_ok=True)

# 1. UI-Kit Frame (1440 x 960)
ui_kit_svg = """<svg width="1440" height="960" viewBox="0 0 1440 960" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1440" height="960" fill="#0A0E17"/>
  
  <!-- Header -->
  <text x="60" y="60" fill="#00E5FF" font-family="Montserrat, Inter, sans-serif" font-size="28" font-weight="800" letter-spacing="1">STRIKE &amp; POCKET — ДИЗАЙН-СИСТЕМА И UI-KIT</text>
  <text x="60" y="85" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="14">Тема Dark Neon Lounge • Базовый модуль 8-pt Grid • Гарнитуры Montserrat / Inter</text>
  <line x1="60" y1="105" x2="1380" y2="105" stroke="#374151" stroke-width="1"/>

  <!-- Колонка 1: Цветовая палитра -->
  <g transform="translate(60, 130)">
    <rect width="400" height="780" rx="12" fill="#111827" stroke="#00E5FF" stroke-opacity="0.25"/>
    <text x="24" y="36" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">1. ЦВЕТОВАЯ ПАЛИТРА</text>
    <line x1="24" y1="48" x2="376" y2="48" stroke="#374151" stroke-width="1"/>

    <!-- Swatches -->
    <g transform="translate(24, 65)">
      <!-- Primary -->
      <rect y="0" width="352" height="48" rx="8" fill="#00E5FF"/>
      <text x="16" y="30" fill="#050B14" font-family="Inter, sans-serif" font-size="13" font-weight="700">Primary Cyan</text>
      <text x="270" y="30" fill="#050B14" font-family="monospace" font-size="12">#00E5FF</text>

      <!-- Secondary -->
      <rect y="56" width="352" height="48" rx="8" fill="#FFB300"/>
      <text x="16" y="86" fill="#050B14" font-family="Inter, sans-serif" font-size="13" font-weight="700">Secondary Amber</text>
      <text x="270" y="86" fill="#050B14" font-family="monospace" font-size="12">#FFB300</text>

      <!-- Success -->
      <rect y="112" width="352" height="48" rx="8" fill="#10B981"/>
      <text x="16" y="142" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700">Success Green</text>
      <text x="270" y="142" fill="#FFFFFF" font-family="monospace" font-size="12">#10B981</text>

      <!-- Danger -->
      <rect y="168" width="352" height="48" rx="8" fill="#EF4444"/>
      <text x="16" y="198" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700">Danger / Error</text>
      <text x="270" y="198" fill="#FFFFFF" font-family="monospace" font-size="12">#EF4444</text>

      <!-- VIP Accent -->
      <rect y="224" width="352" height="48" rx="8" fill="#A855F7"/>
      <text x="16" y="254" fill="#FFFFFF" font-family="Inter, sans-serif" font-size="13" font-weight="700">VIP Purple (Snooker)</text>
      <text x="270" y="254" fill="#FFFFFF" font-family="monospace" font-size="12">#A855F7</text>

      <!-- Surface Card -->
      <rect y="280" width="352" height="48" rx="8" fill="#111827" stroke="#374151"/>
      <text x="16" y="310" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="13" font-weight="700">Surface Card</text>
      <text x="270" y="310" fill="#CBD5E1" font-family="monospace" font-size="12">#111827</text>

      <!-- Background Dark -->
      <rect y="336" width="352" height="48" rx="8" fill="#0A0E17" stroke="#374151"/>
      <text x="16" y="366" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="13" font-weight="700">Background Dark</text>
      <text x="270" y="366" fill="#CBD5E1" font-family="monospace" font-size="12">#0A0E17</text>

      <!-- Text Muted -->
      <rect y="392" width="352" height="48" rx="8" fill="#CBD5E1"/>
      <text x="16" y="422" fill="#0F172A" font-family="Inter, sans-serif" font-size="13" font-weight="700">Text Muted (Hi-Contrast)</text>
      <text x="270" y="422" fill="#0F172A" font-family="monospace" font-size="12">#CBD5E1</text>
    </g>
  </g>

  <!-- Колонка 2: Типографика и модули -->
  <g transform="translate(500, 130)">
    <rect width="440" height="780" rx="12" fill="#111827" stroke="#00E5FF" stroke-opacity="0.25"/>
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

  <!-- Колонка 3: Компоненты в состояниях -->
  <g transform="translate(980, 130)">
    <rect width="400" height="780" rx="12" fill="#111827" stroke="#00E5FF" stroke-opacity="0.25"/>
    <text x="24" y="36" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="16" font-weight="700">3. КОМПОНЕНТЫ (5 СОСТОЯНИЙ)</text>
    <line x1="24" y1="48" x2="376" y2="48" stroke="#374151" stroke-width="1"/>

    <g transform="translate(24, 65)">
      <!-- Buttons -->
      <text y="15" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">КНОПКА PRIMARY (CYAN):</text>
      
      <!-- Default -->
      <rect y="25" width="165" height="38" rx="8" fill="#00E5FF"/>
      <text x="22" y="49" fill="#050B14" font-size="13" font-weight="700" font-family="Inter, sans-serif">Default</text>

      <!-- Hover -->
      <rect x="180" y="25" width="165" height="38" rx="8" fill="#33EBFF" filter="drop-shadow(0 0 8px rgba(0,229,255,0.7))"/>
      <text x="202" y="49" fill="#000000" font-size="13" font-weight="700" font-family="Inter, sans-serif">Hover (Glow)</text>

      <!-- Active / Pressed -->
      <rect y="72" width="165" height="38" rx="8" fill="#00B4D8"/>
      <text x="22" y="96" fill="#000000" font-size="13" font-weight="700" font-family="Inter, sans-serif">Pressed</text>

      <!-- Disabled -->
      <rect x="180" y="72" width="165" height="38" rx="8" fill="#374151"/>
      <text x="202" y="96" fill="#9CA3AF" font-size="13" font-weight="700" font-family="Inter, sans-serif">Disabled</text>

      <!-- Inputs -->
      <text y="140" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">ПОЛЯ ВВОДА (INPUT STATES):</text>
      
      <!-- Input default -->
      <rect y="150" width="345" height="38" rx="6" fill="#0A0E17" stroke="#374151"/>
      <text x="12" y="174" fill="#CBD5E1" font-size="12" font-family="Inter, sans-serif">+7 (927) 800-00-00 [Default]</text>

      <!-- Input focus -->
      <rect y="196" width="345" height="38" rx="6" fill="#0A0E17" stroke="#00E5FF" stroke-width="1.8"/>
      <text x="12" y="220" fill="#FFFFFF" font-size="12" font-family="Inter, sans-serif">2026-11-20 [Focused]</text>

      <!-- Input error -->
      <rect y="242" width="345" height="38" rx="6" fill="#261014" stroke="#EF4444" stroke-width="1.8"/>
      <text x="12" y="266" fill="#FFFFFF" font-size="12" font-family="Inter, sans-serif">+7 (927) [Error]</text>
      <text x="4" y="295" fill="#EF4444" font-size="10" font-family="Inter, sans-serif">&times; Введите телефон в формате +7 (900) 000-00-00</text>

      <!-- Alerts -->
      <text y="325" fill="#94A3B8" font-size="11" font-family="Inter, sans-serif">СТАТУСНЫЕ АЛЕРТЫ:</text>
      
      <rect y="335" width="345" height="36" rx="6" fill="#10B981" fill-opacity="0.2" stroke="#10B981"/>
      <text x="12" y="358" fill="#34D399" font-size="12" font-family="Inter, sans-serif">&check; Бронирование успешно подтверждено</text>

      <rect y="380" width="345" height="36" rx="6" fill="#F59E0B" fill-opacity="0.2" stroke="#F59E0B"/>
      <text x="12" y="403" fill="#FBBF24" font-size="12" font-family="Inter, sans-serif">! Внимание: лимит 6 игроков на дорожку</text>
    </g>
  </g>
</svg>"""

with open(os.path.join(out_dir, "01_UI_Kit_Design_System.svg"), "w", encoding="utf-8") as f:
    f.write(ui_kit_svg)

print("Created Figma-ready SVG:", os.path.join(out_dir, "01_UI_Kit_Design_System.svg"))
