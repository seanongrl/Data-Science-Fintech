# generated using sqlacodegen
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(60), nullable=False)


class News(db.Model):
    __tablename__ = 'news'
    __searchable__ = ['title']

    news_id = Column(INTEGER(11), primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    dt = Column(DateTime, nullable=False)
    source = Column(String(60), nullable=False)
    image = Column(Text)
    link = Column(Text, nullable=False)


class NewsCategory(db.Model):
    __tablename__ = 'news_categories'

    newscat_id = Column(INTEGER(11), primary_key=True)
    news_id = Column(ForeignKey('news.news_id', ondelete='CASCADE', onupdate='CASCADE'), unique=True)
    category_id = Column(ForeignKey('categories.category_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    category = relationship('Category')
    news = relationship('News')


