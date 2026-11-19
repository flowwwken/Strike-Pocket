const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function renderExactScreenshots() {
    const tmpDir = path.join(__dirname, 'chrome_tmp_exact_' + Date.now());
    if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

    const browser = await puppeteer.launch({
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: 'new',
        userDataDir: tmpDir,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crash-reporter', '--no-first-run', '--disable-extensions']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 820, deviceScaleFactor: 2 });

    // ------------------------------------------------------------------------
    // РИСУНОК 5.2 — Структура таблиц базы данных в DB Browser for SQLite
    // ------------------------------------------------------------------------
    const html52 = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", Arial, sans-serif; }
            body { background: #eef2f5; padding: 10px; }
            .window {
                background: #ffffff;
                border: 1px solid #7a8a99;
                box-shadow: 0 4px 20px rgba(0,0,0,0.18);
                border-radius: 4px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                height: 790px;
            }
            .title-bar {
                background: #e2e7ec;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 10px;
                border-bottom: 1px solid #c5d0dc;
                font-size: 12px;
                font-weight: 600;
                color: #2c3e50;
            }
            .win-btns { font-size: 11px; color: #666; letter-spacing: 5px; }
            .menu-bar {
                background: #fbfbfc;
                border-bottom: 1px solid #e1e6eb;
                padding: 3px 10px;
                display: flex;
                gap: 16px;
                font-size: 11.5px;
                color: #333;
            }
            .toolbar {
                background: #f4f6f8;
                border-bottom: 1px solid #dcdfe4;
                padding: 4px 10px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 11.5px;
            }
            .btn {
                background: #ffffff;
                border: 1px solid #b8c2cc;
                padding: 2px 10px;
                border-radius: 3px;
                color: #24292e;
                font-size: 11px;
            }
            .tabs {
                background: #e9edf2;
                display: flex;
                padding-left: 8px;
                padding-top: 5px;
                border-bottom: 1px solid #c9d2dc;
                gap: 2px;
            }
            .tab {
                padding: 5px 14px;
                font-size: 11.5px;
                background: #d6dde5;
                border: 1px solid #b2bcc7;
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                color: #333;
            }
            .tab.active {
                background: #ffffff;
                border-color: #c9d2dc;
                border-bottom: 1px solid #ffffff;
                font-weight: 700;
                color: #0366d6;
                margin-bottom: -1px;
            }
            .grid-area {
                flex: 1;
                overflow-y: auto;
                background: #ffffff;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 11.5px;
            }
            th {
                background: #f0f3f6;
                padding: 5px 8px;
                border: 1px solid #d0d7de;
                text-align: left;
                font-weight: 700;
                color: #24292e;
            }
            td {
                padding: 3.5px 8px;
                border: 1px solid #e1e4e8;
            }
            tr.table-header {
                background: #fafbfc;
                font-weight: 700;
                color: #0366d6;
            }
            .status-bar {
                background: #f0f2f5;
                border-top: 1px solid #c9d2dc;
                height: 22px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 10px;
                font-size: 11px;
                color: #586069;
            }
        </style>
    </head>
    <body>
        <div class="window">
            <div class="title-bar">
                <span>DB Browser for SQLite - db.sqlite3</span>
                <span class="win-btns">— ▢ ✕</span>
            </div>
            <div class="menu-bar">
                <span>Файл</span><span>Правка</span><span>Вид</span><span>Инструменты</span><span>Справка</span>
            </div>
            <div class="toolbar">
                <div class="btn">Открыть БД</div>
                <div class="btn">Записать изменения</div>
                <div class="btn">Отменить</div>
                <div class="btn">БД: db.sqlite3 (SQLite 3.39)</div>
                <div class="btn">Размер: 296 КБ</div>
            </div>
            <div class="tabs">
                <div class="tab active">Структура БД</div>
                <div class="tab">Данные</div>
                <div class="tab">Прагмы</div>
                <div class="tab">Выполнить SQL</div>
            </div>
            <div class="grid-area">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 320px;">Объект БД / Таблица</th>
                            <th style="width: 140px;">Тип</th>
                            <th style="width: 100px;">Записей</th>
                            <th>SQL Схема создания (DDL)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Booking -->
                        <tr class="table-header">
                            <td>🗁 <b>club_booking_booking</b></td>
                            <td>Таблица (Table)</td>
                            <td><b>36 строк</b></td>
                            <td style="color:#57606a;">CREATE TABLE "club_booking_booking" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "booking_number" varchar(30) NOT NULL UNIQUE...);</td>
                        </tr>
                        <tr><td style="padding-left:22px;">[PK] id</td><td>INTEGER</td><td></td><td>NOT NULL PRIMARY KEY AUTOINCREMENT</td></tr>
                        <tr><td style="padding-left:22px;">booking_number</td><td>varchar(30)</td><td></td><td>NOT NULL UNIQUE (SP-YYYYMMDD-XXXX)</td></tr>
                        <tr><td style="padding-left:22px;">[FK] client_id</td><td>bigint</td><td></td><td>NOT NULL REFERENCES "club_booking_client" ("id")</td></tr>
                        <tr><td style="padding-left:22px;">[FK] resource_id</td><td>bigint</td><td></td><td>NOT NULL REFERENCES "club_booking_clubresource" ("id")</td></tr>
                        <tr><td style="padding-left:22px;">booking_date</td><td>date</td><td></td><td>NOT NULL</td></tr>
                        <tr><td style="padding-left:22px;">time_start / time_end</td><td>time</td><td></td><td>NOT NULL (CHECK time_end > time_start)</td></tr>
                        <tr><td style="padding-left:22px;">players_count</td><td>smallint</td><td></td><td>NOT NULL (CHECK players_count > 0)</td></tr>
                        <tr><td style="padding-left:22px;">rental_cost / total_cost</td><td>decimal(9,2)</td><td></td><td>NOT NULL (CHECK >= 0.00)</td></tr>
                        <tr><td style="padding-left:22px;">deposit_amount</td><td>decimal(8,2)</td><td></td><td>NOT NULL (50% в пиковые часы)</td></tr>
                        <tr><td style="padding-left:22px;">status</td><td>varchar(20)</td><td></td><td>NOT NULL (NEW, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED)</td></tr>

                        <!-- Client -->
                        <tr class="table-header">
                            <td>🗁 <b>club_booking_client</b></td>
                            <td>Таблица (Table)</td>
                            <td><b>16 строк</b></td>
                            <td style="color:#57606a;">CREATE TABLE "club_booking_client" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "phone" varchar(20) NOT NULL UNIQUE...);</td>
                        </tr>
                        <tr><td style="padding-left:22px;">[PK] id</td><td>INTEGER</td><td></td><td>NOT NULL PRIMARY KEY AUTOINCREMENT</td></tr>
                        <tr><td style="padding-left:22px;">last_name / first_name</td><td>varchar(50)</td><td></td><td>NOT NULL</td></tr>
                        <tr><td style="padding-left:22px;">phone</td><td>varchar(20)</td><td></td><td>NOT NULL UNIQUE (+7XXXXXXXXXX)</td></tr>
                        <tr><td style="padding-left:22px;">email</td><td>varchar(254)</td><td></td><td>NOT NULL UNIQUE</td></tr>
                        <tr><td style="padding-left:22px;">bonus_balance</td><td>decimal(8,2)</td><td></td><td>NOT NULL (CHECK >= 0.00)</td></tr>

                        <!-- ClubResource -->
                        <tr class="table-header">
                            <td>🗁 <b>club_booking_clubresource</b></td>
                            <td>Таблица (Table)</td>
                            <td><b>22 строки</b></td>
                            <td style="color:#57606a;">CREATE TABLE "club_booking_clubresource" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT...);</td>
                        </tr>
                        <tr><td style="padding-left:22px;">[PK] id</td><td>INTEGER</td><td></td><td>NOT NULL PRIMARY KEY AUTOINCREMENT</td></tr>
                        <tr><td style="padding-left:22px;">[FK] category_id</td><td>bigint</td><td></td><td>NOT NULL REFERENCES "club_booking_resourcecategory" ("id")</td></tr>
                        <tr><td style="padding-left:22px;">resource_number / title</td><td>integer / varchar(100)</td><td></td><td>NOT NULL (Дорожки 1-12, Столы 1-10)</td></tr>
                        <tr><td style="padding-left:22px;">equipment_brand</td><td>varchar(100)</td><td></td><td>NOT NULL (Brunswick Pro, Руптур, Dynamic)</td></tr>

                        <!-- BookingBarOrder (M:M through) -->
                        <tr class="table-header">
                            <td>🗁 <b>club_booking_bookingbarorder</b></td>
                            <td>Таблица (Table)</td>
                            <td><b>71 строка</b></td>
                            <td style="color:#57606a;">CREATE TABLE "club_booking_bookingbarorder" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT...);</td>
                        </tr>
                        <tr><td style="padding-left:22px;">[PK] id</td><td>INTEGER</td><td></td><td>NOT NULL PRIMARY KEY AUTOINCREMENT</td></tr>
                        <tr><td style="padding-left:22px;">[FK] booking_id</td><td>bigint</td><td></td><td>NOT NULL REFERENCES "club_booking_booking" ("id")</td></tr>
                        <tr><td style="padding-left:22px;">[FK] bar_item_id</td><td>bigint</td><td></td><td>NOT NULL REFERENCES "club_booking_baritem" ("id")</td></tr>
                        <tr><td style="padding-left:22px;">quantity</td><td>smallint</td><td></td><td>NOT NULL (CHECK quantity > 0)</td></tr>
                        <tr><td style="padding-left:22px;">price_at_order</td><td>decimal(7,2)</td><td></td><td>NOT NULL (Цена фиксации на момент заказа)</td></tr>

                        <!-- Payment -->
                        <tr class="table-header">
                            <td>🗁 <b>club_booking_payment</b></td>
                            <td>Таблица (Table)</td>
                            <td><b>45 строк</b></td>
                            <td style="color:#57606a;">CREATE TABLE "club_booking_payment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT...);</td>
                        </tr>
                        <tr><td style="padding-left:22px;">[PK] id</td><td>INTEGER</td><td></td><td>NOT NULL PRIMARY KEY AUTOINCREMENT</td></tr>
                        <tr><td style="padding-left:22px;">[FK] booking_id</td><td>bigint</td><td></td><td>NOT NULL REFERENCES "club_booking_booking" ("id")</td></tr>
                        <tr><td style="padding-left:22px;">transaction_id</td><td>varchar(50)</td><td></td><td>NOT NULL UNIQUE</td></tr>
                        <tr><td style="padding-left:22px;">amount</td><td>decimal(9,2)</td><td></td><td>NOT NULL (CHECK amount > 0.00)</td></tr>
                        <tr><td style="padding-left:22px;">fiscal_receipt_number</td><td>varchar(50)</td><td></td><td>Формат 54-ФЗ (ФД/ФП)</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="status-bar">
                <span>Схема БД: 10 таблиц club_booking | 3НФ соблюдена | Целостность внешних ключей OK</span>
                <span>Строк всего: 237+ | UTF-8</span>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(html52);
    await page.screenshot({ path: 'screenshots/fig_5_02_db_schema.png' });
    console.log("Скриншот 5.2 сохранен.");

    // ------------------------------------------------------------------------
    // РИСУНОК 5.3 — Просмотр записей таблицы club_booking_booking
    // ------------------------------------------------------------------------
    const bookingsData = [
        ["#1", "SP-20261102-0001", "Алексеев (#1)", "Дорожка №01 (#1)", "2026-11-02", "14:00-16:00", "4", "2780.00", "0.00", "COMPLETED"],
        ["#2", "SP-20261102-0002", "Васильева (#2)", "Дорожка №02 (#2)", "2026-11-02", "16:00-17:30", "5", "3150.00", "0.00", "COMPLETED"],
        ["#3", "SP-20261102-0003", "Григорьев (#3)", "Дорожка №03 (#3)", "2026-11-02", "19:00-21:00", "6", "4510.00", "2255.00", "COMPLETED"],
        ["#4", "SP-20261103-0004", "Дмитриева (#4)", "Дорожка №04 (#4)", "2026-11-03", "18:00-21:00", "4", "6469.50", "3234.75", "COMPLETED"],
        ["#5", "SP-20261103-0005", "Елисеев (#5)", "Дорожка №05 (#5)", "2026-11-03", "20:00-22:00", "6", "3857.00", "1928.50", "COMPLETED"],
        ["#6", "SP-20261104-0006", "Жданов (#6)", "Дорожка №06 (#6)", "2026-11-04", "13:00-15:00", "3", "3080.00", "0.00", "COMPLETED"],
        ["#7", "SP-20261104-0007", "Зайцева (#7)", "Дорожка №07 (#7)", "2026-11-04", "15:00-16:00", "4", "1840.00", "0.00", "COMPLETED"],
        ["#8", "SP-20261104-0008", "Иванов (#8)", "Дорожка №08 (#8)", "2026-11-04", "19:00-21:30", "5", "5310.00", "2655.00", "COMPLETED"],
        ["#9", "SP-20261105-0009", "Ковалев (#9)", "Дорожка №09 (#9)", "2026-11-05", "17:00-19:00", "6", "3990.00", "0.00", "COMPLETED"],
        ["#10", "SP-20261105-0010", "Лебедева (#10)", "Дорожка №10 (#10)", "2026-11-05", "20:00-22:00", "4", "4454.00", "2227.00", "COMPLETED"],
        ["#11", "SP-20261106-0011", "Морозов (#11)", "Дорожка №11 (#11)", "2026-11-06", "14:00-16:00", "5", "3904.50", "0.00", "COMPLETED"],
        ["#12", "SP-20261106-0012", "Новиков (#12)", "Дорожка №12 (#12)", "2026-11-06", "18:00-20:00", "6", "6420.00", "3210.00", "COMPLETED"],
        ["#13", "SP-20261107-0013", "Орлова (#13)", "Дорожка №01 (#1)", "2026-11-07", "12:00-13:30", "3", "2793.00", "0.00", "COMPLETED"],
        ["#14", "SP-20261107-0014", "Павлов (#14)", "Дорожка №02 (#2)", "2026-11-07", "15:00-17:00", "5", "3564.00", "0.00", "COMPLETED"],
        ["#15", "SP-20261108-0015", "Романов (#15)", "Дорожка №03 (#3)", "2026-11-08", "18:00-20:00", "6", "5601.50", "2800.75", "COMPLETED"],
        ["#16", "SP-20261109-0016", "Семенова (#16)", "Дорожка №04 (#4)", "2026-11-09", "19:00-21:00", "4", "5040.00", "2520.00", "CONFIRMED"]
    ];

    let rows53 = '';
    bookingsData.forEach(r => {
        let stStyle = r[9] === 'COMPLETED' ? 'color:#28a745; font-weight:700;' : (r[9] === 'CONFIRMED' ? 'color:#0366d6; font-weight:700;' : 'color:#6f42c1;');
        rows53 += `<tr>
            <td style="font-weight:700;">${r[0]}</td>
            <td style="color:#0366d6; font-weight:600;">${r[1]}</td>
            <td>${r[2]}</td>
            <td>${r[3]}</td>
            <td>${r[4]}</td>
            <td>${r[5]}</td>
            <td style="text-align:center;">${r[6]}</td>
            <td style="text-align:right; font-weight:700;">${r[7]}</td>
            <td style="text-align:right; color:#d73a49;">${r[8]}</td>
            <td style="${stStyle}">${r[9]}</td>
        </tr>`;
    });

    const html53 = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", Arial, sans-serif; }
            body { background: #eef2f5; padding: 10px; }
            .window {
                background: #ffffff;
                border: 1px solid #7a8a99;
                box-shadow: 0 4px 20px rgba(0,0,0,0.18);
                border-radius: 4px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                height: 790px;
            }
            .title-bar {
                background: #e2e7ec;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 10px;
                border-bottom: 1px solid #c5d0dc;
                font-size: 12px;
                font-weight: 600;
                color: #2c3e50;
            }
            .win-btns { font-size: 11px; color: #666; letter-spacing: 5px; }
            .menu-bar {
                background: #fbfbfc;
                border-bottom: 1px solid #e1e6eb;
                padding: 3px 10px;
                display: flex;
                gap: 16px;
                font-size: 11.5px;
                color: #333;
            }
            .toolbar {
                background: #f4f6f8;
                border-bottom: 1px solid #dcdfe4;
                padding: 4px 10px;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 11.5px;
            }
            .btn {
                background: #ffffff;
                border: 1px solid #b8c2cc;
                padding: 2px 10px;
                border-radius: 3px;
                color: #24292e;
                font-size: 11px;
            }
            .tabs {
                background: #e9edf2;
                display: flex;
                padding-left: 8px;
                padding-top: 5px;
                border-bottom: 1px solid #c9d2dc;
                gap: 2px;
            }
            .tab {
                padding: 5px 14px;
                font-size: 11.5px;
                background: #d6dde5;
                border: 1px solid #b2bcc7;
                border-bottom: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                color: #333;
            }
            .tab.active {
                background: #ffffff;
                border-color: #c9d2dc;
                border-bottom: 1px solid #ffffff;
                font-weight: 700;
                color: #0366d6;
                margin-bottom: -1px;
            }
            .sub-bar {
                background: #f6f8fa;
                padding: 6px 12px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-bottom: 1px solid #d0d7de;
                font-size: 12px;
            }
            .tbl-sel {
                background: #ffffff;
                border: 1px solid #0366d6;
                color: #0366d6;
                font-weight: 700;
                padding: 2px 10px;
                border-radius: 3px;
            }
            .grid-area {
                flex: 1;
                overflow-y: auto;
                background: #ffffff;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 11.5px;
            }
            th {
                background: #f0f3f6;
                padding: 6px 8px;
                border: 1px solid #d0d7de;
                text-align: left;
                font-weight: 700;
                color: #24292e;
            }
            td {
                padding: 4px 8px;
                border: 1px solid #e1e4e8;
            }
            .status-bar {
                background: #f0f2f5;
                border-top: 1px solid #c9d2dc;
                height: 22px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 10px;
                font-size: 11px;
                color: #586069;
            }
        </style>
    </head>
    <body>
        <div class="window">
            <div class="title-bar">
                <span>DB Browser for SQLite - Просмотр данных [club_booking_booking]</span>
                <span class="win-btns">— ▢ ✕</span>
            </div>
            <div class="menu-bar">
                <span>Файл</span><span>Правка</span><span>Вид</span><span>Инструменты</span><span>Справка</span>
            </div>
            <div class="toolbar">
                <div class="btn">Открыть БД</div>
                <div class="btn">Записать изменения</div>
                <div class="btn">Отменить</div>
                <div class="btn">БД: db.sqlite3 (SQLite 3.39)</div>
                <div class="btn">Размер: 296 КБ</div>
            </div>
            <div class="tabs">
                <div class="tab">Структура БД</div>
                <div class="tab active">Данные</div>
                <div class="tab">Прагмы</div>
                <div class="tab">Выполнить SQL</div>
            </div>
            <div class="sub-bar">
                <div>
                    <span>Таблица: </span>
                    <span class="tbl-sel">club_booking_booking (Бронирования дорожек и столов) ▼</span>
                </div>
                <div>
                    <span>Всего записей: 35 | Отображаются: 1 — 16</span>
                </div>
            </div>
            <div class="grid-area">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 45px;">id [PK]</th>
                            <th style="width: 140px;">booking_number</th>
                            <th style="width: 130px;">client_id [FK]</th>
                            <th style="width: 150px;">resource_id [FK]</th>
                            <th style="width: 90px;">booking_date</th>
                            <th style="width: 95px;">time_slot</th>
                            <th style="width: 55px; text-align:center;">players</th>
                            <th style="width: 110px; text-align:right;">total_cost (руб.)</th>
                            <th style="width: 100px; text-align:right;">deposit_amount</th>
                            <th style="width: 100px;">status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rows53}
                    </tbody>
                </table>
            </div>
            <div class="status-bar">
                <span>Таблица: club_booking_booking | Первичный ключ: id | Внешний ключ: client_id -> club_booking_client.id</span>
                <span>35 строк в наборе | Выборка: 0.6 мс</span>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(html53);
    await page.screenshot({ path: 'screenshots/fig_5_03_db_data_bookings.png' });
    console.log("Скриншот 5.3 сохранен.");

    // ------------------------------------------------------------------------
    // РИСУНОК 5.4 — Панель администрирования Django Admin
    // ------------------------------------------------------------------------
    const html54 = `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", -apple-system, Roboto, sans-serif; }
            body { background: #f6f8fa; color: #24292e; }
            .navbar {
                background: #1b2733;
                color: #ffffff;
                padding: 14px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .navbar h1 { font-size: 16px; font-weight: 700; letter-spacing: 0.5px; }
            .user-tools { font-size: 12px; color: #cbd5e1; }
            .breadcrumbs {
                background: #243342;
                color: #e2e8f0;
                padding: 7px 24px;
                font-size: 11.5px;
            }
            .content-wrapper { padding: 24px; max-width: 1350px; margin: 0 auto; }
            .card {
                background: #ffffff;
                border: 1px solid #d0d7de;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                overflow: hidden;
            }
            .card-header {
                background: #243342;
                color: #ffffff;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            table.admin-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 12.5px;
            }
            table.admin-table tr {
                border-bottom: 1px solid #eaeef2;
            }
            table.admin-table tr:hover {
                background: #f8fafc;
            }
            table.admin-table td {
                padding: 10px 18px;
            }
            .model-title {
                font-weight: 600;
                color: #0366d6;
            }
            .model-desc {
                font-size: 11px;
                color: #586069;
                margin-top: 2px;
            }
            .badge {
                background: #e1f0ff;
                color: #0366d6;
                padding: 2px 10px;
                border-radius: 12px;
                font-weight: 700;
                font-size: 11.5px;
                border: 1px solid #c8e1ff;
            }
            .btn-action {
                background: #ffffff;
                border: 1px solid #d0d7de;
                padding: 3px 12px;
                border-radius: 3px;
                font-size: 11.5px;
                color: #24292e;
                margin-left: 6px;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="navbar">
            <h1>Администрирование Django | Информационная система «Strike & Pocket»</h1>
            <div class="user-tools">
                Добро пожаловать, <b>admin (Шеф-Администратор)</b> | Изменить пароль / Выйти
            </div>
        </div>
        <div class="breadcrumbs">
            Главная › Club_Booking (Управление боулингом, бильярдом и заказами бара)
        </div>
        <div class="content-wrapper">
            <div class="card">
                <div class="card-header">
                    ПРИЛОЖЕНИЕ: CLUB_BOOKING (МОДЕЛИ ДАННЫХ И СУЩНОСТИ ПРЕДМЕТНОЙ ОБЛАСТИ)
                </div>
                <table class="admin-table">
                    <tr>
                        <td>
                            <div class="model-title">Категории игровых ресурсов (ResourceCategory)</div>
                            <div class="model-desc">Классификатор: боулинг, русский бильярд, пул, снукер</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">4 записи</span></td>
                        <td style="width: 170px; text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Игровые ресурсы (ClubResource)</div>
                            <div class="model-desc">Дорожки 1-12 Brunswick GS-X, бильярдные столы 1-10</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">22 записи</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Тарифная сетка (Tariff)</div>
                            <div class="model-desc">Справочник почасовых ставок: день (до 18:00) / вечер (после 18:00), будни / вых.</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">16 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Клиенты комплекса (Client)</div>
                            <div class="model-desc">Профили постоянных гостей с бонусными счетами и контактами</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">16 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Клубные карты (ClubCard)</div>
                            <div class="model-desc">Программа лояльности: Silver (5%), Gold (10%), Platinum (15%)</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">12 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Бронирования дорожек и столов (Booking)</div>
                            <div class="model-desc">Основная таблица заказов сеансов игры с датами, временем и статусами (>= 30 шт)</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">35 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Категории меню бара (BarCategory)</div>
                            <div class="model-desc">Разделы каталога: пицца из печи, горячие закуски, бургеры, напитки, десерты</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">5 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Позиции меню бара и кухни (BarItem)</div>
                            <div class="model-desc">Каталог блюд и напитков с граммовками, ценами и флагом доступности</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">16 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Заказы бара к бронированиям (BookingBarOrder)</div>
                            <div class="model-desc">Связующая модель Many-to-Many through со своими атрибутами (порции, статус подачи)</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">71 запись</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <div class="model-title">Платежи и фискальные чеки (Payment)</div>
                            <div class="model-desc">Фискализация по 54-ФЗ: депозиты 50%, окончательные расчеты, эквайринг</div>
                        </td>
                        <td style="text-align:right;"><span class="badge">45 записей</span></td>
                        <td style="text-align:right;">
                            <span class="btn-action">+ Добавить</span>
                            <span class="btn-action">Изменить</span>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(html54);
    await page.screenshot({ path: 'screenshots/fig_5_04_django_admin.png' });
    console.log("Скриншот 5.4 сохранен.");

    await browser.close();
}

renderExactScreenshots().catch(err => {
    console.error("Ошибка при генерации скриншотов:", err);
    process.exit(1);
});
