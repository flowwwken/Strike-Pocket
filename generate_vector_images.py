"""
Генератор оптимизированных легковесных векторных изображений SVG для веб-сервиса Strike & Pocket.
Все изображения < 15 КБ, масштабируемые, с высокой контрастностью.
"""

import os

img_dir = os.path.join("backend", "static", "img")
os.makedirs(img_dir, exist_ok=True)

# 1. Bowling Hero Illustration (800x500)
bowling_svg = """<svg width="800" height="500" viewBox="0 0 800 500" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="800" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="laneGrad" x1="400" y1="120" x2="400" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <radialGradient id="neonCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#00E5FF" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="800" height="500" rx="16" fill="url(#bgGrad)"/>
  <circle cx="400" cy="180" r="240" fill="url(#neonCyan)"/>

  <!-- Перспектива дорожки боулинга -->
  <polygon points="320,130 480,130 680,500 120,500" fill="url(#laneGrad)" stroke="#00E5FF" stroke-opacity="0.3" stroke-width="2"/>
  
  <!-- Направляющие линии дорожки -->
  <line x1="360" y1="130" x2="260" y2="500" stroke="#00E5FF" stroke-width="1.5" stroke-opacity="0.4" stroke-dasharray="8 8"/>
  <line x1="400" y1="130" x2="400" y2="500" stroke="#FFB300" stroke-width="2" stroke-opacity="0.6"/>
  <line x1="440" y1="130" x2="540" y2="500" stroke="#00E5FF" stroke-width="1.5" stroke-opacity="0.4" stroke-dasharray="8 8"/>

  <!-- Кегли (Pins) в конце дорожки -->
  <g transform="translate(400, 150)">
    <!-- Ряд 4 (4 кегли) -->
    <ellipse cx="-45" cy="-25" rx="7" ry="16" fill="#FFFFFF"/>
    <ellipse cx="-15" cy="-25" rx="7" ry="16" fill="#FFFFFF"/>
    <ellipse cx="15" cy="-25" rx="7" ry="16" fill="#FFFFFF"/>
    <ellipse cx="45" cy="-25" rx="7" ry="16" fill="#FFFFFF"/>

    <!-- Ряд 3 (3 кегли) -->
    <ellipse cx="-30" cy="-10" rx="8" ry="18" fill="#FFFFFF"/>
    <ellipse cx="0" cy="-10" rx="8" ry="18" fill="#FFFFFF"/>
    <ellipse cx="30" cy="-10" rx="8" ry="18" fill="#FFFFFF"/>

    <!-- Ряд 2 (2 кегли) -->
    <ellipse cx="-15" cy="8" rx="9" ry="20" fill="#FFFFFF"/>
    <ellipse cx="15" cy="8" rx="9" ry="20" fill="#FFFFFF"/>

    <!-- Головная кегля -->
    <ellipse cx="0" cy="28" rx="10" ry="22" fill="#FFFFFF" stroke="#00E5FF" stroke-width="1"/>
    <rect x="-8" y="24" width="16" height="4" fill="#EF4444"/>
  </g>

  <!-- Шар для боулинга на переднем плане -->
  <circle cx="280" cy="400" r="54" fill="#0A0E17" stroke="#00E5FF" stroke-width="4"/>
  <circle cx="260" cy="385" r="7" fill="#00E5FF"/>
  <circle cx="280" cy="375" r="7" fill="#00E5FF"/>
  <circle cx="270" cy="405" r="7" fill="#00E5FF"/>

  <!-- Неоновый шильдик Brunswick Pro -->
  <rect x="290" y="30" width="220" height="38" rx="8" fill="#111827" stroke="#00E5FF" stroke-width="1.5"/>
  <text x="400" y="55" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="14" font-weight="800" text-anchor="middle" letter-spacing="2">BRUNSWICK GS-X</text>
</svg>"""

with open(os.path.join(img_dir, "bowling-hero.svg"), "w", encoding="utf-8") as f:
    f.write(bowling_svg)

# 2. Russian Pyramid Billiard Table (600x400)
pyramid_svg = """<svg width="600" height="400" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" rx="14" fill="#0B132B"/>
  <!-- Борта стола -->
  <rect x="50" y="50" width="500" height="300" rx="16" fill="#2E1C0C" stroke="#D97706" stroke-width="4"/>
  <!-- Сукно стола -->
  <rect x="80" y="80" width="440" height="240" rx="8" fill="#065F46" stroke="#10B981" stroke-width="2"/>
  
  <!-- 6 луз -->
  <circle cx="82" cy="82" r="14" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
  <circle cx="300" cy="78" r="12" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
  <circle cx="518" cy="82" r="14" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
  <circle cx="82" cy="318" r="14" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
  <circle cx="300" cy="322" r="12" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
  <circle cx="518" cy="318" r="14" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>

  <!-- Белые шары 68мм (Пирамида) -->
  <g transform="translate(370, 200)">
    <!-- Пирамида из 15 шаров -->
    <circle cx="0" cy="0" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="16" cy="-9" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="16" cy="9" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="32" cy="-18" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="32" cy="0" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="32" cy="18" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="48" cy="-27" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="48" cy="-9" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="48" cy="9" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
    <circle cx="48" cy="27" r="9" fill="#FFFFFF" stroke="#CBD5E1"/>
  </g>
  <!-- Биточный шар (желтый/бордовый) -->
  <circle cx="180" cy="200" r="9" fill="#F59E0B" stroke="#B45309" stroke-width="1.5"/>

  <!-- Кий -->
  <line x1="90" y1="260" x2="170" y2="206" stroke="#FDE68A" stroke-width="4" stroke-linecap="round"/>
  
  <text x="300" y="375" fill="#34D399" font-family="Montserrat, sans-serif" font-size="14" font-weight="700" text-anchor="middle">РУССКАЯ ПИРАМИДА 12FT (РУПТУР МАГНАТ)</text>
</svg>"""

with open(os.path.join(img_dir, "billiard-pyramid.svg"), "w", encoding="utf-8") as f:
    f.write(pyramid_svg)

# 3. American Pool (600x400)
pool_svg = """<svg width="600" height="400" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" rx="14" fill="#0B132B"/>
  <rect x="60" y="60" width="480" height="280" rx="16" fill="#1E293B" stroke="#38BDF8" stroke-width="3"/>
  <rect x="90" y="90" width="420" height="220" rx="8" fill="#1E40AF" stroke="#60A5FA" stroke-width="2"/>
  
  <!-- Лузы -->
  <circle cx="92" cy="92" r="14" fill="#0F172A"/>
  <circle cx="300" cy="88" r="12" fill="#0F172A"/>
  <circle cx="508" cy="92" r="14" fill="#0F172A"/>
  <circle cx="92" cy="308" r="14" fill="#0F172A"/>
  <circle cx="300" cy="312" r="12" fill="#0F172A"/>
  <circle cx="508" cy="308" r="14" fill="#0F172A"/>

  <!-- Цветные шары пула 57.2мм -->
  <circle cx="360" cy="200" r="10" fill="#EF4444"/>
  <circle cx="378" cy="190" r="10" fill="#FBBF24"/>
  <circle cx="378" cy="210" r="10" fill="#3B82F6"/>
  <circle cx="396" cy="180" r="10" fill="#A855F7"/>
  <circle cx="396" cy="200" r="10" fill="#000000" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="396" cy="220" r="10" fill="#10B981"/>

  <!-- Белый биток -->
  <circle cx="200" cy="200" r="10" fill="#FFFFFF"/>

  <text x="300" y="375" fill="#38BDF8" font-family="Montserrat, sans-serif" font-size="14" font-weight="700" text-anchor="middle">АМЕРИКАНСКИЙ ПУЛ 9FT (DYNAMIC III)</text>
</svg>"""

with open(os.path.join(img_dir, "billiard-pool.svg"), "w", encoding="utf-8") as f:
    f.write(pool_svg)

# 4. Bar Lounge & Cocktails (600x400)
bar_svg = """<svg width="600" height="400" viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" rx="14" fill="#0F172A"/>
  <!-- Неоновый контур бокалов и пиццы -->
  <circle cx="300" cy="170" r="120" fill="#A855F7" fill-opacity="0.1" stroke="#A855F7" stroke-dasharray="6 6"/>
  
  <!-- Коктейльный бокал -->
  <polygon points="260,130 340,130 300,190" fill="none" stroke="#00E5FF" stroke-width="3"/>
  <line x1="300" y1="190" x2="300" y2="250" stroke="#00E5FF" stroke-width="3"/>
  <line x1="270" y1="250" x2="330" y2="250" stroke="#00E5FF" stroke-width="3" stroke-linecap="round"/>
  <circle cx="310" cy="140" r="6" fill="#EF4444"/> <!-- Оливка/вишенка -->

  <!-- Пицца слайс -->
  <path d="M 360 210 L 440 180 A 90 90 0 0 1 450 250 Z" fill="#FFB300" fill-opacity="0.2" stroke="#FFB300" stroke-width="3"/>
  <circle cx="410" cy="210" r="4" fill="#EF4444"/>
  <circle cx="430" cy="225" r="4" fill="#EF4444"/>

  <text x="300" y="320" fill="#FFB300" font-family="Montserrat, sans-serif" font-size="16" font-weight="700" text-anchor="middle">РЕСТОРАН И ЛАУНДЖ-БАР</text>
  <text x="300" y="345" fill="#CBD5E1" font-family="Inter, sans-serif" font-size="12" text-anchor="middle">Предзаказ горячей пиццы, бургеров и напитков прямо к дорожке</text>
</svg>"""

with open(os.path.join(img_dir, "bar-cocktails.svg"), "w", encoding="utf-8") as f:
    f.write(bar_svg)

# 5. Club Loyalty Card (500x300)
card_svg = """<svg width="500" height="300" viewBox="0 0 500 300" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="500" y2="300" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1E293B"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
  </defs>
  <rect width="500" height="300" rx="18" fill="url(#cardGrad)" stroke="#F59E0B" stroke-width="2"/>
  <text x="40" y="55" fill="#00E5FF" font-family="Montserrat, sans-serif" font-size="18" font-weight="800" letter-spacing="1.5">STRIKE &amp; POCKET</text>
  <text x="40" y="80" fill="#FBBF24" font-family="Montserrat, sans-serif" font-size="14" font-weight="700">GOLD PRIVILEGE CLUB</text>

  <!-- Чип карты -->
  <rect x="40" y="110" width="48" height="38" rx="6" fill="#FBBF24" stroke="#D97706"/>
  <line x1="64" y1="110" x2="64" y2="148" stroke="#92400E"/>
  <line x1="40" y1="129" x2="88" y2="129" stroke="#92400E"/>

  <text x="40" y="195" fill="#CBD5E1" font-family="monospace" font-size="18" letter-spacing="3">SP-GOLD-84920</text>
  <text x="40" y="240" fill="#94A3B8" font-size="11">Владелец: Верин Вадим Сергеевич</text>
  <text x="40" y="260" fill="#34D399" font-size="12" font-weight="700">Скидка: 10% на все услуги боулинга и бильярда</text>

  <!-- QR код имитация -->
  <rect x="390" y="180" width="70" height="70" rx="4" fill="#FFFFFF"/>
  <rect x="400" y="190" width="20" height="20" fill="#000000"/>
  <rect x="430" y="190" width="20" height="20" fill="#000000"/>
  <rect x="400" y="220" width="20" height="20" fill="#000000"/>
  <rect x="425" y="220" width="10" height="10" fill="#000000"/>
  <rect x="440" y="235" width="10" height="10" fill="#000000"/>
</svg>"""

with open(os.path.join(img_dir, "club-card-gold.svg"), "w", encoding="utf-8") as f:
    f.write(card_svg)

print("Все 5 векторных иллюстраций успешно созданы в", img_dir)
