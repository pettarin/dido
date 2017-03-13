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

from flask import _request_ctx_stack
from flask import abort as _abort
from flask import current_app
from flask import url_for as _url_for
import re
import time

EMAIL_TEMPLATE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s.]+$")
"""
Simple regex to match email addresses.
"""


def timestamp():
    """
    Return the current timestamp as an integer.

    :rtype: int
    """
    return int(time.time())


def abort(status_code, message=None):
    """
    Enhanced ``abort()`` function which allows
    passing a simple error message.

    :param int status_code: the (error) status code
    :param str message: the (error) message
    """
    if message is None:
        message = "bad request"
    _abort(status_code, {"message": message})


def is_valid_email(email):
    """
    Check that the given email address is valid.

    Here "valid" means that matches the regex
    ``[^@\s]+@[^@\s]+\.[^@\s.]+$``.

    Note that this check is good enough for a first pass
    (I do not feel like using a more complex, external library
    for this),
    and that nothing can be said about the actual validity
    of the email address until an actual message is sent
    to it anyway.

    :param str email: the email address to be checked
    :rtype: bool
    """
    return re.match(EMAIL_TEMPLATE, email) is not None


def url_for(*args, **kwargs):
    """
    url_for replacement that works even
    when there is no request context.
    """
    if "_external" not in kwargs:
        kwargs["_external"] = False
    reqctx = _request_ctx_stack.top
    if reqctx is None:
        if kwargs["_external"]:
            raise RuntimeError("Cannot generate external URLs without a request context.")
        with current_app.test_request_context():
            return _url_for(*args, **kwargs)
    return _url_for(*args, **kwargs)
