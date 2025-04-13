from json import JSONDecodeError
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from . import db
from .models import Article, Channel
import feedparser
from datetime import datetime

main = Blueprint("main", __name__)

mock_data = [
{
    'id': 1,
    'title': 'Aktuell - FAZ.NET',
    'link': 'https://www.faz.net/rss/aktuell/',
    'description': 'News, Nachrichten und aktuelle Meldungen aus allen Ressorts. Politik, Wirtschaft, Sport, Feuilleton und Finanzen im Überblick.',
    'image_url': 'https://icons.duckduckgo.com/ip3/faz.net.ico'
},
{
    'id': 2,
    'title': 'Spiegel Online – Die große Nachrichtenübersicht aus dem In- und Ausland',
    'link': 'https://www.spiegel.de/schlagzeilen/tops/index.rss',
    'description': 'Aktuelle Nachrichten, Reportagen, Interviews, Videos und Bilder aus Politik, Wirtschaft, Kultur und Sport. Alle Entwicklungen im Newsticker.',
    'image_url': 'https://icons.duckduckgo.com/ip3/spiegel.de.ico'
},
{
    'id': 3,
    'title': 'TechNova – Zukunft, Innovation & digitale Trends',
    'link': 'https://www.technova.io/rss',
    'description': 'Entdecke spannende Artikel rund um Technologie, KI, digitale Transformation, Start-ups und wissenschaftliche Durchbrüche – täglich neu.',
    'image_url': 'https://icons.duckduckgo.com/ip3/technova.io.ico'
},
{
    'id': 4,
    'title': 'Local Times – Regionales aus deiner Umgebung',
    'link': 'https://www.localtimes.example/rss',
    'description': 'Nachrichten aus deiner Region, Veranstaltungen, Wetter und Verkehrsmeldungen. Alles, was du für deinen Alltag wissen musst, an einem Ort.',
    'image_url': 'https://icons.duckduckgo.com/ip3/localtimes.example.ico'
},
{
    'id': 5,
    'title': 'World Digest – Globale News kompakt zusammengefasst',
    'link': 'https://www.worlddigest.news/rss',
    'description': 'Internationale Nachrichten, Krisen, Analysen und Hintergrundberichte in einer kompakten täglichen Übersicht. Ideal für Vielbeschäftigte.',
    'image_url': 'https://icons.duckduckgo.com/ip3/worlddigest.news.ico'
}]


@main.route("/")
def index():
    count = Article.query.count()
    return render_template("index.html.j2", count=count, channels=mock_data)


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

    pagination = Article.query.where(Article.channel_id == channel_id).order_by(Article.published).paginate(page=page, per_page=per_page)
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
    return render_template("channels.html", channels=mock_data)


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
    return jsonify(mock_data)