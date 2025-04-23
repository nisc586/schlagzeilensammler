from json import JSONDecodeError
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from . import db
from .models import Article, Channel
import feedparser
from dateutil import parser as dateparser

main = Blueprint("main", __name__)

@main.route("/")
def index():
    count = Article.query.count()
    channels = [ch.to_dict() for ch in Channel.query.all()]
    return render_template("index.html.j2", count=count, channels=channels)


@main.route("/fetch-articles/rss", methods=["GET"])
def get_articles_from_rss():
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
                published = dateparser.parse(entry.published),
                description = entry.get("description", ""),
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
    return render_template("channels.html.j2", channels=channels)


@main.route("/channels/new", methods=["GET", "POST"])
def create_new_channel():
    if request.method == "POST":
        # default for forms application/x-www-form-urlencoded
        rss_url = request.form["rss_url"]

        if not rss_url:
            flash("Required URL is missing.")
            return redirect(url_for('main.channels'))
        
        rss = feedparser.parse(rss_url)
        if rss.bozo:
            flash("Could not find RSS feed at URL.")
            return redirect(url_for('main.channels'))
        
        feed = rss.feed
        # feed.link does not necessarily link to the rss-channel.
        # In the xml it typically is the atom:link, that points to the rss-URL.
        # The parsed feed does not distinguish between namespaces as far as I know
        # Fallback on the link provided by user
        channel_link = rss_url
        for link in feed.links:
            if (link["type"] == "application/rss+xml"):
                channel_link = link["href"]
                break
        
        if not Channel.query.filter_by(link=channel_link).first():
            new_channel = Channel(
                title = feed.title,
                link = channel_link,
                description = feed.description,
                image_url = feed.image.url,
            )
            db.session.add(new_channel)
            db.session.commit()
            flash(f"Added new channel - {feed.title}")
        else:
            flash(f"Channel from {channel_link} already exists.")

    return redirect(url_for('main.channels'))


@main.route("/channels/list")
def channels_list():
    return jsonify([ch.to_dict() for ch in Channel.query.all()])


@main.route('/channels/<int:channel_id>/delete', methods=['POST'])
def delete_channel(channel_id):
    channel = Channel.query.get_or_404(channel_id)
    db.session.delete(channel)
    db.session.commit()
    return redirect(url_for('main.channels'))

    

@main.route('/channels/<int:channel_id>/article_count')
def get_article_count(channel_id):
    channel = Channel.query.get_or_404(channel_id)
    count = len(channel.articles)
    return jsonify({'count': count})
