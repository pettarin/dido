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

from flask import jsonify
from flask import Blueprint

api = Blueprint("api", __name__)

from . import organizations
from . import users


@api.app_errorhandler(400)
def api_400(e):
    message = "API bad request"
    try:
        message = e.description["message"]
    except:
        pass
    return jsonify({
        "code": 400,
        "message": message
    }), 400


@api.app_errorhandler(403)
def api_403(e):
    return jsonify({
        "code": 403,
        "message": "API requires authentication"
    }), 403


@api.app_errorhandler(404)
def api_404(e):
    return jsonify({
        "code": 404,
        "message": "API not found"
    }), 404


@api.app_errorhandler(500)
def api_500(e):
    return jsonify({
        "code": 500,
        "message": "API internal error"
    }), 500
