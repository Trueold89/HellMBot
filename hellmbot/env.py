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

    @property
    def BOT_TOKEN(self) -> str:
        """
        Gets the Discord bot authorization token from the system environment

        :return: Discord bot token
        """
        env = environ.get("BOT_TOKEN")
        if env is None:
            raise ValueError("Bot token is not set\nTry to install the system ENV BOT_TOKEN\n(export "
                             "BOT_TOKEN=inserthereyourbottoken)")
        return env

    @property
    def CIRCLES_COUNT(self) -> int:
        """
        Sets count of channels to be created

        :return: Count of channels
        """
        env = environ.get("CIRCLES_COUNT")
        if env is None:
            env = 9
        return env
