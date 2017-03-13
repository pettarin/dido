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

from flask_script import Command
from flask_script import Manager
import subprocess
import sys

from dido import create_app
from dido import create_db


class CeleryWorker(Command):
    """
    Start the celery worker.
    """
    name = "celery"
    capture_all_args = True

    def run(self, argv):
        ret = subprocess.call([
            "celery",
            "worker",
            "-A",
            "dido.celery"
        ] + argv)
        sys.exit(ret)


manager = Manager(create_app)
manager.add_command("celery", CeleryWorker())


@manager.command
def createdb(drop_first=False):
    """
    Create the app database.

    :param bool drop_first: if ``True``, drop all existing tables first,
                            if any.
    """
    create_db(drop_first=drop_first)


@manager.command
def test():
    """
    Runs unit tests.
    """
    tests = subprocess.call([
        "python",
        "-c",
        "import tests; tests.run()"
    ])
    sys.exit(tests)


if __name__ == "__main__":
    manager.run()
