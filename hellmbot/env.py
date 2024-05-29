# -*- coding: utf-8 -*-
from os import environ


############################################################################
# Getting values from the system environment / defining standard constants #
############################################################################


class ENV(object):

    @property
    def DB_PATH(self) -> str:
        """
        Sets the path to the sqlite database file

        :return: Path to DataBase file
        """
        default = "/etc/hellmbot/database.sqlite"
        env = environ.get("DB_PATH")
        if env is None:
            return default
        return env
