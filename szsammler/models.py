from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from szsammler import db
from datetime import datetime
from urllib.parse import urlparse


class Article(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[datetime] = mapped_column(DateTime)
    description: Mapped[str] = mapped_column(String)
    channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("channel.id", ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Article({self.id=}, {self.title=})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "published": self.published.isoformat(),
            "description": self.description,
        }


class Channel(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    articles: Mapped[List["Article"]] = relationship("Article", backref="articles", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"Channel({self.id=}, {self.title=})"
    
    def get_image_url(self):
        """Use duckduckgo's icon api if the rss channel does not provide an image-url."""
        if (self.image_url is None):
            url = urlparse(self.link)
            domain = str.split(url.netloc, ".", 1)[-1]
            ddg_url = f"https://icons.duckduckgo.com/ip3/{domain}.ico"
            return ddg_url
        else:
            return self.image_url
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "image_url": self.get_image_url(),
        }
    
