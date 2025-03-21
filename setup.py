# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="HellMBot",
    version="0.3",
    url="https://github.com/Trueold89/HellMBot",
    author="trueold89",
    author_email="trueold89@orudo.ru",
    description="Discord bot that will wake your friends up from deafen by putting them through 9 circles of hell",
    packages=["hellmbot"],
    install_requires=["discord.py", "pydantic", "pydantic_settings", "aiosqlite"],
    entry_points={"console_scripts": ["hellm = hellmbot.bot:start"]},
)
