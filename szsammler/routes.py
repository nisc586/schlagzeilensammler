from json import JSONDecodeError
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from . import db
from .models import Article, Channel
import feedparser
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    count = Article.query.count()
    channels = [ch.to_dict() for ch in Channel.query.all()]
    return render_template("index.html.j2", count=count, channels=channels)


@main.route("/fetch-articles/rss", methods=["GET"])
def get_articles_from_rss():
    DT_FMT = "%a, %d %b %Y %H:%M:%S %z"
    channel_id = request.args.get("channel_id", 1, type=int)

    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({"error": f"Channel with {channel_id=} not found."}), 400

    feed = feedparser.parse(channel.link)
    new_articles = []
    for entry in feed.entries:
        # Do not insert duplicates into database
        if not Article.query.filter_by(title=entry.title).first():
            new_article = Article(
                title = entry.title,
                link = entry.link,
                published = datetime.strptime(entry.published, DT_FMT),
                description = entry.description,
                channel_id = channel_id
            )
            db.session.add(new_article)
            new_articles.append(new_article.to_dict())

    db.session.commit()
    return jsonify({"articles" :new_articles})


@main.route("/fetch-articles/db", methods=["GET"])
def get_articles_from_db():
    page = request.args.get("page", 1, type=int)
    channel_id = request.args.get("channel_id", 1, type=int)
    per_page = 20

    pagination = Article.query.where(Article.channel_id == channel_id).order_by(Article.published.desc()).paginate(page=page, per_page=per_page)
    articles = [article.to_dict() for article in pagination.items]
    return jsonify({
        "articles": articles,
        "has_next": pagination.has_next,
        })


@main.route("/channels/")
def channels_():
    return redirect(url_for("main.channels"))


@main.route("/channels")
def channels():
    channels = [ch.to_dict() for ch in Channel.query.all()]
    return render_template("channels.html", channels=channels)


@main.route("/channels/new", methods=["GET", "POST"])
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
            # TODO: add channel to the database
        
        # TODO: redirect to channels page
        return redirect(url_for('main.channels'))
    else:
        # GET request
        return render_template("channels_new.html")


@main.route("/channels/list")
def channels_list():
    return jsonify([ch.to_dict() for ch in Channel.query.all()])