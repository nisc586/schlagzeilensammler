from flask import Blueprint, render_template, jsonify
from . import db
from .models import Article
import feedparser
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    count = Article.query.count()
    return render_template("index.html", count=count)

@main.route("/fetch-articles", methods=["GET"])
def fetch_articles():
    RSS_URL = "https://www.faz.net/rss/aktuell/"  # TODO: Use different newspapers
    DT_FMT = "%a, %d %b %Y %H:%M:%S %z"

    feed = feedparser.parse(RSS_URL)

    new_articles = []
    for entry in feed.entries:
        # Do not insert duplicates into database
        if not Article.query.filter_by(title=entry.title).first():
            new_article = Article(
                title=entry.title,
                link=entry.link,
                published=datetime.strptime(entry.published, DT_FMT),
                description=entry.description,
                #channel=None  # TODO: Implement newspapers model
            )

        new_articles.append(new_article.to_dict())

    db.session.commit()
    return jsonify({"articles" :new_articles})