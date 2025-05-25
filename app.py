# app.py
import os
from flask import Flask, request, send_from_directory, abort, Response
import xml.etree.ElementTree as ET
from datetime import date, datetime

app = Flask(__name__)

# Шлях до статичних HTM-файлів (твої файли)
HTM_DIR = os.path.join(app.root_path, 'static', 'htm')
# Шлях до XML-шаблону (взятий із l.cgi.xml, але спрощений)
XML_TEMPLATE = os.path.join(app.root_path, 'data', 'xml', 'template.xml')

@app.route('/cgi-bin/l.cgi')
def l_cgi():
    # --- 1. Парсинг базових параметрів ---
    try:
        day   = int(request.args.get('d'))
        month = int(request.args.get('m'))
        year  = int(request.args.get('r'))
        lang  = request.args.get('j', 'uk')   # мова
        cal   = request.args.get('k', 'uk')   # календар
        qt    = request.args.get('qt', '')    # тип відповіді
    except (TypeError, ValueError):
        return abort(400, 'Invalid date parameters')

    # Перевірка дати
    try:
        dt = date(year, month, day)
    except ValueError:
        return abort(400, 'Impossible date')

    if qt == 'pxml':
        # --- 2. Генерація XML ---
        if not os.path.exists(XML_TEMPLATE):
            return abort(500, 'XML template not found')
        tree = ET.parse(XML_TEMPLATE)
        root = tree.getroot()

        # Замінюємо поля дати:
        cd = root.find('CalendarDay')
        cd.find('DateISO').text   = dt.isoformat()
        cd.find('DateDay').text   = str(dt.day)
        cd.find('DateMonth').text = str(dt.month)
        cd.find('DateYear').text  = str(dt.year)
        cd.find('DayOfYear').text = str(dt.timetuple().tm_yday)
        # DayOfWeek: українською
        weekdays = ['понеділок','вівторок','середа','четвер','п’ятниця','субота','неділя']
        cd.find('DayOfWeek').text = weekdays[dt.weekday()]

        # Змінимо атрибути Celebration → наприклад, літургійний тиждень
        celeb = cd.find('Celebration')
        # простий приклад: тиждень у році
        weeknum = dt.isocalendar()[1]
        celeb.find('LiturgicalWeek').text = str(weeknum)

        # Повернути
        xml_bytes = ET.tostring(root, encoding='utf-8')
        return Response(xml_bytes, mimetype='application/xml')

    elif qt in ('htm', 'pdt'):
        # --- 3. Віддаємо потрібний HTM-файл ---
        # Очікуємо, що клієнт передає ім’я файлу:
        fname = request.args.get('file')
        if not fname:
            return abort(400, 'Missing file parameter')
        # Безпечна перевірка шляху:
        if '..' in fname or fname.startswith('/'):
            return abort(400, 'Invalid file name')
        fullpath = os.path.join(HTM_DIR, fname)
        if not os.path.isfile(fullpath):
            return abort(404, f'{fname} not found')
        return send_from_directory(HTM_DIR, fname, mimetype='text/html')

    else:
        return abort(400, 'Unsupported qt value')

if __name__ == '__main__':
    # Для продакшену заміни на WSGI-сервер (gunicorn)
    app.run(host='0.0.0.0', port=5000, debug=True)
