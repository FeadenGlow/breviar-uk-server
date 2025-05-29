from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)

# Ідентифікатор календаря (можна розширити пізніше на інші календарі)
CALENDAR = 'roman-uk'  

# Базові папки для статичних файлів
BASE_DIR = os.path.dirname(__file__)
HTML_DIR = os.path.join(BASE_DIR, 'static', CALENDAR, 'htm')
XML_DIR  = os.path.join(BASE_DIR, 'static', CALENDAR, 'xml')

@app.route('/cgi-bin/l.cgi')
def lcgi():
    # Збираємо всі параметри запиту в словник
    params = request.args.to_dict(flat=True)

    qt = params.get('qt')      # формат відповіді: 'pxml', 'pdt', тощо
    d  = params.get('d')       # день або '*'
    m  = params.get('m')       # місяць
    r  = params.get('r')       # рік
    p  = params.get('p')       # код молитви: 'mi','mrch','mpc','mpred','mna',…
    # є також o0…o6, ds, j, k — ігноруємо для маршрутизації, але вони лишаються в URL

    # 1) Calendar XML для дня
    if qt == 'pxml' and d and d != '*':
        # static/roman-uk/xml/pxml/day/2025_05_28.xml
        filename = f"{r}_{int(m):02d}_{int(d):02d}.xml"
        subdir = os.path.join(XML_DIR, 'pxml', 'day')
        return _send_xml(subdir, filename)

    # 2) Calendar XML для місяця
    if qt == 'pxml' and d == '*':
        # static/roman-uk/xml/pxml/month/2025_05.xml
        filename = f"{r}_{int(m):02d}.xml"
        subdir = os.path.join(XML_DIR, 'pxml', 'month')
        return _send_xml(subdir, filename)

    # 3) Prayer XML (pdt) — різні види молитов
    if qt == 'pdt' and p and d and m and r:
        # static/roman-uk/xml/pdt/mi/2025_05_28.xml  (якщо p='mi')
        filename = f"{r}_{int(m):02d}_{int(d):02d}.xml"
        subdir = os.path.join(XML_DIR, 'pdt', p)
        return _send_xml(subdir, filename)

    # 4) Prayer XML короткі молитви (mpc, mpred, mna, mrch тощо)
    # Код p вже містить потрібний префікс, тому він теж потрапить у гілку 3.

    # 5) HTML відповіді (коли треба .htm, наприклад для 'qt=htm')
    if qt == 'htm' and d and m and r:
        # Ми припускаємо, що ти згенерував аналогічні HTML у:
        # static/roman-uk/htm/2025_05_28.htm
        filename = f"{r}_{int(m):02d}_{int(d):02d}.htm"
        return _send_html(HTML_DIR, filename)

    # Якщо нічого з вище не спрацювало — 400 Bad Request
    abort(400, f"Неправильні або відсутні параметри: {params}")

def _send_xml(subdir, filename):
    path = os.path.join(subdir, filename)
    if not os.path.isfile(path):
        abort(404, f"XML файл не знайдено: {filename}")
    return send_from_directory(subdir, filename, mimetype='text/xml')

def _send_html(subdir, filename):
    path = os.path.join(subdir, filename)
    if not os.path.isfile(path):
        abort(404, f"HTML файл не знайдено: {filename}")
    return send_from_directory(subdir, filename, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
