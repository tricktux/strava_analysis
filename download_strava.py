# File:           download_strava.py
# Description:    Download strava data
# Author:		    Reinaldo Molina
# Email:          rmolin88 at gmail dot com
# Revision:	    0.0.0
# Created:        Wed Mar 27 2019 12:12
# Last Modified:  Wed Mar 27 2019 12:12

import configparser
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path

from splinter import Browser
from stravalib.client import Client

LOG_NAME = 'strava'


@dataclass
class LoginInfo:
    username: str
    password_method: str


@dataclass
class StravaInfo:
    code: str
    client_id: int
    client_secret: str
    redirect_uri: str
    scope: str


def get_strava_code(strava, login):
    """Use client id to get code"""
    logger = logging.getLogger(LOG_NAME)
    logger.debug('[get_strava_code]: client_id = %i', strava.client_id)
    browser = Browser()
    client = Client()
    url = client.authorization_url(
        client_id=strava.client_id,
        redirect_uri=strava.redirect_uri,
        scope=strava.scope)
    browser.visit(url)

    if login.username and login.password_method:
        browser.fill('email', login.username)
        browser.fill('password', login.password_method)
        browser.find_by_id('login-button').click()

    strava.code = input('Please enter code from response url:\n')
    logger.debug('[get_strava_code]: code = "%s"', strava.code)


def init_config(filename, config):
    """Check that filename exists and read the file"""
    logger = logging.getLogger(LOG_NAME)

    my_file = Path(filename)
    if not my_file.is_file():
        logger.fatal('[init_config]: Failed to read config: "%s"', filename)
        sys.exit("Failed to load config file")

    config.read(filename)


def init_log():
    """
    Initialize logging.
    Uses by default current directory to save log file
    Log name is LOG_NAME
    """

    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    logger = logging.getLogger(LOG_NAME)
    handler = RotatingFileHandler(
        '{}/'.format(DIRECTORY) + LOG_NAME + '.log',
        maxBytes=10**6,
        backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def load_strava_info(strava, config):
    """Load and check info from config.ini"""

    strava.client_id = int(config['Strava']['client_id'])
    strava.client_secret = config['Strava']['client_secret'].replace(
        '"', '').replace('\'', '')
    strava.redirect_uri = config['Strava']['redirect_uri'].replace(
        '"', '').replace('\'', '')
    strava.scope = config['Strava']['scope'].replace('"', '').replace('\'', '')

    if not strava.client_id:
        sys.exit("Emtpy client_id")
    if not strava.client_secret:
        sys.exit("Emtpy client_secret")
    if not strava.redirect_uri:
        sys.exit("Emtpy redirect_uri")
    if not strava.scope:
        sys.exit("Emtpy scope")


def get_login_info(login, config):
    """Get configuration file login info"""

    logger = logging.getLogger(LOG_NAME)
    login.username = config['Login']['username'].replace('"', '').replace(
        '\'', '')
    login.password_method = config['Login']['password_method'].replace(
        '"', '').replace('\'', '')

    if not login.password_method:
        return

    #  Attempt to get password
    cmd = login.password_method.replace('"', '')
    cmd = cmd.replace('\'', '')
    logger.debug('[get_login_info]: cmd = "%s"', cmd)
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    login.password_method = result.stdout.decode('utf-8')
    logger.debug('[get_login_info]: password = "%s"', login.password_method)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config_filename = 'config.ini'
    strava_info = StravaInfo
    login = LoginInfo

    init_log()
    init_config(config_filename, config)
    load_strava_info(strava_info, config)
    get_login_info(login, config)
    get_strava_code(strava_info, login)
    print(strava_info.code)
