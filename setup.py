# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="HellMBot",
    version="0.1",
    url="https://git.orudo.ru/trueold89/HellMBot",
    author="trueold89",
    author_email="trueold89@orudo.ru",
    description="Discord bot that will wake your friends up from full mute by putting them through 9 circles of hell",
    packages=["hellmbot"],
    install_requires=["discord.py"],
    entry_points={
        "console_scripts": ["hellm = hellmbot.bot:start"]
    }
)
