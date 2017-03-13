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

from flask import jsonify, g

from .. import db
from ..auth import basic_auth, token_auth

from . import api


@api.route("/tokens", methods=["POST"])
@basic_auth.login_required
def new_token():
    """
    Request a user token.
    This endpoint requires basic auth with nickname and password.
    """
    if g.current_user.token is None:
        g.current_user.generate_token()
        db.session.add(g.current_user)
        db.session.commit()
    return jsonify({"token": g.current_user.token})


@api.route("/tokens", methods=["DELETE"])
@token_auth.login_required
def revoke_token():
    """
    Revoke a user token.
    This endpoint requires a valid user token.
    """
    g.current_user.token = None
    db.session.add(g.current_user)
    db.session.commit()
    return "", 204
