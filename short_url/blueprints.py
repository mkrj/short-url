# -*- coding: utf-8 -*-
import os

from flask import jsonify, request, Blueprint
from short_url.core import shorten_url, expand_url


main_bp = Blueprint('main', __name__)


@main_bp.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.json['url']
    token = shorten_url(long_url)

    if os.getenv('HOST').endswith('/'):
        short_url = os.getenv('HOST') + token
    else:
        short_url = os.getenv('HOST') + '/' + token

    return jsonify(short_url)


@main_bp.route('/expand', methods=['POST'])
def expand():
    short_url = request.json['url']
    token = short_url.rsplit('/')[-1]
    url = expand_url(token)
    if url:
        return jsonify(url)
    else:
        return jsonify('The origin url is not exist.'), 422


@main_bp.route('/', methods=['GET'])
def index():

    return jsonify('Hello!')
