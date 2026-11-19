const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function renderERDiagram() {
    const tmpDir = path.join(__dirname, 'chrome_tmp_er_' + Date.now());
    if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });

    const browser = await puppeteer.launch({
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: 'new',
        userDataDir: tmpDir,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-crash-reporter', '--no-first-run', '--disable-extensions']
    });

    const page = await browser.newPage();
    // Высокое разрешение для диаграммы формата А4/А3 альбомная
    await page.setViewport({ width: 1600, height: 1100, deviceScaleFactor: 2 });

    const html = `
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
                background-color: #ffffff;
                color: #222222;
                padding: 24px;
                width: 1600px;
                height: 1100px;
                position: relative;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
                border-bottom: 2px solid #333333;
                padding-bottom: 12px;
            }
            .header h1 {
                font-size: 20px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                color: #111111;
            }
            .header p {
                font-size: 13px;
                color: #555555;
                margin-top: 4px;
            }
            .diagram-container {
                position: relative;
                width: 1550px;
                height: 980px;
                background: #fafbfc;
                border: 1px solid #d0d7de;
                border-radius: 6px;
            }
            /* SVG для линий связей */
            svg.connections {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1;
            }
            /* Сущности таблицы */
            .entity-card {
                position: absolute;
                background: #ffffff;
                border: 1.5px solid #24292f;
                border-radius: 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.06);
                z-index: 2;
                width: 270px;
                font-size: 11px;
            }
            .entity-card.wide {
                width: 290px;
            }
            .entity-header {
                background: #24292f;
                color: #ffffff;
                padding: 6px 10px;
                font-weight: 700;
                font-size: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top-left-radius: 2px;
                border-top-right-radius: 2px;
            }
            .entity-header span.ru-name {
                font-weight: normal;
                font-size: 11px;
                opacity: 0.85;
            }
            .attribute-list {
                padding: 4px 0;
            }
            .attr-row {
                display: flex;
                padding: 2.5px 8px;
                border-bottom: 1px solid #f0f2f5;
                align-items: center;
            }
            .attr-row:last-child {
                border-bottom: none;
            }
            .attr-key {
                width: 26px;
                font-weight: bold;
                font-size: 10px;
                color: #cf222e;
            }
            .attr-key.fk {
                color: #0969da;
            }
            .attr-key.pfk {
                color: #8250df;
            }
            .attr-name {
                flex: 1;
                font-weight: 600;
                color: #1f2328;
            }
            .attr-type {
                color: #656d76;
                font-family: Consolas, monospace;
                font-size: 10px;
            }
            .legend-box {
                position: absolute;
                bottom: 15px;
                right: 20px;
                background: #ffffff;
                border: 1px solid #d0d7de;
                border-radius: 4px;
                padding: 10px 14px;
                font-size: 11px;
                z-index: 10;
                box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            }
            .legend-box h4 {
                font-size: 11px;
                margin-bottom: 6px;
                text-transform: uppercase;
                color: #24292f;
            }
            .legend-item {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 4px;
            }
            .leg-symbol {
                font-weight: bold;
                font-size: 11px;
                display: inline-block;
                width: 32px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Логическая ER-модель базы данных развлекательного комплекса «Strike & Pocket»</h1>
            <p>Нотация «вороньей лапки» (Crow's Foot Notation) | 3-я нормальная форма (3NF) | Вариант 4</p>
        </div>

        <div class="diagram-container">
            <!-- SVG СВЯЗИ CROW'S FOOT -->
            <svg class="connections" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <!-- Маркер вороньей лапки (многие) -->
                    <marker id="crow" viewBox="0 0 15 15" refX="14" refY="7.5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
                        <path d="M 0 0 L 15 7.5 L 0 15 M 15 7.5 L 0 7.5" fill="none" stroke="#24292f" stroke-width="1.8" />
                    </marker>
                    <!-- Маркер один (две черточки) -->
                    <marker id="one" viewBox="0 0 15 15" refX="1" refY="7.5" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
                        <line x1="6" y1="1" x2="6" y2="14" stroke="#24292f" stroke-width="2" />
                        <line x1="11" y1="1" x2="11" y2="14" stroke="#24292f" stroke-width="2" />
                    </marker>
                    <!-- Маркер ноль или один (нолик и черточка) -->
                    <marker id="zero-one" viewBox="0 0 20 15" refX="1" refY="7.5" markerWidth="12" markerHeight="10" orient="auto-start-reverse">
                        <circle cx="6" cy="7.5" r="4.5" fill="#ffffff" stroke="#24292f" stroke-width="1.8" />
                        <line x1="14" y1="1" x2="14" y2="14" stroke="#24292f" stroke-width="2" />
                    </marker>
                </defs>

                <!-- 1. Client (300, 70) -> ClubCard (50, 70) -->
                <!-- Client (1,1) -> ClubCard (0,N) -->
                <path d="M 320 120 L 260 120" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="275" y="112" font-size="10" fill="#444" font-family="sans-serif">1 : 0..N</text>

                <!-- 2. Client (450, 270) -> Booking (450, 360) -->
                <path d="M 450 260 L 450 360" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="455" y="310" font-size="10" fill="#444" font-family="sans-serif">1 : 0..N</text>

                <!-- 3. ResourceCategory (890, 70) -> ClubResource (890, 250) -->
                <path d="M 890 200 L 890 250" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="895" y="230" font-size="10" fill="#444" font-family="sans-serif">1 : 1..N</text>

                <!-- 4. ResourceCategory (1020, 110) -> Tariff (1230, 110) -->
                <path d="M 1030 110 L 1230 110" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="1115" y="102" font-size="10" fill="#444" font-family="sans-serif">1 : 1..N</text>

                <!-- 5. ClubResource (760, 360) -> Booking (590, 460) -->
                <path d="M 760 360 L 675 360 L 675 460 L 590 460" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="682" y="415" font-size="10" fill="#444" font-family="sans-serif">1 : 0..N</text>

                <!-- 6. Booking (450, 780) -> Payment (450, 840) -->
                <path d="M 450 780 L 450 830" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="455" y="810" font-size="10" fill="#444" font-family="sans-serif">1 : 0..N</text>

                <!-- 7. Booking (590, 560) -> BookingBarOrder (780, 560) -->
                <path d="M 590 560 L 780 560" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="670" y="552" font-size="10" fill="#444" font-family="sans-serif">1 : 0..N</text>

                <!-- 8. BarItem (1230, 560) -> BookingBarOrder (1050, 560) -->
                <path d="M 1230 560 L 1050 560" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="1120" y="552" font-size="10" fill="#444" font-family="sans-serif">1 : 0..N</text>

                <!-- 9. BarCategory (1360, 400) -> BarItem (1360, 470) -->
                <path d="M 1360 400 L 1360 470" fill="none" stroke="#24292f" stroke-width="1.8" marker-start="url(#one)" marker-end="url(#crow)" />
                <text x="1368" y="435" font-size="10" fill="#444" font-family="sans-serif">1 : 1..N</text>
            </svg>

            <!-- 1. CLUB_CARD -->
            <div class="entity-card" style="top: 40px; left: 20px; width: 240px;">
                <div class="entity-header">
                    <span>CLUB_CARD</span>
                    <span class="ru-name">Клубная карта</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">client_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">card_number</span><span class="attr-type">VARCHAR(20) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">card_tier</span><span class="attr-type">VARCHAR(15)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">discount_percent</span><span class="attr-type">DECIMAL(4,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">issued_at</span><span class="attr-type">DATE</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">expires_at</span><span class="attr-type">DATE [NULL]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">is_active</span><span class="attr-type">BOOLEAN</span></div>
                </div>
            </div>

            <!-- 2. CLIENT -->
            <div class="entity-card" style="top: 40px; left: 320px; width: 260px;">
                <div class="entity-header">
                    <span>CLIENT</span>
                    <span class="ru-name">Клиент комплекса</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">last_name</span><span class="attr-type">VARCHAR(50)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">first_name</span><span class="attr-type">VARCHAR(50)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">patronymic</span><span class="attr-type">VARCHAR(50) [NULL]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">phone</span><span class="attr-type">VARCHAR(20) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">email</span><span class="attr-type">VARCHAR(254) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">bonus_balance</span><span class="attr-type">DECIMAL(8,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">is_active</span><span class="attr-type">BOOLEAN</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">created_at</span><span class="attr-type">DATETIME</span></div>
                </div>
            </div>

            <!-- 3. RESOURCE_CATEGORY -->
            <div class="entity-card" style="top: 40px; left: 760px; width: 270px;">
                <div class="entity-header">
                    <span>RESOURCE_CATEGORY</span>
                    <span class="ru-name">Категория зала</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">code</span><span class="attr-type">VARCHAR(30) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">name</span><span class="attr-type">VARCHAR(100)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">description</span><span class="attr-type">TEXT</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">min_players</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">max_players</span><span class="attr-type">INTEGER</span></div>
                </div>
            </div>

            <!-- 4. TARIFF -->
            <div class="entity-card" style="top: 40px; left: 1230px; width: 260px;">
                <div class="entity-header">
                    <span>TARIFF</span>
                    <span class="ru-name">Тарифная сетка</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">category_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">day_type</span><span class="attr-type">VARCHAR(10)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">time_slot</span><span class="attr-type">VARCHAR(10)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">price_per_hour</span><span class="attr-type">DECIMAL(8,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">is_active</span><span class="attr-type">BOOLEAN</span></div>
                </div>
            </div>

            <!-- 5. CLUB_RESOURCE -->
            <div class="entity-card" style="top: 250px; left: 760px; width: 270px;">
                <div class="entity-header">
                    <span>CLUB_RESOURCE</span>
                    <span class="ru-name">Игровой ресурс</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">category_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">resource_number</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">title</span><span class="attr-type">VARCHAR(100)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">equipment_brand</span><span class="attr-type">VARCHAR(100)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">status</span><span class="attr-type">VARCHAR(20)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">max_capacity</span><span class="attr-type">INTEGER</span></div>
                </div>
            </div>

            <!-- 6. BOOKING -->
            <div class="entity-card wide" style="top: 360px; left: 300px; width: 290px;">
                <div class="entity-header">
                    <span>BOOKING</span>
                    <span class="ru-name">Бронирование (Основная)</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">booking_number</span><span class="attr-type">VARCHAR(30) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">client_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">resource_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">booking_date</span><span class="attr-type">DATE</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">time_start</span><span class="attr-type">TIME</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">time_end</span><span class="attr-type">TIME</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">duration_hours</span><span class="attr-type">DECIMAL(4,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">players_count</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">rental_cost</span><span class="attr-type">DECIMAL(9,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">discount_amount</span><span class="attr-type">DECIMAL(8,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">total_cost</span><span class="attr-type">DECIMAL(9,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">deposit_amount</span><span class="attr-type">DECIMAL(8,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">status</span><span class="attr-type">VARCHAR(20)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">notes</span><span class="attr-type">TEXT [NULL]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">created_at</span><span class="attr-type">DATETIME</span></div>
                </div>
            </div>

            <!-- 7. PAYMENT -->
            <div class="entity-card wide" style="top: 830px; left: 300px; width: 290px;">
                <div class="entity-header">
                    <span>PAYMENT</span>
                    <span class="ru-name">Платеж (54-ФЗ)</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">booking_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">transaction_id</span><span class="attr-type">VARCHAR(50) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">payment_type</span><span class="attr-type">VARCHAR(20)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">payment_method</span><span class="attr-type">VARCHAR(20)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">amount</span><span class="attr-type">DECIMAL(9,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">fiscal_receipt_number</span><span class="attr-type">VARCHAR(50) [NULL]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">status</span><span class="attr-type">VARCHAR(20)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">created_at</span><span class="attr-type">DATETIME</span></div>
                </div>
            </div>

            <!-- 8. BOOKING_BAR_ORDER (Through M:M) -->
            <div class="entity-card" style="top: 480px; left: 780px; width: 270px; border: 2px solid #0969da;">
                <div class="entity-header" style="background: #0969da;">
                    <span>BOOKING_BAR_ORDER</span>
                    <span class="ru-name">M:M Заказ бара</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key pfk">FK</span><span class="attr-name">booking_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key pfk">FK</span><span class="attr-name">bar_item_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">quantity</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">price_at_order</span><span class="attr-type">DECIMAL(7,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">status</span><span class="attr-type">VARCHAR(20)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">ordered_at</span><span class="attr-type">DATETIME</span></div>
                </div>
            </div>

            <!-- 9. BAR_CATEGORY -->
            <div class="entity-card" style="top: 250px; left: 1230px; width: 260px;">
                <div class="entity-header">
                    <span>BAR_CATEGORY</span>
                    <span class="ru-name">Категория меню</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">name</span><span class="attr-type">VARCHAR(100) [UQ]</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">description</span><span class="attr-type">TEXT</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">order_priority</span><span class="attr-type">INTEGER</span></div>
                </div>
            </div>

            <!-- 10. BAR_ITEM -->
            <div class="entity-card" style="top: 470px; left: 1230px; width: 260px;">
                <div class="entity-header">
                    <span>BAR_ITEM</span>
                    <span class="ru-name">Позиция меню бара</span>
                </div>
                <div class="attribute-list">
                    <div class="attr-row"><span class="attr-key">PK</span><span class="attr-name">id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key fk">FK</span><span class="attr-name">category_id</span><span class="attr-type">INTEGER</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">name</span><span class="attr-type">VARCHAR(120)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">portion_size</span><span class="attr-type">VARCHAR(50)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">price</span><span class="attr-type">DECIMAL(7,2)</span></div>
                    <div class="attr-row"><span class="attr-key"></span><span class="attr-name">is_available</span><span class="attr-type">BOOLEAN</span></div>
                </div>
            </div>

            <!-- ЛЕГЕНДА ДИАГРАММЫ -->
            <div class="legend-box">
                <h4>Обозначения нотации:</h4>
                <div class="legend-item"><span class="leg-symbol" style="color:#cf222e;">PK</span><span>Первичный ключ (Primary Key)</span></div>
                <div class="legend-item"><span class="leg-symbol" style="color:#0969da;">FK</span><span>Внешний ключ (Foreign Key)</span></div>
                <div class="legend-item"><span class="leg-symbol">||</span><span>Кардинальность: Ровно один (1)</span></div>
                <div class="legend-item"><span class="leg-symbol">&gt;&lt;</span><span>Кардинальность: Многие (0..N / 1..N)</span></div>
                <div class="legend-item"><span class="leg-symbol" style="color:#0969da; border:1px solid #0969da; padding:0 2px; font-size:9px;">M:M</span><span>Связующая таблица (Associative Table)</span></div>
            </div>
        </div>
    </body>
    </html>
    `;

    await page.setContent(html);
    await page.screenshot({
        path: 'er_diagram_variant_4.png',
        fullPage: false,
        clip: { x: 0, y: 0, width: 1600, height: 1100 }
    });

    console.log("ER-диаграмма успешно сохранена в er_diagram_variant_4.png");
    await browser.close();
}

renderERDiagram().catch(err => {
    console.error("Ошибка при рендере ER-диаграммы:", err);
    process.exit(1);
});
