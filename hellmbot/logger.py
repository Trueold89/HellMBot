# -*- coding: utf-8 -*-
from logging import getLogger, Formatter, StreamHandler, INFO
from sys import stdout as stdout

formatter = Formatter("[%(asctime)s] [%(levelname)s] %(message)s")


def setup_handler():
    console_handler = StreamHandler(stdout)
    console_handler.setFormatter(formatter)
    return console_handler


handler = setup_handler()


def setup_logger():
    log = getLogger(__name__)
    log.setLevel(INFO)
    log.addHandler(handler)
    return log


logger = setup_logger()
