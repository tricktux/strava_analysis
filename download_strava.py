# File:           download_strava.py
# Description:    Download strava data
# Author:		    Reinaldo Molina
# Email:          rmolin88 at gmail dot com
# Revision:	    0.0.0
# Created:        Wed Mar 27 2019 12:12
# Last Modified:  Wed Mar 27 2019 12:12

import sys
import configparser
import time
from splinter import Browser
import os
import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass
from pathlib import Path
from stravalib.client import Client
import subprocess

LOG_NAME = 'strava'


@dataclass
class LoginInfo:
    username: str
    password_method: str


@dataclass
class StravaInfo:
    client_id: int
    client_secret: str
    redirect_uri: str
    scope: str


def get_strava_code(strava):
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
    strava.client_secret = config['Strava']['client_secret']
    strava.redirect_uri = config['Strava']['redirect_uri']
    strava.scope = config['Strava']['scope']

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
    login.username = config['Login']['username']
    login.password_method = config['Login']['password_method']

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
    #  get_strava_code(strava_info)
