from sqlalchemy.orm import mapped_column, Mapped
from szsammler import db


class Headline(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(nullable=False)
    link: Mapped[str] = mapped_column()
    pub_date: Mapped[str] = mapped_column()  # todo: use datetime type for pubDate
    description: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column()  # todo: add channel table and foreign key

    def __repr__(self):
        return f"Headline(id={self.id}, title={self.title}, pub_date={self.pub_date})"