from flask import current_app, g
import click
from sqlalchemy import create_engine, Column, String
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import mapped_column, Mapped

Base = declarative_base()


class Headline(Base):
    __tablename__ = "headlines"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(nullable=False)
    link: Mapped[str] = mapped_column()
    pub_date: Mapped[str] = mapped_column()  # todo: use datetime type for pubDate
    description: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column()  # todo: add channel table and foreign key

    def __repr__(self):
        return f"Headline(id={self.id}, title={self.title}, pub_date={self.pub_date})"


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
    stmt = select(Headline)
    with Session(get_db()) as session:
        result = session.execute(stmt).fetchall()
    return result