# -*- coding: utf-8 -*-
from short_url import db
from short_url.models import ShortUrl


def add(url: str, token: str):
    model = ShortUrl(url=url, token=token)
    db.session.add(model)
    db.session.commit()


def load(token: str) -> ShortUrl:

    return db.session.query(ShortUrl).filter(ShortUrl.token == token).first()
