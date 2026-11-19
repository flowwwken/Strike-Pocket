"""
Скрипт генерации er_diagram_variant_4.drawio в формате draw.io (mxGraph XML)
Студент: Верин Вадим Сергеевич, гр. ИСдо-45.
"""

import xml.etree.ElementTree as ET

def generate_er_drawio(filename="er_diagram_variant_4.drawio"):
    mxfile = ET.Element('mxfile', host="app.diagrams.net", modified="2026-11-15T12:00:00.000Z", agent="Antigravity ER Modeler", version="21.0.0")
    diagram = ET.SubElement(mxfile, 'diagram', id="ER_Diagram_StrikePocket", name="ERD Strike & Pocket")
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1600", dy="1100", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1654", pageHeight="1169", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')

    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    # Стили
    entity_style = "shape=swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;html=1;whiteSpace=wrap;swimlaneFillColor=#FFFFFF;fillColor=#24292F;fontColor=#FFFFFF;strokeColor=#24292F;rounded=1;arcSize=4;"
    through_entity_style = "shape=swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;html=1;whiteSpace=wrap;swimlaneFillColor=#FFFFFF;fillColor=#0969DA;fontColor=#FFFFFF;strokeColor=#0969DA;rounded=1;arcSize=4;"
    row_style = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;fontSize=10;fontColor=#24292F;strokeBottom=1;strokeColor=#E1E4E8;"
    
    edge_style = "edgeStyle=orthogonalEdgeStyle;fontSize=10;html=1;endArrow=ERmany;startArrow=ERone;strokeColor=#24292F;strokeWidth=1.5;rounded=0;"

    entities = [
        {
            "id": "e_client",
            "name": "CLIENT (Клиент)",
            "x": 340, "y": 40, "width": 260, "height": 220,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "  last_name: VARCHAR(50)",
                "  first_name: VARCHAR(50)",
                "  patronymic: VARCHAR(50) [NULL]",
                "  phone: VARCHAR(20) [UQ]",
                "  email: VARCHAR(254) [UQ]",
                "  bonus_balance: DECIMAL(8,2)",
                "  is_active: BOOLEAN",
                "  created_at: DATETIME"
            ]
        },
        {
            "id": "e_clubcard",
            "name": "CLUB_CARD (Клубная карта)",
            "x": 40, "y": 40, "width": 240, "height": 200,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "# client_id: INTEGER [FK]",
                "  card_number: VARCHAR(20) [UQ]",
                "  card_tier: VARCHAR(15)",
                "  discount_percent: DECIMAL(4,2)",
                "  issued_at: DATE",
                "  expires_at: DATE [NULL]",
                "  is_active: BOOLEAN"
            ]
        },
        {
            "id": "e_resource_category",
            "name": "RESOURCE_CATEGORY (Категория зала)",
            "x": 760, "y": 40, "width": 270, "height": 160,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "  code: VARCHAR(30) [UQ]",
                "  name: VARCHAR(100)",
                "  description: TEXT",
                "  min_players: INTEGER",
                "  max_players: INTEGER"
            ]
        },
        {
            "id": "e_tariff",
            "name": "TARIFF (Тарифная сетка)",
            "x": 1230, "y": 40, "width": 260, "height": 160,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "# category_id: INTEGER [FK]",
                "  day_type: VARCHAR(10)",
                "  time_slot: VARCHAR(10)",
                "  price_per_hour: DECIMAL(8,2)",
                "  is_active: BOOLEAN"
            ]
        },
        {
            "id": "e_club_resource",
            "name": "CLUB_RESOURCE (Игровой ресурс)",
            "x": 760, "y": 250, "width": 270, "height": 180,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "# category_id: INTEGER [FK]",
                "  resource_number: INTEGER",
                "  title: VARCHAR(100)",
                "  equipment_brand: VARCHAR(100)",
                "  status: VARCHAR(20)",
                "  max_capacity: INTEGER"
            ]
        },
        {
            "id": "e_booking",
            "name": "BOOKING (Бронирование)",
            "x": 320, "y": 340, "width": 290, "height": 360,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "  booking_number: VARCHAR(30) [UQ]",
                "# client_id: INTEGER [FK]",
                "# resource_id: INTEGER [FK]",
                "  booking_date: DATE",
                "  time_start: TIME",
                "  time_end: TIME",
                "  duration_hours: DECIMAL(4,2)",
                "  players_count: INTEGER",
                "  rental_cost: DECIMAL(9,2)",
                "  discount_amount: DECIMAL(8,2)",
                "  total_cost: DECIMAL(9,2)",
                "  deposit_amount: DECIMAL(8,2)",
                "  status: VARCHAR(20)",
                "  notes: TEXT [NULL]",
                "  created_at: DATETIME"
            ]
        },
        {
            "id": "e_payment",
            "name": "PAYMENT (Фискальный платеж)",
            "x": 320, "y": 790, "width": 290, "height": 220,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "# booking_id: INTEGER [FK]",
                "  transaction_id: VARCHAR(50) [UQ]",
                "  payment_type: VARCHAR(20)",
                "  payment_method: VARCHAR(20)",
                "  amount: DECIMAL(9,2)",
                "  fiscal_receipt_number: VARCHAR(50) [NULL]",
                "  status: VARCHAR(20)",
                "  created_at: DATETIME"
            ]
        },
        {
            "id": "e_booking_bar_order",
            "name": "BOOKING_BAR_ORDER (Заказ бара M:M)",
            "x": 760, "y": 480, "width": 280, "height": 180,
            "style": through_entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "# booking_id: INTEGER [FK]",
                "# bar_item_id: INTEGER [FK]",
                "  quantity: INTEGER",
                "  price_at_order: DECIMAL(7,2)",
                "  status: VARCHAR(20)",
                "  ordered_at: DATETIME"
            ]
        },
        {
            "id": "e_bar_category",
            "name": "BAR_CATEGORY (Категория меню)",
            "x": 1230, "y": 250, "width": 260, "height": 140,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "  name: VARCHAR(100) [UQ]",
                "  description: TEXT",
                "  order_priority: INTEGER"
            ]
        },
        {
            "id": "e_bar_item",
            "name": "BAR_ITEM (Позиция меню бара)",
            "x": 1230, "y": 470, "width": 260, "height": 180,
            "style": entity_style,
            "attrs": [
                "+ id: INTEGER [PK]",
                "# category_id: INTEGER [FK]",
                "  name: VARCHAR(120)",
                "  portion_size: VARCHAR(50)",
                "  price: DECIMAL(7,2)",
                "  is_available: BOOLEAN"
            ]
        }
    ]

    for ent in entities:
        c_id = ent['id']
        cell = ET.SubElement(root, 'mxCell', id=c_id, value=ent['name'], style=ent['style'], vertex="1", parent="1")
        ET.SubElement(cell, 'mxGeometry', x=str(ent['x']), y=str(ent['y']), width=str(ent['width']), height=str(ent['height']), **{"as": "geometry"})
        
        for idx, attr in enumerate(ent['attrs']):
            row_id = f"{c_id}_attr_{idx}"
            rcell = ET.SubElement(root, 'mxCell', id=row_id, value=attr, style=row_style, vertex="1", parent=c_id)
            ET.SubElement(rcell, 'mxGeometry', y=str(26 + idx * 20), width=str(ent['width']), height="20", **{"as": "geometry"})

    # Связи (edges)
    connections = [
        ("edge_1", "e_client", "e_clubcard", "1 : 0..N (выдача карт)"),
        ("edge_2", "e_client", "e_booking", "1 : 0..N (оформление брони)"),
        ("edge_3", "e_resource_category", "e_club_resource", "1 : 1..N (оборудование)"),
        ("edge_4", "e_resource_category", "e_tariff", "1 : 1..N (сетка тарифов)"),
        ("edge_5", "e_club_resource", "e_booking", "1 : 0..N (аренда дорожек/столов)"),
        ("edge_6", "e_booking", "e_payment", "1 : 0..N (фискальные чеки 54-ФЗ)"),
        ("edge_7", "e_booking", "e_booking_bar_order", "1 : 0..N (предзаказ кухни)"),
        ("edge_8", "e_bar_item", "e_booking_bar_order", "1 : 0..N (включение блюда в заказ)"),
        ("edge_9", "e_bar_category", "e_bar_item", "1 : 1..N (позиции категории)")
    ]

    for edge_id, src, tgt, label in connections:
        edge = ET.SubElement(root, 'mxCell', id=edge_id, value=label, style=edge_style, edge="1", parent="1", source=src, target=tgt)
        ET.SubElement(edge, 'mxGeometry', relative="1", **{"as": "geometry"})

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"Файл {filename} успешно сгенерирован!")

if __name__ == '__main__':
    generate_er_drawio()
