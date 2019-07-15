# -*- coding: utf-8 -*-
from short_url import redis_store
from short_url.schema import add, load


CHAR_SET = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')


def encode(num: int):
    """
    将一个十进制的整数编码成六十二进制的字符串
    :param num:int, 待转化的数字
    :return:
    """
    if not isinstance(num, int):
        raise TypeError('The type of num should be int, while %s got.' % type(num))

    if num == 0:
        return CHAR_SET[0]

    res = []
    length = len(CHAR_SET)
    while num:
        num, remain = divmod(num, length)
        res.append(CHAR_SET[remain])

    return ''.join(reversed(res))


def shorten_url(url: str):
    """
    将短网址转化为62位编码的字符串
    :param url:
    :return:
    """
    num = int(redis_store.incr('SHORT_CNT'))  # 充当了计数器的角色
    token = encode(num)
    add(url, token)

    return token


def expand_url(token: str):
    """
    根据token返回数据库存储的原始url
    :param token:
    :return:
    """
    model = load(token)

    return model.url if model else ''
