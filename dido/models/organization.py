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

from .. import db
from ..utils import timestamp
from .base import BaseModel


class Organization(BaseModel):
    """
    The model of an Organization,
    to be stored in table ``organizations``.
    """
    __tablename__ = "organizations"
    orgid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=True, unique=False)
    approval_method = db.Column(db.Integer, default=timestamp)
    approval_email = db.Column(db.String(256), nullable=True, unique=False)
    users = db.relationship("User", lazy="dynamic")

    ENUM_APPROVAL_NONE = 0
    ENUM_APPROVAL_SELF = 1
    ENUM_APPROVAL_ADMIN = 2

    FROM_FIELDS = [
        "name",
        "description",
        "approval_method",
        "approval_email",
    ]

    TO_FIELDS = [
        "orgid",
        "created_at",
        "updated_at",
        "name",
        "description",
        "approval_method",
        "approval_email",
    ]

    @staticmethod
    def create(data):
        """
        Create a new organization.

        :param dict data: the new data to put into this organization
        """
        organization = Organization()
        organization.from_dict(data, partial_update=False)
        return organization

    @staticmethod
    def list_all():
        """
        Return a list of ``Organization`` objects,
        representing all the organizations in the database,
        sorted alphabetically by name.

        :rtype: list
        """
        return Organization.query.order_by(Organization.name.asc()).all()

    @staticmethod
    def query_by_id(orgid):
        """
        Return the organization with the given id
        (or ``None`` if not found).

        :param int orgid: the id of the organization to check
        :rtype: ``Organization``
        """
        return Organization.query.filter_by(orgid=orgid).first()

    @staticmethod
    def exists(orgid):
        """
        Check whether an organization with the given id exists.

        :param int orgid: the id of the organization to check
        :rtype: bool
        """
        return Organization.query_by_id(orgid) is not None
