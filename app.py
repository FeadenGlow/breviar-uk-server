from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/cgi-bin/l.cgi")
def handle_lcgi():
    qt = request.args.get("qt", "")
    d = request.args.get("d", "")
    m = request.args.get("m", "")
    r = request.args.get("r", "")
    j = request.args.get("j", "uk")
    k = request.args.get("k", "uk")

    # Обробка запиту виду qt=pxml
    if qt == "pxml":
        # Якщо d == '*', значить потрібен цілий місяць (можна реалізувати пізніше)
        if d == "*" or not d:
            return Response("<error>Запит місячного календаря ще не реалізований</error>", status=400, mimetype="application/xml")
        else:
            # Формуємо ім’я файлу для конкретної дати
            try:
                day = int(d)
                month = int(m)
                year = int(r)
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                file_path = f"data/{date_str}.xml"
                if not os.path.exists(file_path):
                    return Response(f"<error>Файл {date_str}.xml не знайдено</error>", status=404, mimetype="application/xml")
                with open(file_path, "r", encoding="utf-8") as f:
                    xml_content = f.read()
                return Response(xml_content, mimetype="application/xml")
            except:
                return Response("<error>Неправильний формат параметрів</error>", status=400, mimetype="application/xml")

    return Response("<error>Невідомий тип запиту</error>", status=400, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



