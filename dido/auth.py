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

from flask import g
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from flask_httpauth import HTTPTokenAuth

from . import db
from .models import User
from .utils import abort

# Authentication objects for username/password auth, token auth, and
# a token optional auth that is used for open endpoints.
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth("Bearer")
token_optional_auth = HTTPTokenAuth("Bearer")

# no authentication (useful for debug)
no_auth = HTTPBasicAuth()


@no_auth.verify_password
def no_verify_password(name, password_raw):
    return False


@no_auth.error_handler
def no_password_error():
    abort(401, "authentication required")


@basic_auth.verify_password
def verify_password(name, password_raw):
    """
    Password verification callback.
    """
    if (not name) or (not password_raw):
        return False
    user = User.query_by_id(name=name)
    if (user is None) or (not user.verify_password(password_raw)):
        return False
    g.current_user = user
    return True


@basic_auth.error_handler
def password_error():
    """
    Return a 401 error to the client.
    """
    # TODO: abort(401, "authentication required")
    # To avoid login prompts in the browser, use the "Bearer" realm.
    return (
        jsonify({"error": "authentication required"}),
        401,
        {"WWW-Authenticate": "Bearer realm=\"Authentication Required\""}
    )


@token_auth.verify_token
def verify_token(token):
    """Token verification callback."""
    user = User.query.filter_by(token=token).first()
    if user is None:
        return False
    user.ping()
    db.session.add(user)
    db.session.commit()
    g.current_user = user
    return True


@token_auth.error_handler
def token_error():
    """
    Return a 401 error to the client.
    """
    # TODO: abort(401, "authentication required")
    # To avoid login prompts in the browser, use the "Bearer" realm.
    return (
        jsonify({"error": "authentication required"}),
        401,
        {"WWW-Authenticate": "Bearer realm=\"Authentication Required\""}
    )


@token_optional_auth.verify_token
def verify_optional_token(token):
    """
    Alternative token authentication that allows anonymous logins.
    """
    if token == "":
        # no token provided, mark the logged in users as None and continue
        g.current_user = None
        return True
    # but if a token was provided, make sure it is valid
    return verify_token(token)
