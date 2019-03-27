# File:           password.py
# Description:    Attempt as many usernames as possible
# Author:		    Reinaldo Molina
# Email:          rim18 at psu dot edu
# Revision:	    0.0.0
# Created:        Sat Feb 02 2019 15:43
# Last Modified:  Sat Feb 02 2019 15:43

import time
from splinter import Browser
import os
import logging
from logging.handlers import RotatingFileHandler

BROWSER = Browser()
DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def init_log():
    """
    Initialize logging.
    Uses by default DIRECTORY
    """

    logger = logging.getLogger("browser")
    handler = RotatingFileHandler(
        '{}/browser.log'.format(DIRECTORY), maxBytes=10**6, backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def sign_in():
    """Sign in"""
    link = 'http://localhost:18888/WebGoat/start.mvc#lesson/PasswordReset.lesson/3'
    BROWSER.visit(link)
    BROWSER.fill('username', 'rmolin88')
    BROWSER.fill('password', 'rmolin88')
    BROWSER.find_by_text('Sign in').click()


def find_lesson(name):
    """activate lesson"""
    logger = logging.getLogger("browser")
    for lesson in name:
        logger.debug('[find_lesson]: lesson = "%s"', lesson)
        BROWSER.find_by_text(lesson).click()
        time.sleep(1)


if __name__ == '__main__':
    init_log()
    sign_in()
    link = 'http://localhost:18888/WebGoat/start.mvc#lesson/PasswordReset.lesson/3'
    BROWSER.visit(link)
    BROWSER.fill('username', 'rmolin88')
    BROWSER.fill('securityQuestion', 'red')
    BROWSER.find_by_text('Submit').click()
