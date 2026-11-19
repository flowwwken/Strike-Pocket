/**
 * Скрипт автоматического снятия скриншотов веб-страниц «Strike & Pocket».
 * Создает скриншоты в двух ключевых разрешениях: 1440px (Desktop) и 375px (Mobile).
 * Занятия 7-9. Студент: Верин Вадим Сергеевич, группа ИСдо-45.
 */

const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const htmlDir = path.join(__dirname, 'temp_rendered_html');
const outDir = path.join(__dirname, '07_09_Дни_7_9_Разработка_интерфейса', 'screenshots');

if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

const pages = [
  { name: '01_home', title: 'Главная страница комплекса' },
  { name: '02_catalog', title: 'Каталог игровых зон и дорожек' },
  { name: '03_hall_map', title: 'Интерактивная карта залов клуба' },
  { name: '04_booking_wizard', title: 'Мастер онлайн-бронирования' },
  { name: '05_profile', title: 'Профиль гостя и клубная карта' },
  { name: '06_about', title: 'О клубе, правила и тарифная сетка' },
  { name: '07_check_booking', title: 'Проверка статуса бронирования' },
  { name: '08_bar_menu', title: 'Меню кухни и лаундж-бара' }
];

async function captureAll() {
  console.log('Запуск Chromium для захвата скриншотов...');
  const tmpProfileDir = path.join(__dirname, 'chrome_tmp_d79_' + Date.now());
  if (!fs.existsSync(tmpProfileDir)) fs.mkdirSync(tmpProfileDir, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: 'new',
    userDataDir: tmpProfileDir,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
      '--disable-crash-reporter',
      '--no-first-run',
      '--disable-extensions'
    ]
  });

  const page = await browser.newPage();

  for (const p of pages) {
    const htmlPath = path.join(htmlDir, `${p.name}.html`);
    if (!fs.existsSync(htmlPath)) continue;

    const fileUrl = 'file:///' + htmlPath.replace(/\\/g, '/');

    // 1. Десктоп (1440px)
    await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
    await page.goto(fileUrl, { waitUntil: 'load' });
    await page.evaluate(() => document.body.style.background = '#060911');
    const desktopFile = path.join(outDir, `${p.name}_desktop_1440.png`);
    await page.screenshot({ path: desktopFile, fullPage: true });
    console.log(`[OK 1440px] ${desktopFile}`);

    // 2. Мобильный (375px)
    await page.setViewport({ width: 375, height: 812, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    await page.goto(fileUrl, { waitUntil: 'load' });
    await page.evaluate(() => document.body.style.background = '#060911');
    const mobileFile = path.join(outDir, `${p.name}_mobile_375.png`);
    await page.screenshot({ path: mobileFile, fullPage: true });
    console.log(`[OK 375px]  ${mobileFile}`);
  }

  await browser.close();

  // Удаляем временный профиль chrome
  try {
    fs.rmSync(tmpProfileDir, { recursive: true, force: true });
  } catch (e) {}

  console.log('Все 16 скриншотов успешно сохранены в:', outDir);
}

captureAll().catch(err => {
  console.error('Ошибка создания скриншотов:', err);
  process.exit(1);
});
