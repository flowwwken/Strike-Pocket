import xml.etree.ElementTree as ET

def create_drawio_xml(filename, diagram_name, elements):
    """
    elements: list of dicts:
      type: 'pool', 'lane', 'task', 'gateway', 'event', 'edge'
      id, label, x, y, width, height, parent, source, target
    """
    mxfile = ET.Element('mxfile', host="app.diagrams.net", modified="2024-11-11T12:00:00.000Z", agent="BPMN 2.0 Modeler", version="21.0.0")
    diagram = ET.SubElement(mxfile, 'diagram', id="bpmn_diag", name=diagram_name)
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1422", dy="794", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="827", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')
    
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")
    
    for el in elements:
        cell_id = el['id']
        parent = el.get('parent', '1')
        label = el.get('label', '')
        el_type = el['type']
        
        if el_type == 'pool':
            style = "swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=30;horizontal=0;horizontalStack=0;fillColor=#E8EEF5;strokeColor=#4B6B94;fontStyle=1;fontSize=12;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width=str(el['width']), height=str(el['height']), **{"as": "geometry"})
        elif el_type == 'lane':
            style = "swimlane;html=1;startSize=30;horizontal=0;fillColor=#FFFFFF;strokeColor=#B0C0D0;fontSize=11;fontStyle=1;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width=str(el['width']), height=str(el['height']), **{"as": "geometry"})
        elif el_type == 'task':
            style = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#EDF5FF;strokeColor=#3A7BD5;strokeWidth=2;fontSize=11;align=center;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width=str(el['width']), height=str(el['height']), **{"as": "geometry"})
        elif el_type == 'gateway':
            style = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFDE6;strokeColor=#D4A017;strokeWidth=2;fontSize=10;align=center;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width="40", height="40", **{"as": "geometry"})
        elif el_type == 'start_event':
            style = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#E6FFE6;strokeColor=#2E7D32;strokeWidth=2;fontSize=10;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width="36", height="36", **{"as": "geometry"})
        elif el_type == 'end_event':
            style = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FFE6E6;strokeColor=#C62828;strokeWidth=3;fontSize=10;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width="36", height="36", **{"as": "geometry"})
        elif el_type == 'timer_event':
            style = "ellipse;shape=doubleEllipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FFF8E1;strokeColor=#F57F17;strokeWidth=2;fontSize=10;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, vertex="1", parent=parent)
            geo = ET.SubElement(cell, 'mxGeometry', x=str(el['x']), y=str(el['y']), width="36", height="36", **{"as": "geometry"})
        elif el_type == 'edge':
            style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#333333;strokeWidth=1.5;fontSize=10;"
            cell = ET.SubElement(root, 'mxCell', id=cell_id, value=label, style=style, edge="1", parent=parent, source=el['source'], target=el['target'])
            geo = ET.SubElement(cell, 'mxGeometry', relative="1", **{"as": "geometry"})
            
    tree = ET.ElementTree(mxfile)
    with open(filename, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f"Generated {filename}")

def build_all_drawio():
    # 1. AS IS
    elements_1 = [
        {'id': 'p1', 'type': 'pool', 'label': 'Боулинг-клуб (AS IS)', 'x': 20, 'y': 20, 'width': 1100, 'height': 540},
        {'id': 'l1', 'type': 'lane', 'label': 'Посетитель', 'parent': 'p1', 'x': 30, 'y': 0, 'width': 1070, 'height': 180},
        {'id': 'l2', 'type': 'lane', 'label': 'Оператор зала', 'parent': 'p1', 'x': 30, 'y': 180, 'width': 1070, 'height': 180},
        {'id': 'l3', 'type': 'lane', 'label': 'Кассир', 'parent': 'p1', 'x': 30, 'y': 360, 'width': 1070, 'height': 180},
        
        {'id': 'e1', 'type': 'start_event', 'label': 'Старт', 'parent': 'l1', 'x': 30, 'y': 65},
        {'id': 't1', 'type': 'task', 'label': 'Позвонить в клуб', 'parent': 'l1', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't2', 'type': 'task', 'label': 'Принять звонок', 'parent': 'l2', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't3', 'type': 'task', 'label': 'Проверить журнал', 'parent': 'l2', 'x': 230, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'g1', 'type': 'gateway', 'label': 'Есть места?', 'parent': 'l2', 'x': 370, 'y': 62},
        {'id': 't4', 'type': 'task', 'label': 'Записать в журнал', 'parent': 'l2', 'x': 440, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'tm1', 'type': 'timer_event', 'label': 'Ожидание дня', 'parent': 'l2', 'x': 580, 'y': 64},
        {'id': 't5', 'type': 'task', 'label': 'Прибыть в клуб', 'parent': 'l1', 'x': 640, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't6', 'type': 'task', 'label': 'Уточнить число гостей', 'parent': 'l2', 'x': 640, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'g2', 'type': 'gateway', 'label': '> 6 чел?', 'parent': 'l2', 'x': 780, 'y': 62},
        {'id': 't7', 'type': 'task', 'label': 'Искать вторую дорожку', 'parent': 'l2', 'x': 840, 'y': 20, 'width': 110, 'height': 50},
        {'id': 't8', 'type': 'task', 'label': 'Включить 1 дорожку', 'parent': 'l2', 'x': 840, 'y': 100, 'width': 110, 'height': 50},
        {'id': 't9', 'type': 'task', 'label': 'Отыграть сессию', 'parent': 'l1', 'x': 880, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't10', 'type': 'task', 'label': 'Рассчитать часы стыка', 'parent': 'l3', 'x': 640, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't11', 'type': 'task', 'label': 'Принять оплату', 'parent': 'l3', 'x': 800, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'e2', 'type': 'end_event', 'label': 'Конец', 'parent': 'l3', 'x': 950, 'y': 64},
        
        {'id': 'ed1', 'type': 'edge', 'source': 'e1', 'target': 't1'},
        {'id': 'ed2', 'type': 'edge', 'source': 't1', 'target': 't2'},
        {'id': 'ed3', 'type': 'edge', 'source': 't2', 'target': 't3'},
        {'id': 'ed4', 'type': 'edge', 'source': 't3', 'target': 'g1'},
        {'id': 'ed5', 'type': 'edge', 'source': 'g1', 'target': 't4', 'label': 'Да'},
        {'id': 'ed6', 'type': 'edge', 'source': 't4', 'target': 'tm1'},
        {'id': 'ed7', 'type': 'edge', 'source': 'tm1', 'target': 't6'},
        {'id': 'ed8', 'type': 'edge', 'source': 't5', 'target': 't6'},
        {'id': 'ed9', 'type': 'edge', 'source': 't6', 'target': 'g2'},
        {'id': 'ed10', 'type': 'edge', 'source': 'g2', 'target': 't7', 'label': '>6'},
        {'id': 'ed11', 'type': 'edge', 'source': 'g2', 'target': 't8', 'label': '<=6'},
        {'id': 'ed12', 'type': 'edge', 'source': 't7', 'target': 't9'},
        {'id': 'ed13', 'type': 'edge', 'source': 't8', 'target': 't9'},
        {'id': 'ed14', 'type': 'edge', 'source': 't9', 'target': 't10'},
        {'id': 'ed15', 'type': 'edge', 'source': 't10', 'target': 't11'},
        {'id': 'ed16', 'type': 'edge', 'source': 't11', 'target': 'e2'}
    ]
    create_drawio_xml('diagram_1_as_is.drawio', 'Главный процесс AS IS', elements_1)
    
    # 2. TO BE
    elements_2 = [
        {'id': 'p2', 'type': 'pool', 'label': 'Система боулинга (TO BE)', 'x': 20, 'y': 20, 'width': 1100, 'height': 540},
        {'id': 'l1', 'type': 'lane', 'label': 'Посетитель сайта', 'parent': 'p2', 'x': 30, 'y': 0, 'width': 1070, 'height': 180},
        {'id': 'l2', 'type': 'lane', 'label': 'Сервер Django', 'parent': 'p2', 'x': 30, 'y': 180, 'width': 1070, 'height': 180},
        {'id': 'l3', 'type': 'lane', 'label': 'Оператор зала', 'parent': 'p2', 'x': 30, 'y': 360, 'width': 1070, 'height': 180},
        
        {'id': 'e1', 'type': 'start_event', 'label': 'Старт', 'parent': 'l1', 'x': 30, 'y': 65},
        {'id': 't1', 'type': 'task', 'label': 'Выбрать дату и время', 'parent': 'l1', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't2', 'type': 'task', 'label': 'Проверить слоты (Fetch JSON)', 'parent': 'l2', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't3', 'type': 'task', 'label': 'Указать число гостей', 'parent': 'l1', 'x': 230, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'g1', 'type': 'gateway', 'label': '> 6 гостей?', 'parent': 'l2', 'x': 360, 'y': 62},
        {'id': 't4', 'type': 'task', 'label': 'Потребовать 2 дорожки', 'parent': 'l2', 'x': 420, 'y': 20, 'width': 110, 'height': 50},
        {'id': 't5', 'type': 'task', 'label': 'Выбрать 2 дорожки', 'parent': 'l1', 'x': 550, 'y': 20, 'width': 110, 'height': 50},
        {'id': 't6', 'type': 'task', 'label': 'Выбрать 1 дорожку', 'parent': 'l1', 'x': 550, 'y': 100, 'width': 110, 'height': 50},
        {'id': 't7', 'type': 'task', 'label': 'Рассчитать стык тарифов', 'parent': 'l2', 'x': 680, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't8', 'type': 'task', 'label': 'Транзакция (atomic)', 'parent': 'l2', 'x': 810, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't9', 'type': 'task', 'label': 'Сформировать талон и email', 'parent': 'l2', 'x': 940, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't10', 'type': 'task', 'label': 'Отметить визит в панели', 'parent': 'l3', 'x': 810, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'e2', 'type': 'end_event', 'label': 'Успешно', 'parent': 'l3', 'x': 970, 'y': 64},
        
        {'id': 'ed1', 'type': 'edge', 'source': 'e1', 'target': 't1'},
        {'id': 'ed2', 'type': 'edge', 'source': 't1', 'target': 't2'},
        {'id': 'ed3', 'type': 'edge', 'source': 't2', 'target': 't3'},
        {'id': 'ed4', 'type': 'edge', 'source': 't3', 'target': 'g1'},
        {'id': 'ed5', 'type': 'edge', 'source': 'g1', 'target': 't4', 'label': '>6'},
        {'id': 'ed6', 'type': 'edge', 'source': 'g1', 'target': 't6', 'label': '<=6'},
        {'id': 'ed7', 'type': 'edge', 'source': 't4', 'target': 't5'},
        {'id': 'ed8', 'type': 'edge', 'source': 't5', 'target': 't7'},
        {'id': 'ed9', 'type': 'edge', 'source': 't6', 'target': 't7'},
        {'id': 'ed10', 'type': 'edge', 'source': 't7', 'target': 't8'},
        {'id': 'ed11', 'type': 'edge', 'source': 't8', 'target': 't9'},
        {'id': 'ed12', 'type': 'edge', 'source': 't9', 'target': 't10'},
        {'id': 'ed13', 'type': 'edge', 'source': 't10', 'target': 'e2'}
    ]
    create_drawio_xml('diagram_2_to_be.drawio', 'Главный процесс TO BE', elements_2)
    
    # 3. Bar Preorder
    elements_3 = [
        {'id': 'p3', 'type': 'pool', 'label': 'Предзаказ бара', 'x': 20, 'y': 20, 'width': 1100, 'height': 540},
        {'id': 'l1', 'type': 'lane', 'label': 'Посетитель', 'parent': 'p3', 'x': 30, 'y': 0, 'width': 1070, 'height': 180},
        {'id': 'l2', 'type': 'lane', 'label': 'Сервер Django', 'parent': 'p3', 'x': 30, 'y': 180, 'width': 1070, 'height': 180},
        {'id': 'l3', 'type': 'lane', 'label': 'Кухня / Бар', 'parent': 'p3', 'x': 30, 'y': 360, 'width': 1070, 'height': 180},
        
        {'id': 'e1', 'type': 'start_event', 'label': 'Старт', 'parent': 'l1', 'x': 30, 'y': 65},
        {'id': 't1', 'type': 'task', 'label': 'Открыть меню бара', 'parent': 'l1', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't2', 'type': 'task', 'label': 'Выбрать блюда и напитки', 'parent': 'l1', 'x': 230, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't3', 'type': 'task', 'label': 'Проверить остатки блюд', 'parent': 'l2', 'x': 230, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'g1', 'type': 'gateway', 'label': 'В наличии?', 'parent': 'l2', 'x': 370, 'y': 62},
        {'id': 't4', 'type': 'task', 'label': 'Рассчитать сумму заказа', 'parent': 'l2', 'x': 440, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't5', 'type': 'task', 'label': 'Сохранить PreOrderItem', 'parent': 'l2', 'x': 580, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't6', 'type': 'task', 'label': 'Сформировать лист кухни', 'parent': 'l2', 'x': 720, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'tm1', 'type': 'timer_event', 'label': 'За 15 мин до игры', 'parent': 'l3', 'x': 750, 'y': 64},
        {'id': 't7', 'type': 'task', 'label': 'Приготовить блюда', 'parent': 'l3', 'x': 820, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't8', 'type': 'task', 'label': 'Подать к дорожке', 'parent': 'l3', 'x': 950, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'e2', 'type': 'end_event', 'label': 'Выдано', 'parent': 'l3', 'x': 1080, 'y': 64},
        
        {'id': 'ed1', 'type': 'edge', 'source': 'e1', 'target': 't1'},
        {'id': 'ed2', 'type': 'edge', 'source': 't1', 'target': 't2'},
        {'id': 'ed3', 'type': 'edge', 'source': 't2', 'target': 't3'},
        {'id': 'ed4', 'type': 'edge', 'source': 't3', 'target': 'g1'},
        {'id': 'ed5', 'type': 'edge', 'source': 'g1', 'target': 't4', 'label': 'Да'},
        {'id': 'ed6', 'type': 'edge', 'source': 't4', 'target': 't5'},
        {'id': 'ed7', 'type': 'edge', 'source': 't5', 'target': 't6'},
        {'id': 'ed8', 'type': 'edge', 'source': 't6', 'target': 'tm1'},
        {'id': 'ed9', 'type': 'edge', 'source': 'tm1', 'target': 't7'},
        {'id': 'ed10', 'type': 'edge', 'source': 't7', 'target': 't8'},
        {'id': 'ed11', 'type': 'edge', 'source': 't8', 'target': 'e2'}
    ]
    create_drawio_xml('diagram_3_bar_preorder.drawio', 'Процесс 2 Предзаказ бара', elements_3)
    
    # 4. Club Card
    elements_4 = [
        {'id': 'p4', 'type': 'pool', 'label': 'Программа лояльности', 'x': 20, 'y': 20, 'width': 1100, 'height': 540},
        {'id': 'l1', 'type': 'lane', 'label': 'Посетитель', 'parent': 'p4', 'x': 30, 'y': 0, 'width': 1070, 'height': 180},
        {'id': 'l2', 'type': 'lane', 'label': 'Сервер Django', 'parent': 'p4', 'x': 30, 'y': 180, 'width': 1070, 'height': 180},
        {'id': 'l3', 'type': 'lane', 'label': 'Администратор', 'parent': 'p4', 'x': 30, 'y': 360, 'width': 1070, 'height': 180},
        
        {'id': 'e1', 'type': 'start_event', 'label': 'Старт', 'parent': 'l1', 'x': 30, 'y': 65},
        {'id': 't1', 'type': 'task', 'label': 'Ввести номер карты', 'parent': 'l1', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't2', 'type': 'task', 'label': 'Проверить карту в БД', 'parent': 'l2', 'x': 90, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'g1', 'type': 'gateway', 'label': 'Активна?', 'parent': 'l2', 'x': 240, 'y': 62},
        {'id': 't3', 'type': 'task', 'label': 'Определить % скидки', 'parent': 'l2', 'x': 310, 'y': 55, 'width': 110, 'height': 55},
        {'id': 't4', 'type': 'task', 'label': 'Вычесть скидку из цены', 'parent': 'l2', 'x': 450, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'tm1', 'type': 'timer_event', 'label': 'Оплата сессии', 'parent': 'l2', 'x': 590, 'y': 64},
        {'id': 't5', 'type': 'task', 'label': 'Обновить сумму расходов', 'parent': 'l2', 'x': 660, 'y': 55, 'width': 110, 'height': 55},
        {'id': 'g2', 'type': 'gateway', 'label': 'Повысить %?', 'parent': 'l2', 'x': 800, 'y': 62},
        {'id': 't6', 'type': 'task', 'label': 'Повысить уровень карты', 'parent': 'l2', 'x': 870, 'y': 20, 'width': 110, 'height': 50},
        {'id': 't7', 'type': 'task', 'label': 'Сохранить статус', 'parent': 'l2', 'x': 870, 'y': 100, 'width': 110, 'height': 50},
        {'id': 'e2', 'type': 'end_event', 'label': 'Завершено', 'parent': 'l2', 'x': 1020, 'y': 64},
        
        {'id': 'ed1', 'type': 'edge', 'source': 'e1', 'target': 't1'},
        {'id': 'ed2', 'type': 'edge', 'source': 't1', 'target': 't2'},
        {'id': 'ed3', 'type': 'edge', 'source': 't2', 'target': 'g1'},
        {'id': 'ed4', 'type': 'edge', 'source': 'g1', 'target': 't3', 'label': 'Да'},
        {'id': 'ed5', 'type': 'edge', 'source': 't3', 'target': 't4'},
        {'id': 'ed6', 'type': 'edge', 'source': 't4', 'target': 'tm1'},
        {'id': 'ed7', 'type': 'edge', 'source': 'tm1', 'target': 't5'},
        {'id': 'ed8', 'type': 'edge', 'source': 't5', 'target': 'g2'},
        {'id': 'ed9', 'type': 'edge', 'source': 'g2', 'target': 't6', 'label': 'Да'},
        {'id': 'ed10', 'type': 'edge', 'source': 'g2', 'target': 't7', 'label': 'Нет'},
        {'id': 'ed11', 'type': 'edge', 'source': 't6', 'target': 'e2'},
        {'id': 'ed12', 'type': 'edge', 'source': 't7', 'target': 'e2'}
    ]
    create_drawio_xml('diagram_4_club_card.drawio', 'Процесс 3 Клубные карты', elements_4)

if __name__ == '__main__':
    build_all_drawio()
