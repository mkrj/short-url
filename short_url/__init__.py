# -*- coding: utf-8 -*-
import os
import sys
import traceback

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from short_url.settings import config
from short_url.extensions import db, redis_store, migrate
from short_url.blueprints import main_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    redis_store.init_app(app)
    migrate.init_app(app, db)


def register_errorhandlers(app):
    @app.errorhandler(Exception)
    def errors(e):
        message = getattr(e, 'description', None) or getattr(e, 'msg', None) or str(e)

        error = {
            'code': str(getattr(e, 'code', 500)),
            'name': str(getattr(e, 'name', '')),
            'message': message
        }

        if app.debug or os.getenv('ENV') == 'dev':
            error['trace'] = traceback.format_exception(*sys.exc_info())
            # print(''.join(error['trace']))

        code = error['code'] if isinstance(e, HTTPException) else 500
        # 注：error['code'] 有可能是字符串，比如 SQL语法错误引起的 Exception

        return jsonify(error), int(code)


def register_blueprints(app):
    app.register_blueprint(main_bp)
