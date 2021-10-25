# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""main.py

Creates a Flask app instance and registers various services and middleware.
"""

from flask import Flask, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
from sweetrpg_library_web.application.cache import cache
from sweetrpg_library_web.application import constants
from logging.config import dictConfig
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
import analytics
import os


ENV_FILE = find_dotenv()
if ENV_FILE:
    print(f"Loading environment from {ENV_FILE}...")
    load_dotenv(ENV_FILE)


def create_app(app_name=constants.APPLICATION_NAME):
    print("Configuring logging...")
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s %(module)s/%(funcName)s: %(message)s",
                },
                "logstash": {
                    "class": "logstash_async.formatter.FlaskLogstashFormatter",
                    "metadata": {"beat": "sweetrpg-COMPONENT-web"},
                }
            },
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "default"},
                         "logstash": {"class": "logstash_async.handler.AsynchronousLogstashHandler", "formatter": "logstash",
                                      "host": os.environ[constants.LOGSTASH_HOST],
                                      "port": int(os.environ[constants.LOGSTASH_PORT]),
                                      "database_path": "/tmp/sweetrpg_COMPONENT_web_flask_logstash.db",
                                      "transport": "logstash_async.transport.BeatsTransport",
                                      }},
            "root": {"level": os.environ.get(constants.LOG_LEVEL) or "INFO", "handlers": ["wsgi", "logstash"]},
        }
    )

    app = Flask(app_name)
    app.debug = app.config["DEBUG"]
    app.config.from_object("sweetrpg_COMPONENT_web.application.config.BaseConfig")
    # env = DotEnv(app)

    app.logger.info("Setting up cache...")
    cache.init_app(app)

    # app.logger.info("Setting up cache...")
    # oauth.init_app(app)

    app.logger.info("Setting up analytics...")
    analytics.write_key = app.config.get("SEGMENT_WRITE_KEY")
    analytics.debug = app.config.get("DEBUG") or False

    app.logger.info("Setting up session manager...")
    session = Session(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    if not app.debug:
        app.logger.info("Setting up Sentry...")
        sentry = SentryWsgiMiddleware(app)

    app.logger.info("Setting up endpoints...")

    # from sweetrpg_library_web.application.blueprints.volumes import blueprint as volumes_blueprint
    # app.register_blueprint(volumes_blueprint, url_prefix="/volumes")

    from sweetrpg_web_core.blueprints.health import blueprint as health_blueprint

    app.register_blueprint(health_blueprint, url_prefix="/health")

    vue = Vue(app)

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'application': ('static/sass', 'static/css', '/static/css')
    })
    scss = Scss(app, static_dir='static', asset_dir='assets')

    print(app.url_map)

    return app
