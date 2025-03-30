from json import JSONDecodeError
from flask import Blueprint, render_template, jsonify, request
from . import db
from .models import Article, Channel
import feedparser
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    count = Article.query.count()
    return render_template("index.html", count=count)

@main.route("/fetch-articles/rss", methods=["GET"])
def get_articles_from_rss():
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
                channel_id=1  # TODO: Implement newspapers model
            )
            db.session.add(new_article)
            new_articles.append(new_article.to_dict())

    db.session.commit()
    return jsonify({"articles" :new_articles})


@main.route("/fetch-articles/db", methods=["GET"])
def get_articles_from_db():
    articles = [article.to_dict() for article in Article.query.all()]
    return jsonify({"articles": articles})


@main.route("/channel/new", methods=["GET", "POST"])
def create_new_channel():
    if request.method == "POST":
        if request.content_type == "application/json":
            if not request.data:
                return jsonify({"error": "Missing payload, 'rss_url' is required."}), 400
            rss_url = request.get_json().get("rss_url")
        else:
            # default for forms application/x-www-form-urlencoded
            rss_url = request.form["rss_url"]

        if not rss_url:
            return jsonify({"error": "RSS Url is required."}), 400
        
        rss = feedparser.parse(rss_url)
        if rss.bozo:
            return jsonify({"error": f"Invalid RSS feed at: {rss_url}"}), 400
        
        feed = rss.feed
        # feed.link does not necessarily link to the rss-channel.
        # In the xml it typically is the atom:link, that points to the rss-URL.
        # The parsed feed does not distinguish between namespaces as far as I know
        for link in feed.links:
            if (link["type"] == "application/rss+xml"):
                channel_link = link["href"]
                break
        
        if not Channel.query.filter_by(link=feed.link).first():
            new_channel = Channel(
                title = feed.title,
                link = channel_link,
                description = feed.description,
                image_url = feed.image.url,
            )
        
        return jsonify({"channel": new_channel.to_dict()})
    else:
        # GET request
        return render_template("channel_new.html")


@main.route("/success")
def success():
    return "Erfolgreich Channel hinzugefügt!"