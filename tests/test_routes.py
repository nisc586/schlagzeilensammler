import pytest
from flask import url_for
from conftest import client
from pathlib import Path

def test_create_new_channel_redirect(client):
    response = client.post("/channels/new", data={})
    assert response.status_code == 302

def test_create_new_channel(client, app):
    some_xml = Path("tests\data\sz.xml")
    
    response = client.post("/channels/new", data={"rss_url": str(some_xml)}, follow_redirects=True)
    assert b"Added new channel - Alle Meldungen - SZ.de" in response.data

    with app.app_context():
        from szsammler.models import Channel
        ch = Channel.query.filter_by(title = "Alle Meldungen - SZ.de").scalar()
    
    assert ch.title == "Alle Meldungen - SZ.de"


def test_create_new_channel_already_exists(client):
    some_xml = Path("tests\data\sz.xml")

    response = client.post("/channels/new", data={"rss_url": str(some_xml)})
    response = client.post("/channels/new", data={"rss_url": str(some_xml)}, follow_redirects=True)
    # Note that it takes the channel_url from the rss-file.
    assert b"Channel from https://rss.sueddeutsche.de/alles already exists." in response.data

def test_create_new_channel_no_url(client):
    response = client.post("/channels/new", data={}, follow_redirects=True)
    assert b"Required URL is missing." in response.data

def test_create_new_channel_invalid_rss(client):
    response = client.post("/channels/new", data={"rss_url": "example.org"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/channels")

    response = client.post("/channels/new", data={"rss_url": "example.org"}, follow_redirects=True)
    assert b"Could not find RSS feed at URL." in response.data