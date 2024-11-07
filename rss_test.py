from rss_parser import RSSParser
from requests import get

rss_url = "https://www.faz.net/rss/aktuell/"
response = get(rss_url)

rss = RSSParser.parse(response.text)

print(f"RSS channel has {len(rss.channel.items)} items")

for item in rss.channel.items:
    print(item.title)
    print(item.description)
    print("\n")