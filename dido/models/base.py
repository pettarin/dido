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
from ..utils import abort

class BaseModel(db.Model):
    __abstract__ = True

    FROM_FIELDS = []
    TO_FIELDS = []

    def save(self):
        """
        Save the current edits to the db.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except:
            abort(400, "unable to save data")

    def from_dict(self, data, partial_update=True):
        """
        Import data from a dictionary.

        :param obj model: the object model
        :param dict data: the new data to put into this object
        :param bool partial_update: if ``True``, allow partial updates
        """
        for field in self.FROM_FIELDS:
            try:
                setattr(self, field, data[field])
            except KeyError:
                if not partial_update:
                    abort(400, "missing key %s" % field)

    def to_dict(self):
        """
        Export object data to a dictionary.
        """
        data = {}
        for field in self.TO_FIELDS:
            data[field] = getattr(self, field)
        return data
