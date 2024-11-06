from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Willkommen beim Schlagzeilensammler</p>"

@app.route("/api")
def api():
    return "<p>TODO</p>"