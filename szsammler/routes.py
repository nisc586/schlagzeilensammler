from flask import Blueprint, render_template
from .models import Headline

main = Blueprint("main", __name__)

@main.route("/")
def index():
    count = 0
    count = Headline.query.count()
    return render_template("index.html", count=count)
