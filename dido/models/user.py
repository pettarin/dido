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

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .. import db
from ..utils import abort
from ..utils import timestamp
from .base import BaseModel


class User(BaseModel):
    """
    The model of a User,
    to be stored in table ``users``.
    """
    __tablename__ = "users"
    userid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    name = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    accepted_tos = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    organization = db.Column(db.Integer, db.ForeignKey("organizations.orgid"))

    FROM_FIELDS = [
        "name",
        "email",
        "password",
        "accepted_tos",
        "active",
        "deleted",
        "organization",
    ]

    TO_FIELDS = [
        "userid",
        "created_at",
        "updated_at",
        "name",
        "email",
        "accepted_tos",
        "active",
        "deleted",
        "organization",
    ]

    def revoke_tokens(self):
        # TODO
        pass

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password_raw):
        self.password_hash = generate_password_hash(password_raw)
        self.revoke_tokens()

    def verify_password(self, password_raw):
        return check_password_hash(self.password_hash, password_raw)

    @staticmethod
    def create(data):
        """
        Create a new user.

        :param dict data: the new data to put into this user
        """
        user = User()
        user.from_dict(data, partial_update=False)
        return user

    def delete(self):
        if self.deleted:
            abort(400, "user already deleted")
        if not self.active:
            abort(400, "user not active")
        self.deleted = True
        self.save()
        self.revoke_tokens()

    def activate(self):
        if self.deleted:
            abort(400, "user deleted")
        if self.active:
            abort(400, "user already active")
        self.active = True
        self.save()

    @staticmethod
    def query_by_id(userid):
        """
        Return the user with the given id
        (or ``None`` if not found).

        :param int userid: the id of the user to check
        :rtype: ``User``
        """
        return User.query.filter_by(userid=userid).first()

    @staticmethod
    def query_by_name_email(name, email=None):
        """
        Return the user with the given name and email
        (or ``None`` if not found).

        :param str name: the name of the user to check
        :param str email: the email of the user to check
        :rtype: ``User``
        """
        if email is None:
            return User.query.filter_by(name=name).first()
        return User.query.filter_by(name=name, email=email).first()

    @staticmethod
    def exists(name, email):
        return User.query_by_name_email(name, email) is not None
