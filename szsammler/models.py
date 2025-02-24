from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, DateTime
from szsammler import db
from datetime import datetime


class Article(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str]= mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str] = mapped_column(String)
    # channel: Mapped[str] = mapped_column()  # TODO: add channel table and foreign key

    def __repr__(self):
        return f"Article(id={self.id}, title={self.title}, pub_date={self.pub_date})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "published": self.published.isoformat(),
            "description": self.description,
        }