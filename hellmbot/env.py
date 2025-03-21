# -*- coding: utf-8 -*-

############################################################################
# Getting values from the system environment / defining standard constants #
############################################################################

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class ENV(BaseSettings):
    BOT_TOKEN: str = Field(description="Discord bot authorization token")
    CLIENT_ID: str = Field(description="Discord Client ID")
    DB_PATH: Optional[str] = Field(
        description="Path to sqlite database file",
        default="/etc/hellmbot/database.sqlite",
    )
    CIRCLES_COUNT: Optional[int] = Field(
        description="Count of channels to be created", default=9
    )


env = ENV()
