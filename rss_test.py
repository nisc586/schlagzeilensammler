from rss_parser import RSSParser
from requests import get
import sqlite3

rss_url = "https://www.faz.net/rss/aktuell/"
response = get(rss_url)
rss = RSSParser.parse(response.text)

con = sqlite3.connect("instance/test_db.sqlite")
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS headlines;")
cur.execute("""
    CREATE TABLE headlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        link TEXT,
        pubDate TEXT,
        descriptionText TEXT,
        newspaper TEXT
    );
""")

print(f"RSS channel has {len(rss.channel.items)} items")

for item in rss.channel.items:
    cur.execute(f"INSERT INTO headlines (title, link, pubDate, descriptionText, newspaper) VALUES ('{item.title.content}', '{item.links[0].content}', '{item.pub_date.content}', '{item.description.content}', 'FAZ')")

con.commit()
con.close()


con = sqlite3.connect("instance/test_db.sqlite")
cur = con.cursor()
cur.execute("SELECT * FROM headlines")

for row in cur.fetchall():
    print(row, "\n")
con.close()