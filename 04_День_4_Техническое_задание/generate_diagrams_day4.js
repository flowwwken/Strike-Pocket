const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function renderDiagrams() {
    const browser = await puppeteer.launch({
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crash-reporter', '--no-first-run', '--disable-extensions']
    });

    // 1. Diagram 1: Navigation and Site Map
    const page1 = await browser.newPage();
    await page1.setViewport({ width: 1200, height: 680, deviceScaleFactor: 2 });
    
    const html1 = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: "Segoe UI", Arial, sans-serif; background: #ffffff; padding: 20px; }
            .header-banner {
                background: #1b365d;
                color: #ffffff;
                text-align: center;
                padding: 14px;
                font-size: 17px;
                font-weight: bold;
                letter-spacing: 0.5px;
                border-radius: 4px;
                margin-bottom: 25px;
            }
            .root-node-wrap {
                display: flex;
                justify-content: center;
                margin-bottom: 30px;
                position: relative;
            }
            .root-node {
                background: #f4f6f9;
                border: 2px solid #1b365d;
                border-radius: 8px;
                padding: 12px 30px;
                text-align: center;
                width: 440px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.08);
            }
            .root-node .title { font-size: 15px; font-weight: bold; color: #1b365d; margin-bottom: 4px; }
            .root-node .desc { font-size: 11px; color: #555555; }
            .branches {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
            }
            .branch-col {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .branch-head {
                border-radius: 6px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 13px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            }
            .head-1 { background: #eef5ea; border: 2px solid #385723; color: #385723; }
            .head-2 { background: #fdf2e9; border: 2px solid #b95319; color: #b95319; }
            .head-3 { background: #eaf2fb; border: 2px solid #1b365d; color: #1b365d; }
            .head-4 { background: #f5eefb; border: 2px solid #6c3483; color: #6c3483; }
            .sub-card {
                background: #ffffff;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 9px 12px;
                font-size: 11.5px;
                color: #24292f;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
                line-height: 1.35;
            }
        </style>
    </head>
    <body>
        <div class="header-banner">
            СТРУКТУРНАЯ СХЕМА НАВИГАЦИИ И КАРТЫ ВЕБ-СЕРВИСА «STRIKE & POCKET»
        </div>
        <div class="root-node-wrap">
            <div class="root-node">
                <div class="title">Главная страница (/)</div>
                <div class="desc">Промо-витрина • Быстрый поиск слотов • Переход к онлайн-бронированию</div>
            </div>
        </div>
        <div class="branches">
            <div class="branch-col">
                <div class="branch-head head-1">Каталог ресурсов<br><span style="font-size:11px;font-weight:normal;">(/catalog/)</span></div>
                <div class="sub-card">Фильтрация: боулинг / бильярд</div>
                <div class="sub-card">Параметры столов (русский, пул, снукер)</div>
                <div class="sub-card">Тарифные сетки (день / вечер / вых.)</div>
                <div class="sub-card">Карточка ресурса (/lane/&lt;id&gt;/)</div>
            </div>
            <div class="branch-col">
                <div class="branch-head head-2">Онлайн-бронирование<br><span style="font-size:11px;font-weight:normal;">(/booking/)</span></div>
                <div class="sub-card">Интерактивная карта зала (SVG)</div>
                <div class="sub-card">Календарь слотов (дискретность 30/60 мин)</div>
                <div class="sub-card">Контроль лимита (до 6 чел. на дорожку)</div>
                <div class="sub-card">Калькулятор тарифа (стык 18:00)</div>
                <div class="sub-card">Предзаказ меню бара и кухни</div>
            </div>
            <div class="branch-col">
                <div class="branch-head head-3">Личный кабинет<br><span style="font-size:11px;font-weight:normal;">(/account/)</span></div>
                <div class="sub-card">Авторизация по SMS / телефону</div>
                <div class="sub-card">История и статусы броней</div>
                <div class="sub-card">Электронные чеки (54-ФЗ)</div>
                <div class="sub-card">Отмена / перенос брони (за 2 часа)</div>
                <div class="sub-card">Клубные карты и скидки</div>
            </div>
            <div class="branch-col">
                <div class="branch-head head-4">Служебный раздел<br><span style="font-size:11px;font-weight:normal;">(/admin/ | /arm/)</span></div>
                <div class="sub-card">Шахматка занятости зала (АРМ)</div>
                <div class="sub-card">Фиксация явки / отметки No-Show</div>
                <div class="sub-card">Управление светом и питанием дорожек</div>
                <div class="sub-card">Печать наряда-заказа на кухню/бар</div>
                <div class="sub-card">Экспорт финансовой отчетности</div>
            </div>
        </div>
    </body>
    </html>
    `;

    await page1.setContent(html1);
    await page1.screenshot({ path: 'fig_4_01_site_map.png' });
    console.log('Saved fig_4_01_site_map.png');
    await page1.close();

    // 2. Diagram 2: Architecture & Booking flow
    const page2 = await browser.newPage();
    await page2.setViewport({ width: 1200, height: 720, deviceScaleFactor: 2 });

    const html2 = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: "Segoe UI", Arial, sans-serif; background: #ffffff; padding: 20px; }
            .header-banner {
                background: #1b365d;
                color: #ffffff;
                text-align: center;
                padding: 13px;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 0.5px;
                border-radius: 4px;
                margin-bottom: 20px;
            }
            .container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 25px;
            }
            .panel {
                border-radius: 8px;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .client-panel {
                background: #fbfcfd;
                border: 2px solid #1b365d;
            }
            .server-panel {
                background: #24292e;
                border: 2px solid #3c4043;
                color: #e1e4e8;
            }
            .panel-title {
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                padding-bottom: 8px;
                border-bottom: 1px solid rgba(0,0,0,0.1);
            }
            .client-panel .panel-title { color: #1b365d; }
            .server-panel .panel-title { color: #58a6ff; border-bottom: 1px solid #444d56; }
            .step-box {
                background: #ffffff;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                padding: 11px;
                font-size: 12px;
                line-height: 1.4;
                box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            }
            .step-box .st-head { font-weight: bold; color: #1b365d; margin-bottom: 4px; }
            .calc-result {
                background: #eef3f8;
                border: 1.5px solid #1b365d;
                border-radius: 6px;
                padding: 12px;
                font-size: 11.5px;
                line-height: 1.45;
            }
            .calc-result .formula { font-weight: bold; color: #1b365d; margin-bottom: 4px; }
            .calc-result .total { font-size: 13px; font-weight: bold; color: #d03801; margin-top: 4px; }
            .btn-book {
                background: #1b365d;
                color: #ffffff;
                text-align: center;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                margin-top: 4px;
            }
            .srv-box {
                background: #2f363d;
                border: 1px solid #444d56;
                border-radius: 6px;
                padding: 11px;
                font-size: 11.5px;
                line-height: 1.4;
            }
            .srv-box .st-head { font-weight: bold; color: #79b8ff; margin-bottom: 4px; }
        </style>
    </head>
    <body>
        <div class="header-banner">
            АРХИТЕКТУРНО-ФУНКЦИОНАЛЬНАЯ СХЕМА ОНЛАЙН-БРОНИРОВАНИЯ И ВАЛИДАЦИИ ТАРИФОВ
        </div>
        <div class="container">
            <div class="panel client-panel">
                <div class="panel-title">БРАУЗЕР ПОЛЬЗОВАТЕЛЯ: СТРАНИЦА БРОНИРОВАНИЯ (/booking/)</div>
                <div class="step-box">
                    <div class="st-head">1. Выбор ресурса и даты:</div>
                    • Тип: Боулинг Brunswick (1–12) или Русский бильярд 12ft (1–6)<br>
                    • Интерактивная схема зала (SVG): выбор дорожки № 4<br>
                    • Календарь даты: [ 2026-11-20 ]
                </div>
                <div class="step-box">
                    <div class="st-head">2. Параметры времени и контроль лимита игроков:</div>
                    • Время сеанса: 17:00 – 19:00 (длительность 2 часа)<br>
                    • Количество игроков: 7 человек &rarr; <b>ПРЕДУПРЕЖДЕНИЕ: Лимит 6 чел.!</b><br>
                    • Предложение системы: «Забронировать 2 соседние дорожки (№4 и №5)»
                </div>
                <div class="step-box">
                    <div class="st-head">3. Предзаказ кухни/бара и данные гостя:</div>
                    • Заказ бара: Пицца Пепперони (650 р.), Морс клюквенный (250 р.)<br>
                    • Контакты: +7 (999) 123-45-67 • Клубная карта: [ GOLD-4412 ] (-10%)
                </div>
                <div class="calc-result">
                    <div class="formula">ДИНАМИЧЕСКИЙ РАСЧЕТ ЦЕНЫ (Асинхронный fetch /api/calculate-price/):</div>
                    <b>Формула:</b> P = T_до_18 (1ч &times; 800р) + T_после_18 (1ч &times; 1400р) + Бар (900р) - 10%<br>
                    Детализация: Дневной тариф (до 18:00): 800 р. | Вечерний (после 18:00): 1 400 р.<br>
                    <div class="total">ИТОГО К ОПЛАТЕ ДЕПОЗИТА: 2 790 руб. [Статус: СЛОТ СВОБОДЕН]</div>
                </div>
                <div class="btn-book">ПЕРЕЙТИ К ОПЛАТЕ БРОНИРОВАНИЯ</div>
            </div>

            <div class="panel server-panel">
                <div class="panel-title">СЕРВЕР DJANGO (БЭКЕНД И БАЗА ДАННЫХ)</div>
                <div class="srv-box">
                    <div class="st-head">1. Обработчик /api/calculate-price/ (TariffService)</div>
                    Принимает JSON (resource_id, start_time, duration, guests, card_id).<br>
                    Разделяет интервал на дневные часы (до 18:00) и вечерние (после 18:00).<br>
                    Мгновенно возвращает детализированный расчет стоимости (отклик &lt; 50 мс).
                </div>
                <div class="srv-box">
                    <div class="st-head">2. Модуль контроля слотов и лимитов (BookingValidator)</div>
                    ORM-запрос: Slot.objects.filter(resource, time_range).exists().<br>
                    Проверка вместимости: if guests &gt; 6: require_second_lane().<br>
                    Блокировка даты и времени слота при исчерпании свободных дорожек.
                </div>
                <div class="srv-box">
                    <div class="st-head">3. Атомарное сохранение (transaction.atomic)</div>
                    Пессимистическая блокировка строки слота (select_for_update).<br>
                    Создание Booking (статус: «Ожидает оплаты»), резерв на 10 минут.<br>
                    Сохранение OrderItem предзаказа бара (Many-to-Many).<br>
                    Фискализация по 54-ФЗ и передача в онлайн-эквайринг.
                </div>
                <div class="srv-box">
                    <div class="st-head">4. Оповещение персонала и аппаратная интеграция</div>
                    Звуковой сигнал и push-уведомление в АРМ Администратора клуба.<br>
                    Печать наряда-заказа на кухню/бар ровно к моменту начала сеанса.<br>
                    Фоновая задача Celery: включение светильника над столом бильярда.
                </div>
            </div>
        </div>
    </body>
    </html>
    `;

    await page2.setContent(html2);
    await page2.screenshot({ path: 'fig_4_02_architecture.png' });
    console.log('Saved fig_4_02_architecture.png');
    await page2.close();

    await browser.close();
}

renderDiagrams();
