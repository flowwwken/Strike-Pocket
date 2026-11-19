"""
Скрипт рендеринга всех 8 страниц веб-сервиса «Strike & Pocket» через Django Test Client.
Сохраняет HTML-код страниц со встраиванием CSS и SVG для последующего снятия скриншотов через Puppeteer.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strike_pocket_backend.settings')

import django
django.setup()

from django.test import Client as HttpClient
from django.urls import reverse

client = HttpClient()

pages = [
    ('01_home', reverse('home')),
    ('02_catalog', reverse('catalog')),
    ('03_hall_map', reverse('hall_map')),
    ('04_booking_wizard', reverse('booking_wizard')),
    ('05_profile', reverse('profile')),
    ('06_about', reverse('about')),
    ('07_check_booking', reverse('check_booking')),
    ('08_bar_menu', reverse('bar_menu')),
]

out_dir = Path('temp_rendered_html')
out_dir.mkdir(exist_ok=True)

# Читаем наш основной CSS-файл
css_path = Path('backend/static/css/strike_pocket.css')
with open(css_path, 'r', encoding='utf-8') as f:
    custom_css = f.read()

for name, url in pages:
    res = client.get(url)
    if res.status_code == 200:
        html = res.content.decode('utf-8')
        # Заменяем относительную ссылку на статический CSS прямым тегом style
        html = html.replace(
            '<link rel="stylesheet" href="/static/css/strike_pocket.css">',
            f'<style>\n{custom_css}\n</style>'
        )
        # Подменяем пути к static img на абсолютные file:// URL для локального рендера
        img_dir = (Path(__file__).resolve().parent / 'backend' / 'static' / 'img').as_uri()
        html = html.replace('/static/img/', f'{img_dir}/')

        out_file = out_dir / f'{name}.html'
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Rendered {name} -> {out_file} ({len(html)} bytes)')
    else:
        print(f'Error rendering {name}: status {res.status_code}')

print('All pages successfully dumped for Puppeteer!')
