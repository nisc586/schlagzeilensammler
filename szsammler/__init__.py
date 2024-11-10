from flask import Flask, render_template, abort, url_for


app = app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/headlines")
def headlines_api():
    headlines = [
        "Trump erneut Präsident!",
        "Barcelona Kantersieg in der Champions League!",
        "Programmierer immer noch arbeitslos",
    ]
    return headlines

@app.route("/settings")
def settings():
    abort(501)