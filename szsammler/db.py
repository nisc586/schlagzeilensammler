from flask import current_app, g
import click
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

def get_db():
    if "db" not in g:
        url = f"sqlite:///{current_app.config['DATABASE']}"
        g.db = create_engine(url)
        # todo: log db engine created

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    # todo: log db engine deleted


def init_db():
    db = get_db()
    metadata_obj = MetaData()
    headlines_table = Table(
        "headlines",
        metadata_obj,
        Column("id", Integer, autoincrement=True),
        Column("title", String, nullable=False),
        Column("link", String),
        Column("pubDate", String),  # todo: use datetime type for pubDate
        Column("descriptionText", String),
        Column("channel", String),  # todo: add channel table and foreign key
    )
    metadata_obj.drop_all(db)
    metadata_obj.create_all(db)


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)