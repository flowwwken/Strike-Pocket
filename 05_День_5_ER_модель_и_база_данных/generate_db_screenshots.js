const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const dbData = JSON.parse(fs.readFileSync('db_preview_data.json', 'utf-8'));

async function generateScreenshots() {
    const tmpDir = path.join(__dirname, 'chrome_tmp_scr_' + Date.now());
    if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

    const browser = await puppeteer.launch({
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: 'new',
        userDataDir: tmpDir,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crash-reporter', '--no-first-run', '--disable-extensions']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 760, deviceScaleFactor: 2 });

    // -------------------------------------------------------------
    // Скриншот 1: Структура базы данных в DB Browser for SQLite
    // -------------------------------------------------------------
    const schemaHtml = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", Arial, sans-serif; }
            body { background: #f0f0f0; padding: 12px; }
            .window {
                background: #ffffff;
                border: 1px solid #707070;
                box-shadow: 0 4px 16px rgba(0,0,0,0.25);
                border-radius: 6px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                height: 720px;
            }
            .title-bar {
                background: #e1e4e8;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 10px;
                border-bottom: 1px solid #d0d0d0;
                user-select: none;
            }
            .title-left {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 12px;
                color: #222;
                font-weight: 500;
            }
            .title-icon {
                width: 16px;
                height: 16px;
                background: #0969da;
                border-radius: 3px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 10px;
                font-weight: bold;
            }
            .win-buttons {
                display: flex;
                gap: 12px;
                font-size: 11px;
                color: #555;
            }
            .menu-bar {
                background: #fbfbfb;
                border-bottom: 1px solid #e5e5e5;
                padding: 4px 10px;
                display: flex;
                gap: 16px;
                font-size: 12px;
                color: #333;
            }
            .toolbar {
                background: #f7f7f7;
                border-bottom: 1px solid #e1e4e8;
                padding: 6px 12px;
                display: flex;
                align-items: center;
                gap: 14px;
                font-size: 11px;
                color: #444;
            }
            .tool-btn {
                background: #ffffff;
                border: 1px solid #ccc;
                padding: 3px 8px;
                border-radius: 3px;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            .tabs-bar {
                background: #e8ecf1;
                display: flex;
                padding-left: 10px;
                padding-top: 6px;
                border-bottom: 1px solid #c9d0d8;
                gap: 2px;
            }
            .tab {
                padding: 6px 16px;
                font-size: 12px;
                background: #dce2e9;
                border: 1px solid #b5c0cc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: #333;
            }
            .tab.active {
                background: #ffffff;
                border-color: #c9d0d8;
                border-bottom: 1px solid #ffffff;
                font-weight: 600;
                color: #0969da;
                margin-bottom: -1px;
            }
            .content-area {
                flex: 1;
                display: flex;
                background: #ffffff;
                overflow: hidden;
            }
            .tree-view {
                flex: 1;
                padding: 10px;
                overflow-y: auto;
                font-size: 12px;
                font-family: Consolas, monospace;
            }
            .tree-table {
                width: 100%;
                border-collapse: collapse;
                text-align: left;
                font-size: 11px;
            }
            .tree-table th {
                background: #f0f3f6;
                padding: 6px 8px;
                border: 1px solid #d0d7de;
                font-family: "Segoe UI", sans-serif;
                font-weight: 600;
                font-size: 11px;
                color: #333;
            }
            .tree-table td {
                padding: 4px 8px;
                border: 1px solid #e1e4e8;
            }
            .tree-table tr.header-row {
                background: #fbfcfd;
                font-weight: bold;
                color: #1f2328;
                cursor: pointer;
            }
            .tbl-tag {
                background: #ddf4ff;
                color: #0969da;
                padding: 1px 5px;
                border-radius: 3px;
                font-size: 10px;
                font-weight: bold;
                margin-right: 6px;
            }
            .status-bar {
                background: #f0f0f0;
                border-top: 1px solid #d0d0d0;
                height: 24px;
                display: flex;
                align-items: center;
                padding: 0 10px;
                font-size: 11px;
                color: #666;
                justify-content: space-between;
            }
        </style>
    </head>
    <body>
        <div class="window">
            <div class="title-bar">
                <div class="title-left">
                    <div class="title-icon">SQL</div>
                    <span>DB Browser for SQLite - C:\\Users\\Чошгун\\Desktop\\praktika1vadim\\db.sqlite3</span>
                </div>
                <div class="win-buttons">
                    <span>—</span>
                    <span>▢</span>
                    <span>✕</span>
                </div>
            </div>
            <div class="menu-bar">
                <span>Файл</span>
                <span>Правка</span>
                <span>Вид</span>
                <span>Инструменты</span>
                <span>Справка</span>
            </div>
            <div class="toolbar">
                <div class="tool-btn">📂 Открыть БД</div>
                <div class="tool-btn">💾 Записать изменения</div>
                <div class="tool-btn">↺ Откатить изменения</div>
                <span style="color:#aaa;">|</span>
                <span>Схема: SQLite 3 (UTF-8)</span>
                <span style="color:#aaa;">|</span>
                <span>Таблиц приложения: 10</span>
            </div>
            <div class="tabs-bar">
                <div class="tab active">Структура БД</div>
                <div class="tab">Данные</div>
                <div class="tab">Прагмы</div>
                <div class="tab">SQL</div>
            </div>
            <div class="content-area">
                <div class="tree-view">
                    <table class="tree-table">
                        <thead>
                            <tr>
                                <th style="width: 320px;">Объект БД / Поле</th>
                                <th style="width: 140px;">Тип данных</th>
                                <th style="width: 90px;">Ограничения</th>
                                <th>SQL DDL определение таблицы</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- club_booking_booking -->
                            <tr class="header-row">
                                <td><span class="tbl-tag">TABLE</span> <b>club_booking_booking</b> (36 строк)</td>
                                <td>table</td>
                                <td>PRIMARY</td>
                                <td style="color:#57606a;">CREATE TABLE "club_booking_booking" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT...)</td>
                            </tr>
                            <tr><td style="padding-left: 24px;">🔑 id</td><td>integer</td><td>NOT NULL, PK</td><td style="color:#888;">Первичный ключ автоинкремент</td></tr>
                            <tr><td style="padding-left: 24px;">booking_number</td><td>varchar(30)</td><td>UNIQUE, NOT NULL</td><td style="color:#888;">Уникальный номер бронирования SP-YYYYMMDD-XXXX</td></tr>
                            <tr><td style="padding-left: 24px;">🔗 client_id</td><td>integer</td><td>NOT NULL, FK</td><td style="color:#888;">Внешний ключ -> club_booking_client(id)</td></tr>
                            <tr><td style="padding-left: 24px;">🔗 resource_id</td><td>integer</td><td>NOT NULL, FK</td><td style="color:#888;">Внешний ключ -> club_booking_clubresource(id)</td></tr>
                            <tr><td style="padding-left: 24px;">booking_date</td><td>date</td><td>NOT NULL</td><td style="color:#888;">Дата проведения игры</td></tr>
                            <tr><td style="padding-left: 24px;">time_start / time_end</td><td>time</td><td>NOT NULL</td><td style="color:#888;">Временной интервал сеанса (CHECK time_end > time_start)</td></tr>
                            <tr><td style="padding-left: 24px;">total_cost / deposit_amount</td><td>decimal(9,2)</td><td>NOT NULL</td><td style="color:#888;">Сумма аренды с учетом бара и размер 50% депозита</td></tr>
                            <tr><td style="padding-left: 24px;">status</td><td>varchar(20)</td><td>NOT NULL</td><td style="color:#888;">NEW, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED</td></tr>

                            <!-- club_booking_client -->
                            <tr class="header-row">
                                <td><span class="tbl-tag">TABLE</span> <b>club_booking_client</b> (16 строк)</td>
                                <td>table</td>
                                <td>PRIMARY</td>
                                <td style="color:#57606a;">CREATE TABLE "club_booking_client" ("id" integer NOT NULL PRIMARY KEY...)</td>
                            </tr>
                            <tr><td style="padding-left: 24px;">🔑 id</td><td>integer</td><td>NOT NULL, PK</td><td style="color:#888;">Первичный ключ клиента</td></tr>
                            <tr><td style="padding-left: 24px;">last_name / first_name</td><td>varchar(50)</td><td>NOT NULL</td><td style="color:#888;">Фамилия и имя клиента</td></tr>
                            <tr><td style="padding-left: 24px;">phone</td><td>varchar(20)</td><td>UNIQUE, NOT NULL</td><td style="color:#888;">Контактный номер телефона +7XXXXXXXXXX</td></tr>
                            <tr><td style="padding-left: 24px;">email</td><td>varchar(254)</td><td>UNIQUE, NOT NULL</td><td style="color:#888;">E-mail для чеков и уведомлений</td></tr>
                            <tr><td style="padding-left: 24px;">bonus_balance</td><td>decimal(8,2)</td><td>NOT NULL</td><td style="color:#888;">Накопленные бонусные рубли программы лояльности</td></tr>

                            <!-- club_booking_clubresource -->
                            <tr class="header-row">
                                <td><span class="tbl-tag">TABLE</span> <b>club_booking_clubresource</b> (22 строки)</td>
                                <td>table</td>
                                <td>PRIMARY</td>
                                <td style="color:#57606a;">CREATE TABLE "club_booking_clubresource" ("id" integer NOT NULL PRIMARY KEY...)</td>
                            </tr>
                            <tr><td style="padding-left: 24px;">🔑 id</td><td>integer</td><td>NOT NULL, PK</td><td style="color:#888;">Идентификатор игрового ресурса</td></tr>
                            <tr><td style="padding-left: 24px;">🔗 category_id</td><td>integer</td><td>NOT NULL, FK</td><td style="color:#888;">Внешний ключ -> club_booking_resourcecategory(id)</td></tr>
                            <tr><td style="padding-left: 24px;">resource_number / title</td><td>integer / varchar</td><td>NOT NULL</td><td style="color:#888;">Дорожки 1-12, Столы 1-10</td></tr>
                            <tr><td style="padding-left: 24px;">equipment_brand</td><td>varchar(100)</td><td>NOT NULL</td><td style="color:#888;">Brunswick GS-X, Руптур Магнат, Dynamic III</td></tr>

                            <!-- club_booking_bookingbarorder -->
                            <tr class="header-row">
                                <td><span class="tbl-tag">TABLE</span> <b>club_booking_bookingbarorder</b> (71 строка, M:M)</td>
                                <td>table</td>
                                <td>THROUGH</td>
                                <td style="color:#57606a;">CREATE TABLE "club_booking_bookingbarorder" ("id" integer NOT NULL PRIMARY KEY...)</td>
                            </tr>
                            <tr><td style="padding-left: 24px;">🔑 id</td><td>integer</td><td>NOT NULL, PK</td><td style="color:#888;">Идентификатор позиции предзаказа</td></tr>
                            <tr><td style="padding-left: 24px;">🔗 booking_id / bar_item_id</td><td>integer</td><td>NOT NULL, FK</td><td style="color:#888;">Связующие ключи Many-to-Many между Booking и BarItem</td></tr>
                            <tr><td style="padding-left: 24px;">quantity / price_at_order</td><td>integer / decimal</td><td>NOT NULL</td><td style="color:#888;">Количество порций и зафиксированная цена</td></tr>

                            <!-- club_booking_payment -->
                            <tr class="header-row">
                                <td><span class="tbl-tag">TABLE</span> <b>club_booking_payment</b> (45 строк)</td>
                                <td>table</td>
                                <td>PRIMARY</td>
                                <td style="color:#57606a;">CREATE TABLE "club_booking_payment" ("id" integer NOT NULL PRIMARY KEY...)</td>
                            </tr>
                            <tr><td style="padding-left: 24px;">🔑 id / transaction_id</td><td>integer / varchar</td><td>NOT NULL, PK, UQ</td><td style="color:#888;">ID транзакции интернет-эквайринга</td></tr>
                            <tr><td style="padding-left: 24px;">🔗 booking_id</td><td>integer</td><td>NOT NULL, FK</td><td style="color:#888;">Внешний ключ -> club_booking_booking(id)</td></tr>
                            <tr><td style="padding-left: 24px;">payment_type / method</td><td>varchar(20)</td><td>NOT NULL</td><td style="color:#888;">PREPAYMENT_50, FINAL_PAYMENT / CARD, SBP, CASH</td></tr>
                            <tr><td style="padding-left: 24px;">amount / fiscal_receipt_number</td><td>decimal / varchar</td><td>NOT NULL</td><td style="color:#888;">Фискальный знак ОФД по 54-ФЗ</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="status-bar">
                <span>База данных подключена: db.sqlite3</span>
                <span>Кодировка: UTF-8 | Таблиц: 10 | Индексов: 18</span>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(schemaHtml);
    await page.screenshot({
        path: 'screenshots/fig_5_01_db_schema.png',
        clip: { x: 0, y: 0, width: 1280, height: 760 }
    });
    console.log("Скриншот 1 (структура БД) сохранен в screenshots/fig_5_01_db_schema.png");

    // -------------------------------------------------------------
    // Скриншот 2: Просмотр записей таблицы club_booking_booking
    // -------------------------------------------------------------
    let rowsHtml = '';
    dbData.bookings.forEach((row, i) => {
        const bg = (i % 2 === 0) ? '#ffffff' : '#f9fbfd';
        rowsHtml += `
        <tr style="background:${bg};">
            <td style="text-align:center; color:#777;">${row[0]}</td>
            <td style="font-weight:600; color:#0969da;">${row[1]}</td>
            <td>${row[2]}</td>
            <td>${row[3]}</td>
            <td>${row[4]}</td>
            <td>${row[5]}-${row[6]}</td>
            <td style="text-align:center;">${row[7]}</td>
            <td style="text-align:right; font-weight:600;">${parseFloat(row[8]).toFixed(2)} ₽</td>
            <td style="text-align:right; color:#cf222e;">${parseFloat(row[9]).toFixed(2)} ₽</td>
            <td><span style="background:#dafbe1; color:#1a7f37; padding:1px 6px; border-radius:3px; font-size:10px;">${row[10]}</span></td>
        </tr>
        `;
    });

    const dataHtml = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", Arial, sans-serif; }
            body { background: #f0f0f0; padding: 12px; }
            .window {
                background: #ffffff;
                border: 1px solid #707070;
                box-shadow: 0 4px 16px rgba(0,0,0,0.25);
                border-radius: 6px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                height: 720px;
            }
            .title-bar {
                background: #e1e4e8;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 10px;
                border-bottom: 1px solid #d0d0d0;
            }
            .title-left {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 12px;
                color: #222;
                font-weight: 500;
            }
            .title-icon {
                width: 16px;
                height: 16px;
                background: #0969da;
                border-radius: 3px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 10px;
                font-weight: bold;
            }
            .menu-bar {
                background: #fbfbfb;
                border-bottom: 1px solid #e5e5e5;
                padding: 4px 10px;
                display: flex;
                gap: 16px;
                font-size: 12px;
                color: #333;
            }
            .tabs-bar {
                background: #e8ecf1;
                display: flex;
                padding-left: 10px;
                padding-top: 6px;
                border-bottom: 1px solid #c9d0d8;
                gap: 2px;
            }
            .tab {
                padding: 6px 16px;
                font-size: 12px;
                background: #dce2e9;
                border: 1px solid #b5c0cc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: #333;
            }
            .tab.active {
                background: #ffffff;
                border-color: #c9d0d8;
                border-bottom: 1px solid #ffffff;
                font-weight: 600;
                color: #0969da;
                margin-bottom: -1px;
            }
            .table-selector-bar {
                background: #f6f8fa;
                padding: 8px 12px;
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 12px;
                border-bottom: 1px solid #d0d7de;
            }
            .tbl-dropdown {
                background: #ffffff;
                border: 1px solid #d0d7de;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 600;
                color: #24292f;
            }
            .grid-container {
                flex: 1;
                overflow-y: auto;
            }
            .data-grid {
                width: 100%;
                border-collapse: collapse;
                font-size: 11px;
            }
            .data-grid th {
                background: #f0f3f6;
                padding: 6px 8px;
                border: 1px solid #d0d7de;
                font-weight: 600;
                color: #24292f;
                position: sticky;
                top: 0;
            }
            .data-grid td {
                padding: 5px 8px;
                border: 1px solid #e1e4e8;
            }
            .status-bar {
                background: #f0f0f0;
                border-top: 1px solid #d0d0d0;
                height: 24px;
                display: flex;
                align-items: center;
                padding: 0 10px;
                font-size: 11px;
                color: #555;
                justify-content: space-between;
            }
        </style>
    </head>
    <body>
        <div class="window">
            <div class="title-bar">
                <div class="title-left">
                    <div class="title-icon">SQL</div>
                    <span>DB Browser for SQLite - [Просмотр данных: club_booking_booking]</span>
                </div>
                <div style="font-size:11px; color:#555;">— ▢ ✕</div>
            </div>
            <div class="menu-bar">
                <span>Файл</span>
                <span>Правка</span>
                <span>Вид</span>
                <span>Инструменты</span>
                <span>Справка</span>
            </div>
            <div class="tabs-bar">
                <div class="tab">Структура БД</div>
                <div class="tab active">Данные</div>
                <div class="tab">Прагмы</div>
                <div class="tab">SQL</div>
            </div>
            <div class="table-selector-bar">
                <span>Таблица:</span>
                <span class="tbl-dropdown">club_booking_booking ▼</span>
                <span style="color:#888;">|</span>
                <span>Быстрый фильтр: <input type="text" placeholder="Поиск..." style="border:1px solid #ccc; padding:2px 6px; border-radius:3px; font-size:11px;" /></span>
                <span style="color:#888;">|</span>
                <span>Отображено записей: 1 - 25 из 36</span>
            </div>
            <div class="grid-container">
                <table class="data-grid">
                    <thead>
                        <tr>
                            <th style="width:40px;">id</th>
                            <th style="width:140px;">booking_number</th>
                            <th style="width:160px;">client (ФИО)</th>
                            <th style="width:160px;">resource (Оборудование)</th>
                            <th style="width:85px;">booking_date</th>
                            <th style="width:90px;">time_slot</th>
                            <th style="width:50px;">guests</th>
                            <th style="width:95px;">total_cost</th>
                            <th style="width:95px;">deposit (50%)</th>
                            <th style="width:100px;">status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rowsHtml}
                    </tbody>
                </table>
            </div>
            <div class="status-bar">
                <span>Таблица: club_booking_booking | Всего строк в базе: 36</span>
                <span>Выделена строка 1 | Кодировка: UTF-8</span>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(dataHtml);
    await page.screenshot({
        path: 'screenshots/fig_5_02_db_data_bookings.png',
        clip: { x: 0, y: 0, width: 1280, height: 760 }
    });
    console.log("Скриншот 2 (данные бронирований) сохранен в screenshots/fig_5_02_db_data_bookings.png");

    // -------------------------------------------------------------
    // Скриншот 3: Django Admin - список моделей и реестр
    // -------------------------------------------------------------
    const adminHtml = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Roboto", "Segoe UI", Arial, sans-serif; }
            body { background: #f8f9fa; color: #333; }
            .header-nav {
                background: #1b365d;
                color: #ffffff;
                padding: 12px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .header-nav h1 {
                font-size: 17px;
                font-weight: 500;
                letter-spacing: 0.5px;
            }
            .header-nav .user-info {
                font-size: 12px;
                opacity: 0.9;
            }
            .breadcrumbs {
                background: #34495e;
                color: #ecf0f1;
                padding: 8px 24px;
                font-size: 12px;
            }
            .container {
                display: flex;
                padding: 24px;
                gap: 24px;
            }
            .sidebar-card {
                flex: 1;
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                overflow: hidden;
            }
            .card-header {
                background: #f1f5f9;
                padding: 10px 16px;
                font-weight: 700;
                font-size: 13px;
                color: #1e293b;
                border-bottom: 1px solid #e2e8f0;
                display: flex;
                justify-content: space-between;
            }
            .model-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
            }
            .model-table td {
                padding: 9px 16px;
                border-bottom: 1px solid #f1f5f9;
            }
            .model-table tr:hover {
                background: #f8fafc;
            }
            .model-name {
                font-weight: 600;
                color: #0284c7;
            }
            .action-link {
                color: #64748b;
                font-size: 11px;
                text-decoration: none;
            }
            .badge-count {
                background: #e0f2fe;
                color: #0369a1;
                font-weight: bold;
                padding: 2px 7px;
                border-radius: 10px;
                font-size: 11px;
            }
        </style>
    </head>
    <body>
        <div class="header-nav">
            <h1>Панель управления Strike & Pocket | Панель администратора Django 5.2</h1>
            <div class="user-info">
                Оператор: <b>Верин Вадим Сергеевич (Администратор)</b> | Выйти
            </div>
        </div>
        <div class="breadcrumbs">
            Главная › Приложение «Управление бронированием и баром» (club_booking)
        </div>
        <div class="container">
            <!-- Модели бронирования -->
            <div class="sidebar-card">
                <div class="card-header">
                    <span>СЕРВИС БРОНИРОВАНИЯ И РЕСУРСОВ</span>
                    <span style="font-size:11px; color:#64748b;">Django ORM Models</span>
                </div>
                <table class="model-table">
                    <tr>
                        <td><span class="model-name">Бронирования</span></td>
                        <td style="text-align:right;"><span class="badge-count">36 записей</span></td>
                        <td style="width:80px; text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Клиенты</span></td>
                        <td style="text-align:right;"><span class="badge-count">16 клиентов</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Клубные карты</span></td>
                        <td style="text-align:right;"><span class="badge-count">12 карт</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Игровые ресурсы</span></td>
                        <td style="text-align:right;"><span class="badge-count">22 объекта</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Категории ресурсов</span></td>
                        <td style="text-align:right;"><span class="badge-count">4 категории</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Тарифная сетка</span></td>
                        <td style="text-align:right;"><span class="badge-count">16 тарифов</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                </table>
            </div>

            <!-- Модели бара и платежей -->
            <div class="sidebar-card">
                <div class="card-header">
                    <span>БАР, КУХНЯ И ПЛАТЕЖИ (54-ФЗ)</span>
                    <span style="font-size:11px; color:#64748b;">Связующие и финансовые таблицы</span>
                </div>
                <table class="model-table">
                    <tr>
                        <td><span class="model-name">Заказы бара к бронированиям (M:M)</span></td>
                        <td style="text-align:right;"><span class="badge-count">71 позиция</span></td>
                        <td style="width:80px; text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Платежи и фискальные чеки</span></td>
                        <td style="text-align:right;"><span class="badge-count">45 чеков</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Позиции меню бара</span></td>
                        <td style="text-align:right;"><span class="badge-count">16 блюд</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                    <tr>
                        <td><span class="model-name">Категории меню бара</span></td>
                        <td style="text-align:right;"><span class="badge-count">5 разделов</span></td>
                        <td style="text-align:right;"><span class="action-link">+ Добавить</span></td>
                    </tr>
                </table>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(adminHtml);
    await page.screenshot({
        path: 'screenshots/fig_5_03_django_admin.png',
        clip: { x: 0, y: 0, width: 1280, height: 760 }
    });
    console.log("Скриншот 3 (Django Admin) сохранен в screenshots/fig_5_03_django_admin.png");

    await browser.close();
}

generateScreenshots().catch(err => {
    console.error("Ошибка при генерации скриншотов:", err);
    process.exit(1);
});
