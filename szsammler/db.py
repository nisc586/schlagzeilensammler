from flask import current_app, g
import click
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import select
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Headline(Base):
    __tablename__ = "headlines"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    link = Column("link", String)
    pub_date = Column("pubDate", String)  # todo: use datetime type for pubDate
    description = Column("descriptionText", String)
    channel = Column("channel", String)  # todo: add channel table and foreign key


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
    Base.metadata.drop_all(db)
    Base.metadata.create_all(db)


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_headlines():
    return select(Headline)