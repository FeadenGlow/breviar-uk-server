from flask import Flask, request, send_from_directory
app = Flask(__name__)

@app.route("/cgi-bin/l.cgi")
def liturgical():
    day = request.args.get("d", "test")
    return send_from_directory("data", f"{day}.xml", mimetype="application/xml")

@app.route("/")
def index():
    return "Breviar server is running!"
