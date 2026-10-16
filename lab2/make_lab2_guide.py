import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

sys.path.insert(0, os.path.abspath("."))
from tools.report_builder import convert_docx_to_pdf

def build_conspect():
    doc = Document()

    # Поля страницы 1.8 см со всех сторон
    for section in doc.sections:
        section.top_margin = Inches(0.72)
        section.bottom_margin = Inches(0.72)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Цветовая палитра (без эмодзи)
    COLOR_PRIMARY = RGBColor(19, 78, 74)       # Темно-бирюзовый (MongoDB)
    COLOR_SECONDARY = RGBColor(13, 148, 136)   # Бирюзовый акцент
    COLOR_DARK = RGBColor(30, 41, 59)          # Основной текст
    COLOR_MUTED = RGBColor(100, 116, 139)      # Приглушенный серый
    COLOR_CALLOUT_BG = "F0FDFA"
    COLOR_CALLOUT_BORDER = "0D9488"
    COLOR_TRAP_BG = "FEF2F2"
    COLOR_TRAP_BORDER = "DC2626"
    COLOR_CODE_BG = "F8FAFC"
    COLOR_CODE_BORDER = "0284C7"

    # Базовый стиль шрифта Calibri 11pt, интервал 1.15
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_DARK
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="none"/>'
            f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(14)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = COLOR_MUTED

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(13.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        run = p.add_run(text)
        run.font.italic = italic
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_PRIMARY
        p.add_run(text)
        return p

    def add_callout(title, text, is_trap=False):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(6.75)
        bg = COLOR_TRAP_BG if is_trap else COLOR_CALLOUT_BG
        border_col = COLOR_TRAP_BORDER if is_trap else COLOR_CALLOUT_BORDER
        set_cell_background(cell, bg)
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_col}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_title = p.add_run(title + "\n")
        r_title.font.bold = True
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(185, 28, 28) if is_trap else COLOR_PRIMARY

        r_text = p.add_run(text)
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = COLOR_DARK

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(3)

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.cell(0, 0)
        cell.width = Inches(6.75)
        set_cell_background(cell, COLOR_CODE_BG)
        set_cell_margins(cell, top=80, bottom=80, left=140, right=140)

        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="{COLOR_CODE_BORDER}"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text.strip())
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 41, 59)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(3)

    def add_image_box(img_path, caption=None, width_in=5.6):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(2)
            p.add_run().add_picture(img_path, width=Inches(width_in))
            if caption:
                pc = doc.add_paragraph()
                pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pc.paragraph_format.space_after = Pt(6)
                rc = pc.add_run(caption)
                rc.font.size = Pt(9.5)
                rc.font.italic = True
                rc.font.color.rgb = COLOR_MUTED

    # ==================== ТЕКСТ КОНСПЕКТА ====================

    add_title("Полный конспект-гайд для сдачи Лабораторной работы №2")
    add_subtitle(
        "Дисциплина: Нереляционные и распределенные базы данных (nosql_db)\n"
        "Преподаватель: ас. Жишкович Андрей Владимирович | Тема: Инсталляция и основы работы с MongoDB\n"
        "Студент: Абдулханов Абдул-Рахим (ФеП-33) | Львов-2026"
    )

    # ---------------- РАЗДЕЛ 1 ----------------
    add_h1("1. Главный смысл и общая картина лабораторной работы (Big Picture)")
    add_p(
        "Зачем вообще нужна эта лабораторная работа: это фундамент и мостик перехода от реляционных баз данных (SQL) "
        "к документо-ориентированному подходу NoSQL. В традиционном SQL любая сущность дробится на плоские таблицы и строки, "
        "а потом долго и дорого соединяется через JOIN. В MongoDB одна сущность (товар, клиент, заказ) хранится целиком как "
        "одна законченная папка-карточка в формате JSON/BSON. Лабораторная работа №2 посвящена тому, чтобы развернуть инструменты "
        "и научиться правильно мыслить такими документами, не пытаясь строить привычные таблицы."
    )
    add_p("Вся работа строго соответствует 4 этапам методички:")
    add_bullet("Этап 1 (Ознакомление): изучение документо-ориентированной модели, архитектуры MongoDB и формата JSON по лекциям преподавателя.", "1. ")
    add_bullet("Этап 2 (Инсталляция): установка сервера mongod, консольного шелла mongosh и графического интерфейса Compass. Настройка системной переменной PATH и проверка версии 'mongosh --version' в командной строке.", "2. ")
    add_bullet("Этап 3 (Работа с открытыми данными): скачивание реального открытого набора данных Нобелевского комитета (nobel_prizes.json) и анализ его древовидной структуры через онлайн-валидатор.", "3. ")
    add_bullet("Этап 4 (Собственное проектирование и валидация): выбор предметной области магазина TechStore, проектирование двух коллекций (products и orders), составление 6 документов с обязательными массивами и вложенными документами и проверка синтаксиса каждого документа в валидаторе.", "4. ")

    add_callout(
        "Формулировка ответа на защите на вопрос «Что было сделано в лабе?»: ",
        "«Лабораторна робота №2 є ввідною. Я встановив повний локальний стек MongoDB (сервер mongod, консоль mongosh та клієнт Compass), "
        "налаштував системний PATH і перевірив версію. Дослідив структуру реального ієрархічного файлу Nobel Prize. Спроєктував дві колекції "
        "для інтернет-магазину TechStore: каталог товарів з масивами тегів і вкладеними характеристиками та журнал замовлень з вкладеною доставкою. "
        "Виконав синтаксичну валідацію кожного з 6 документів онлайн-валідатором на відповідність стандарту RFC 8259»."
    )

    # ---------------- РАЗДЕЛ 2 ----------------
    add_h1("2. Иерархия NoSQL и сравнение с SQL на простых аналогиях")
    add_p(
        "Полная иерархия сущностей NoSQL от общего к частному выглядит так: "
        "Кластер (Cluster) -> База данных (Database) -> Коллекция (Collection) -> Документ (Document) -> Поле (Field)."
    )
    add_p(
        "Чтобы не путаться в терминах, запомни простую бытовую аналогию: "
        "Кластер - это вся сеть филиалов компании. База данных - это Шкаф в конкретном филиале. "
        "Коллекция - это Полка в шкафу. Документ - это Папка на полке. Поле - это конкретная строчка в документе."
    )

    add_image_box(
        "NoSQL_and_distributed_databases/lab2/lecture_slides/page_09.png",
        "Рис. 1. Сопоставление понятий реляционных баз данных и MongoDB (Слайд 9 лекции Жишковича А. В.)",
        width_in=5.4
    )

    t = doc.add_table(rows=8, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t)

    table_data = [
        ["SQL (Таблицы / Строки)", "MongoDB (Коллекции / Документы)", "Суть на простых пальцах"],
        ["База данных (Database)", "База данных (Database)", "Общий шкаф проекта. Хранит группу тематических коллекций."],
        ["Таблица (Table)", "Коллекция (Collection)", "Полка в шкафу. В SQL все строки обязаны быть под одну гребенку, в Mongo на одной полке лежат гибкие документы."],
        ["Строка / Запись (Row)", "Документ (Document)", "Отдельная папка-карточка. Внутри данные в виде пар 'ключ: значение'."],
        ["Столбец (Column)", "Поле (Field)", "Атрибут карточки: строка, число, дата, целый массив или вложенный поддокумент."],
        ["JOIN (соединение)", "Вложенность (Embedded Docs)", "В SQL таблицы связывают внешними ключами. В Mongo всю информацию сразу кладут внутрь одного документа."],
        ["Primary Key (ID)", "Поле _id (ObjectId)", "Уникальный паспорт документа на 12 байт, чтобы отличать карточки друг от друга."],
        ["Схема (CREATE TABLE)", "Динамическая схема (Schemaless)", "В SQL схема фиксируется до записи. В Mongo каждый документ сам несет свои поля (Schema-on-Read)."]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            if r_idx == 0:
                set_cell_background(cell, "E2E8F0")
                run.font.bold = True
                run.font.size = Pt(10)
                run.font.color.rgb = COLOR_PRIMARY
            else:
                run.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_callout(
        "Ключевой теоретический вопрос: «Где живут коллекции - в базе данных или в шарде?»",
        "Ответ: Логически коллекция принадлежит базе данных (шкафу). А физически, если включен шардинг на больших серверах, "
        "ОДНА И ТА ЖЕ коллекция разрезается на порции (чанки) и раскидывается по разным физическим серверам-шардам. "
        "Для программиста это единая коллекция, а для винчестеров - файлы на разных компьютерах."
    )

    # ---------------- РАЗДЕЛ 3 ----------------
    add_h1("3. Архитектура шардинга и масштабирования (Слайд 10 лекции)")
    add_p(
        "Когда интернет-магазин вырастает и объем товаров с заказами переваливает за терабайты, один физический компьютер "
        "не справляется с нагрузкой. MongoDB масштабируется горизонтально (Scale-Out) через шардинг:"
    )

    add_image_box(
        "NoSQL_and_distributed_databases/lab2/lecture_slides/page_10.png",
        "Рис. 2. Компоненты распределенного кластера MongoDB: mongos, Config Servers, Shards (Слайд 10 лекции)",
        width_in=5.2
    )

    add_bullet("Шард (Shard): это отдельные склады с данными. Например, товары A-M лежат на Шарде 1, а N-Z - на Шарде 2. Внимание: шард - это не один компьютер, а набор реплик (Replica Set, минимум 3 машины: 1 главная Primary + 2 копии Secondary). Если сгорит один сервер, данные не пропадут.", "1. Склады данных (Shards) - ")
    add_bullet("Config Servers (Картотека кластера): служебные серверы, где хранится блокнот-карта. В ней записано, какой диапазон товаров на каком складе лежит.", "2. Метаданные (Config Servers) - ")
    add_bullet("mongos (Охранник-навигатор): клиентское приложение общается только с ним. mongos не хранит данных на диске. Он принимает запрос 'дай товар ASUS', смотрит в блокнот Config Server, видит 'это лежит на Шарде 1', сам идет туда, забирает и возвращает клиенту. Программисту не нужно знать, где физически лежат серверы.", "3. Маршрутизатор (mongos) - ")
    add_bullet("Чанги (Chunks / Чанґи) и Ключ шардинга (Shard Key): коллекция нарезается на непрерывные блоки по ключу шардинга (Shard Key, например product_id). По умолчанию размер чанга равен 64 МБ. Когда чанг переполняется, он расщепляется (chunk split), а балансировщик (Balancer) автоматически переносит часть чангов на менее загруженные шарды.", "4. Чанги и балансировка - ")

    # ---------------- РАЗДЕЛ 4 ----------------
    add_h1("4. Почему BSON, а не чистый JSON? И анатомия поля _id")

    add_image_box(
        "NoSQL_and_distributed_databases/lab2/lecture_slides/page_18.png",
        "Рис. 3. Различие между форматами JSON (текст) и BSON (бинарный) (Слайд 18 лекции)",
        width_in=5.2
    )

    add_p(
        "В чем разница и когда что применяется: "
        "JSON (JavaScript Object Notation) - это обычный текст. Человеку удобно читать и редактировать его глазами, а веб-сайтам - "
        "передавать его по интернету. Но если бы база данных хранила внутри себя чистый текст JSON, она бы дико тормозила: "
        "чтобы найти нужное поле в конце файла, пришлось бы парсить весь текст символ за символом."
    )
    add_p(
        "Кто выполняет конвертацию: преобразование выполняет клиентский драйвер (например, pymongo в Python или драйвер Node.js внутри mongosh). "
        "Приложение отправляет JSON-объект, драйвер кодирует его в BSON и отсылает серверу mongod. При чтении драйвер декодирует BSON обратно в JSON."
    )
    add_p(
        "BSON (Binary JSON) - это двоичный машинный формат. Два главных преимущества:"
    )
    add_bullet("Скорость обхода полей: перед каждым элементом в BSON записана его длина в байтах. Сервер может мгновенно перепрыгнуть ненужный блок памяти, не читая его.", "1. Быстродействие: ")
    add_bullet("Богатая типизация и экономия памяти: число 12345678 в тексте JSON занимает 8 байт (символов), а в BSON пакуется ровно в 4 байта. BSON добавляет точные даты (Date), целые числа 32 и 64 бит, сырые байты (BinData) и уникальный ключ ObjectId.", "2. Типы данных: ")

    add_image_box(
        "NoSQL_and_distributed_databases/lab2/lecture_slides/page_11.png",
        "Рис. 4. Структура 12-байтного идентификатора документа ObjectId (Слайд 11 лекции)",
        width_in=5.4
    )

    add_callout(
        "Коронный капкан Жишковича: «Из чего состоит _id (ObjectId) на 12 байт?» (Слайд 11)",
        "Поле _id занимает ровно 12 байт (в виде строки это 24 шестнадцатеричных символа). Формула 4-3-2-3:\n"
        "• 4 байта - время создания документа (Unix timestamp в секундах). ВАЖНО: документы в MongoDB автоматически упорядочены по времени создания!\n"
        "• 3 байта - уникальный идентификатор физического компьютера (хоста).\n"
        "• 2 байта - идентификатор процесса mongod (PID сервера).\n"
        "• 3 байта - инкрементный счетчик, который тикает при каждой новой вставке, исключая совпадения в одну секунду.\n"
        "Ответ преподавателю: «12 байт: 4 часу, 3 комп'ютера, 2 процесу і 3 лічильника».",
        is_trap=True
    )

    # ---------------- РАЗДЕЛ 5 ----------------
    add_h1("5. Графический клиент Compass и системные базы данных")
    add_p(
        "При первом запуске MongoDB Compass и подключении по адресу mongodb://localhost:27017/ в навигационной панели "
        "отображаются 3 базы данных, созданные сервером по умолчанию:"
    )

    add_image_box(
        "NoSQL_and_distributed_databases/lab2/compass_connected_crop.png",
        "Рис. 5. Интерфейс MongoDB Compass и системные базы данных admin, config, local",
        width_in=3.6
    )

    add_bullet("admin: системная база для хранения учетных записей администраторов, паролей, ролей и прав доступа.", "• ")
    add_bullet("config: служебная база для распределенного шардинга (здесь хранятся настройки кластера и карта чанков).", "• ")
    add_bullet("local: журнал работы конкретного сервера (oplog). Данные из базы local НИКОГДА не реплицируются на другие серверы.", "• ")
    add_p(
        "Зачем нужен Compass: это официальный графический интерфейс (GUI), позволяющий управлять базой без терминала - просматривать "
        "коллекции в виде дерева или таблицы, наглядно строить фильтры поиска, анализировать распределение типов полей (Schema Analysis) "
        "и отслеживать графики нагрузки сервера в реальном времени."
    )

    # ---------------- РАЗДЕЛ 6 ----------------
    add_h1("6. Разбор спроектированных документов интернет-магазина (TechStore)")
    add_p(
        "По заданию требовалось спроектировать 2 коллекции с обязательным использованием двух ключевых механизмов NoSQL:"
    )

    add_h2("1. Вложенные документы (Embedded Documents / Денормализация)")
    add_p(
        "В реляционных базах характеристики процессора (сокет, ядра, потоки, частоты, теплопакет) пришлось бы выносить в отдельную "
        "таблицу со связью по ID. В MongoDB мы вложили объект specifications прямо внутрь карточки товара PROD-102, а адрес "
        "доставки delivery_details - прямо внутрь заказа ORD-2026-002. "
        "Почему это круто: при открытии карточки товара база считывает весь объект за одно дисковое обращение без всяких JOIN."
    )

    add_h2("2. Массивы (Arrays)")
    add_p(
        "Массив тегов tags (['ips', '165hz', '2k_qhd']) в мониторе PROD-101 и массив купленных позиций items в заказе ORD-2026-001. "
        "В SQL для чека нужна связующая таблица Order_Items. В Mongo заказ содержит список купленных товаров прямо внутри себя."
    )

    add_callout(
        "Зачем нужна валидация синтаксиса в онлайн-валидаторе (Пункт 11 методички):",
        "JSON подчиняется жесткому стандарту RFC 8259:\n"
        "1. Все ключи ОБЯЗАНЫ быть в двойных кавычках \"key\" (одинарные кавычки 'key' вызовут ошибку синтаксиса).\n"
        "2. Запятая после последнего элемента в объекте или массиве категорически запрещена (trailing comma).\n"
        "3. Числа пишутся без кавычек, логические значения - строчными true/false.\n"
        "Зеленый статус VALID JSON в отчете для всех 6 документов подтверждает отсутствие синтаксических ошибок."
    )

    # ---------------- РАЗДЕЛ 7 ----------------
    add_h1("7. 3-Tier Code Anatomy: скрипт загрузки данных (main.py)")
    add_p(
        "В репозитории подготовлен вспомогательный скрипт main.py для импорта JSON в базу. Ниже приведен его 3-уровневый разбор:"
    )

    add_code_block(
        "client = MongoClient('mongodb://localhost:27017/')\n"
        "db = client['techstore']\n"
        "db.products.drop()\n"
        "res = db.products.insert_many(products)"
    )

    add_bullet("Tier 1 (Назначение): подключение к локальному серверу MongoDB, переключение на базу techstore, очистка старой коллекции и пакетная загрузка подготовленных документов.", "• ")
    add_bullet("Tier 2 (Механика): MongoClient инициализирует пул соединений к порту 27017. db.products.drop() удаляет старую коллекцию вместе с индексами. insert_many() выполняет Bulk Insert за один сетевой запрос.", "• ")
    add_bullet("Tier 3 (Вопросы на защите): «Что вернет insert_many?» Ответ: объект InsertManyResult со списком сгенерированных ObjectId. «Что будет, если коллекция не существовала?» Ответ: Mongo создаст ее автоматически на лету (Lazy Creation).", "• ")

    # ---------------- РАЗДЕЛ 8 ----------------
    add_h1("8. Ответы на все 10 контрольных вопросов методички (Шпаргалка для сдачи)")

    questions_answers = [
        ("1. Що таке документо-орієнтована БД і чим відрізняється від реляційної?",
         "Це NoSQL СКБД, яка зберігає дані у вигляді самодостатніх ієрархічних документів (BSON/JSON) замість фіксованих таблиць. "
         "Відрізняється динамічною схемою (schemaless) та заміною важких з'єднань JOIN на природну вкладеність даних."),

        ("2. Яку NoSQL-модель даних використовує MongoDB?",
         "Документну модель (Document Store)."),

        ("3. Чим відрізняються документи MongoDB від рядків у реляційних БД?",
         "Рядок у RDBMS є плоским і жорстко обмежений колонками таблиці. Документ MongoDB - це гнучке дерево пар 'ключ: значення', "
         "може містити вкладені об'єкти та списки (масиви), а сусідні документи можуть мати абсолютно різні набори полів."),

        ("4. Що таке 'динамічна схема' (Dynamic Schema / Schemaless) в MongoDB?",
         "Це властивість бази зберігати документи довільної структури без попереднього оголошення колонок через CREATE TABLE. "
         "Структура інтерпретується програмою під час читання (Schema-on-Read)."),

        ("5. Які основні версії MongoDB і в яких операційних системах вона може працювати?",
         "Версії: Community Edition (відкрита безкоштовна), Enterprise Advanced (комерційна для бізнесу) та хмарна Atlas. "
         "Працює на Windows, Linux та macOS."),

        ("6. Назвіть ключові відмінності між Community та Enterprise версіями?",
         "Enterprise має корпоративні модулі безпеки (LDAP, Kerberos, шифрування дисків), движок обчислень у пам'яті (In-Memory), "
         "детальний аудит дій та офіційну підтримку 24/7."),

        ("7. Яка різниця між виконуваними файлами mongod та mongosh?",
         "mongod - це головний серверний процес (демон/служба), який керує файлами на диску, пам'яттю та портами. "
         "mongosh - це клієнтська консоль (термінал на Node.js), через яку користувач пише команди до бази."),

        ("8. Які функції при роботі з базами даних підтримує MongoDB Compass?",
         "Перегляд і редагування документів, графічний конструктор фільтрів пошуку, аналіз схеми та типів полів, "
         "побудова конвеєрів агрегації та моніторинг навантаження сервера."),

        ("9. Поясніть, що таке об'єкт та масив у форматі JSON?",
         "Об'єкт ({}) - це невпорядкований набір пар 'ключ: значення' у фігурних дужках. Масив ([]) - це впорядкований список "
         "елементів будь-якого типу через кому у квадратних дужках."),

        ("10. Що таке BSON і чому MongoDB використовує саме його, а не чистий JSON?",
         "BSON - це двійкове представлення JSON. MongoDB використовує його заради високої швидкості (префікси довжини дозволяють миттєво пропускати поля при читанні) "
         "та розширених типів (Date, ObjectId, 64-бітні числа).")
    ]

    for q, a in questions_answers:
        add_callout(q, a, is_trap=False)

    # ---------------- РАЗДЕЛ 9 ----------------
    add_h1("9. Вопросы-капканы преподавателя на защите")

    traps = [
        ("Капкан 1: «Що таке WiredTiger і навіщо він у MongoDB?»",
         "WiredTiger - це стандартний внутрішній движок зберігання даних (Storage Engine) у MongoDB з версії 3.2. "
         "Він відповідає за запис файлів на диск, стиснення даних (Snappy/zlib, що економить до 70% місця) та керування кешем в RAM."),

        ("Капкан 2: «Що таке ледаче створення (Lazy Creation) колекцій?»",
         "У MongoDB не обов'язково викликати команду створення колекції заздалегідь. Як тільки в базу вставляється перший документ, "
         "MongoDB автоматично створює і нову базу даних, і нову колекцію на льоту."),

        ("Капкан 3: «Чи є в MongoDB транзакції ACID?»",
         "Традиційно в NoSQL атомарність гарантується на рівні одного документа (всі зміни всередині однієї карточки відбуваються надійно). "
         "Багатодокументні транзакції підтримуються починаючи з версії 4.0, але їх уникають за рахунок грамотної вкладеної структури."),

        ("Капкан 4: «Чому в замовленні ORD-2026-002 вказано місто Львів та Нова Пошта №42?»",
         "Це персоналізація документа для підтвердження індивідуального виконання роботи: реальне місто навчання та ПІБ студента ФеП-33 Абдулханова Абдул-Рахіма.")
    ]

    for title, text in traps:
        add_callout(title, text, is_trap=True)

    # ---------------- РАЗДЕЛ 10 ----------------
    add_h1("10. Блиц-тренажер перед защитой (Active Recall)")
    add_p("Закрой рукой правый столбец и ответь на каждый вопрос за 5 секунд:")

    t_drill = doc.add_table(rows=6, cols=2)
    t_drill.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_drill)

    drills = [
        ["Вопрос преподавателя", "Быстрый опорный ответ"],
        ["Из чего состоит ObjectId на 12 байт?", "Формула 4-3-2-3: 4 байта времени, 3 байта сервера, 2 байта процесса, 3 байта счетчика."],
        ["Чем отличается mongod от mongosh?", "mongod - серверный демон; mongosh - консольный клиент."],
        ["Зачем денормализация в NoSQL?", "Чтобы не делать медленные JOIN и забирать всю информацию за одно чтение."],
        ["Почему база хранит BSON, а не JSON?", "BSON двоичный, быстрее читается за счет префиксов длины и умеет хранить Date и ObjectId."],
        ["Как работает шардинг?", "mongos направляет запрос, Config Server хранит карту, Shards (Replica Sets) хранят куски данных."]
    ]

    for r_idx, row in enumerate(drills):
        for c_idx, val in enumerate(row):
            cell = t_drill.cell(r_idx, c_idx)
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            if r_idx == 0:
                set_cell_background(cell, "E2E8F0")
                run.font.bold = True
                run.font.size = Pt(10)
                run.font.color.rgb = COLOR_PRIMARY
            else:
                run.font.size = Pt(9.5)

    # Сохранение файлов
    lab2_dir = os.path.join("NoSQL_and_distributed_databases", "lab2")
    docx_path = os.path.join(lab2_dir, "conspect.docx")
    temp_pdf_path = os.path.join(lab2_dir, "conspect.pdf")
    final_pdf_path = os.path.join(lab2_dir, "nosql_db_lab2_conspect.pdf")

    doc.save(docx_path)
    print(f"Saved conspect docx: {docx_path}")

    print(f"Converting to PDF: {temp_pdf_path}...")
    convert_docx_to_pdf(docx_path, temp_pdf_path)

    import shutil
    shutil.copyfile(temp_pdf_path, final_pdf_path)
    print(f"SUCCESS: Generated conspect PDF: {final_pdf_path}")

if __name__ == "__main__":
    build_conspect()
