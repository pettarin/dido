#!/usr/bin/env python
# coding=utf-8

# dido is an API server and Web application for the aeneas forced aligner
#
# Copyright (C) 2017, Alberto Pettarin (www.albertopettarin.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from config import config

"""
**dido** is an API server and Web application for the **aeneas** forced aligner
"""

__author__ = "Alberto Pettarin"
__email__ = "dido@readbeyond.it"
__copyright__ = "Copyright 2017, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "GNU AGPL v3"
__status__ = "Planning"
__version__ = "0.0.1"


# Flask extensions
db = SQLAlchemy()
# celery = Celery(
#     __name__,
#     broker=os.environ.get("CELERY_BROKER_URL", "redis://"),
#     backend=os.environ.get("CELERY_BROKER_URL", "redis://")
# )

# Import models so that they are registered with SQLAlchemy
from . import models

# Import celery task so that it is registered with the Celery workers
# from .tasks import run_flask_request


def create_db(drop_first=False):
    """
    Create the database.

    :param bool drop_first: if ``True``, drop all existing tables first,
                            if any.
    """
    if drop_first:
        db.drop_all()
    db.create_all()


def create_app(config_name=None):
    """
    Create the Flask app object,
    configure it, and
    register all the API/frontend blueprints.

    If ``config_name`` is ``None``, try
    reading the ``DIDO_CONFIG`` OS environment variable,
    and, if not found, use ``development``.

    :param str config_name: name of the app configuration to run.
    """
    if config_name is None:
        config_name = os.environ.get("DIDO_CONFIG", "development")
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # initialize flask extensions
    db.init_app(app)
    # celery.conf.update(config[config_name].CELERY_CONFIG)

    # register front-end routes
    from .fe import fe as fe_blueprint
    app.register_blueprint(fe_blueprint)

    # register API routes
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # register async tasks support
    # from .tasks import tasks_bp as tasks_blueprint
    # app.register_blueprint(tasks_blueprint, url_prefix="/tasks")

    return app
