from flask import Flask, request, Response
import os
from datetime import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRAYERS_DIR = os.path.join(BASE_DIR, "prayers")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")

@app.route("/cgi-bin/l.cgi")
def handle_cgi():
    qt = request.args.get("qt")
    d = request.args.get("d")
    m = request.args.get("m")
    r = request.args.get("r")
    j = request.args.get("j")  # мова (uk)
    k = request.args.get("k")  # календар (uk)

    if qt != "pxml" or not all([d, m, r, j, k]):
        return Response("Bad request", status=400)

    try:
        day = int(d)
        month = int(m)
        year = int(r)
        date_str = f"{year}-{month:02}-{day:02}"
    except ValueError:
        return Response("Invalid date", status=400)

    xml_path = ensure_xml_exists(year, month, day)
    if not os.path.exists(xml_path):
        return Response("Prayer text not found", status=404)

    with open(xml_path, encoding="utf-8") as f:
        return Response(f.read(), mimetype="text/xml")


def ensure_xml_exists(year: int, month: int, day: int) -> str:
    target_dir = os.path.join(GENERATED_DIR, str(year), f"{month:02}")
    os.makedirs(target_dir, exist_ok=True)

    xml_file = os.path.join(target_dir, f"{day:02}.xml")
    if os.path.exists(xml_file):
        return xml_file

    html_filename = f"{day:02}cezrok_pc.htm"
    html_path = os.path.join(PRAYERS_DIR, html_filename)
    print(f"Looking for file: {html_path}")
    if not os.path.exists(html_path):
        return xml_file  # порожній, але уникнемо помилки

    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    xml = generate_xml_from_html(html, f"{year}-{month:02}-{day:02}")

    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml)

    return xml_file


def generate_xml_from_html(html: str, date_iso: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body or soup
    text = body.get_text(separator="\n", strip=True)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<LHData>
  <CalendarDay>
    <DateISO>{date_iso}</DateISO>
    <Celebration>
      <Id>uk_custom</Id>
      <StringTitle><span>{text[:50]}</span></StringTitle>
      <LiturgicalCelebrationColor Id="2" />
    </Celebration>
  </CalendarDay>
</LHData>
"""


@app.route("/")
def home():
    return "Breviar UK Server is running."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
