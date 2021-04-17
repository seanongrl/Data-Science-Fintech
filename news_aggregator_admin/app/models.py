# generated using sqlacodegen
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from app import db


news_categories_table = db.Table('news_categories', db.Model.metadata,
                           db.Column('news_id', db.Integer, db.ForeignKey('news.news_id')),
                           db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'))
                           )


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(60), nullable=False)

    # def __str__(self):
    #     return self.name  # tells flask-admin to display the name instead of the object (routes line 25)

    def __str__(self):
        return "{}".format(self.name)


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
    category = db.relationship('Category', secondary=news_categories_table)

    # category = relationship('Category', secondary="news_categories",
    #                         backref=db.backref('news', lazy='dynamic'))


# class NewsCategory(db.Model):
#     __tablename__ = 'news_categories'
#
#     newscat_id = Column(INTEGER(11), primary_key=True)
#     news_id = Column(
#         ForeignKey('news.news_id', ondelete='CASCADE', onupdate='CASCADE'),
#         unique=True)
#     category_id = Column(
#         ForeignKey('categories.category_id', ondelete='CASCADE',
#                    onupdate='CASCADE'), nullable=False, index=True)
#
#     category = relationship('Category')
#     news = relationship('News')

