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
from flask import request

from ..models import User
from ..models import Organization
from ..utils import abort
from ..utils import is_valid_email

from . import api


@api.route("/users/register", methods=["POST"])
def new_user():
    """
    Register a new user.
    This endpoint is publicly available.
    """
    req = request.get_json()

    # validate request
    fields = [
        ("name", "name required"),
        ("email", "email address required"),
        ("password", "password required"),
        ("password_confirm", "password confirm required"),
        ("organization", "organization id required"),
        ("accept_tos", "accept_tos required"),
    ]
    for field, msg in fields:
        if field not in req:
            abort(400, msg)
    if req["password"] != req["password_confirm"]:
        abort(400, "password and password_confirm not matching")
    if not req["accept_tos"]:
        abort(400, "tos must be accepted")
    if not is_valid_email(req["email"]):
        abort(400, "invalid email address")
    if User.exists(req["name"], req["email"]):
        abort(400, "user already existing")
    if not Organization.exists(req["organization"]):
        abort(400, "invalid organization id")

    # here the request seems valid

    # add user, but do not activate it yet
    user = User.create({
        "name": req["name"],
        "email": req["email"],
        "password": req["password"],
        "accepted_tos": True,
        "active": False,
        "deleted": False,
        "organization": req["organization"],
    })
    user.save()

    # check the validation required by the organization
    org = Organization.query_by_id(user.organization)
    if org.approval_method == Organization.ENUM_APPROVAL_NONE:
        # no approval required
        user.activate()
    elif org.approval_method == Organization.ENUM_APPROVAL_SELF:
        # self approval required => send email to user address
        # TODO
        print("self approval => send email!")
    else:
        # admin approval required => send email to admin address
        # TODO
        print("admin approval => send email!")

    res = {
        "code": 200,
        "message": "success",
        "userid": user.userid
    }
    return jsonify(res)
