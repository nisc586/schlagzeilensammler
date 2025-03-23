import pytest
from conftest import client
from pathlib import Path

def test_create_new_channel(client):
    some_xml = Path("tests\data\sz.xml")
    response = client.post("/channel/new", json={"rss_url": str(some_xml)})
    channel = response.get_json()["channel"]
    assert response.status_code == 200
    assert channel["title"] == "Alle Meldungen - SZ.de"
    assert channel["description"] == "sz.de"
    assert channel["link"] == "https://rss.sueddeutsche.de/alles"
    assert channel["image_url"] == "https://www.sueddeutsche.de/assets/img/favicon.ico"


def test_create_new_channel_no_url(client):
    response = client.post("/channel/new", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json() == {'error': "Missing payload, 'rss_url' is required."}


def test_create_new_channel_invalid_rss(client):
    response = client.post("/channel/new", content_type="application/json", json={"rss_url": "example.org"})
    assert response.status_code == 400
    assert response.get_json() == {"error": f"Invalid RSS feed at: example.org"}