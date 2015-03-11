# coding: utf-8
from datetime import datetime
from ._base import db


class Book(db.Model):
    """Model for book"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    intro = db.Column(db.Text)
    cover = db.Column(db.String(200))
    amazon_url = db.Column(db.String(300))
    douban_url = db.Column(db.String(200))
    pub_date = db.Column(db.Date)
    press = db.Column(db.String(100))
    pages = db.Column(db.Integer)
    price = db.Column(db.Float)
    isbn = db.Column(db.String(50))

    def __repr__(self):
        return '<Book %s>' % self.title