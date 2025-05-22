from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/cgi-bin/l.cgi")
def handle_lcgi():
    # Отримаємо дату з параметрів запиту
    day = request.args.get("d", "2025-01-01")

    # Тут ти можеш зчитати відповідний XML-файл з диска
    file_path = f"data/{day}.xml"  # наприклад: data/2025-05-22.xml
    if not os.path.exists(file_path):
        return Response(f"<error>Файл {day}.xml не знайдено</error>", status=404, mimetype="application/xml")

    with open(file_path, "r", encoding="utf-8") as f:
        xml_content = f.read()

    return Response(xml_content, mimetype="application/xml")


