# -*- coding: utf-8 -*-
from short_url import db
from sqlalchemy.sql import func


class ShortUrl(db.Model):
    __tablename__ = 'short_urls'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    token = db.Column(db.String(10), nullable=False, index=True)
    created_at = db.Column(db.TIMESTAMP(), nullable=False, server_default=func.now())
