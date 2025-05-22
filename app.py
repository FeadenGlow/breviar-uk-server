from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route("/cgi-bin/l.cgi")
def handle_lcgi():
    day = request.args.get("d", "2025-01-01")
    file_path = f"data/{day}.xml"
    if not os.path.exists(file_path):
        return Response(f"<error>Файл {day}.xml не знайдено</error>", status=404, mimetype="application/xml")
    with open(file_path, "r", encoding="utf-8") as f:
        xml_content = f.read()
    return Response(xml_content, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



