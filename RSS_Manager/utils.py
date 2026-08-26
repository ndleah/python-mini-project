import os
from datetime import datetime
from typing import Dict, List, Optional

import feedparser
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

db_path = os.path.join(os.path.dirname(__file__), "subscriptions.db")
engine = create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase):
    pass

class Subscription(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[Optional[str]]
    link: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        return f"Feed(id={self.id!r}, url={self.url!r},title={self.title},tag={self.tag!r},link={self.link!r})"

Base.metadata.create_all(bind=engine)

def add_feed_to_db(url: str, title: str, tag: str | None, link: str):
    with Session(engine) as session:
        session.add(Subscription(url=url, title=title, tag=tag, link=link))
        session.commit()

def get_all_feeds():
    with Session(engine) as session:
        feeds = session.query(Subscription).all()
        return feeds

def get_feed_by_id(feed_id: int):
    with Session(engine) as session:
        feed = session.query(Subscription).filter(Subscription.id == feed_id).first()
        return feed

def get_articles_for_feed(feed_id: int):
    feed_db = get_feed_by_id(feed_id)
    if not feed_db:
        return []
    feed = Feed(feed_db.url)
    return feed.articles()

def delete_feed_from_db(url: str):
    with Session(engine) as session:
        feed = session.query(Subscription).filter(Subscription.url == url).first()
        if feed:
            session.delete(feed)
            session.commit()

class Feed:
    def __init__(self, url: str, tag: str | None = None) -> None:
        self.rss_feed: str = url
        self.tag: str | None = tag
        self.feed_parse = feedparser.parse(url)
        feed_info = getattr(self.feed_parse, 'feed', {})
        self.title: str = getattr(feed_info, 'title', url)
        self.link: str = getattr(feed_info, 'link', url)

    def articles(self) -> List[Dict[str, any]]:
        """list all the articles of Feed"""
        articles = []
        for entry in getattr(self.feed_parse, 'entries', []):
            pub_parsed = getattr(entry, 'published_parsed', None)
            pub_date = datetime(*pub_parsed[:6]) if pub_parsed else datetime.now()
            article = {
                "title": getattr(entry, 'title', 'Untitled'),
                "link": getattr(entry, 'link', '#'),
                "published_parsed": pub_date,
            }
            articles.append(article)
        return articles

    def __str__(self) -> str:
        return f"{self.title} -> {self.link}"

    def __repr__(self) -> str:
        return f"Feed({self.title})"

