from flask import Flask, render_template, abort
from pathlib import Path

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE = Path(app.instance_path) / "db.sqlite"
    )
    from . import db
    db.init_app(app)

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
    
    return app