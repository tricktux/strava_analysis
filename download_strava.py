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

LOG_NAME = 'strava'
#  from stravalib.client import Client
#  import pandas as pd


@dataclass
class StravaInfo:
    code: str
    client_id: str
    client_secret: str


def get_code():
    """Use client id to get code"""
    browser = Browser()


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

    strava.client_id = config['Strava']['client_id']
    strava.code = config['Strava']['code']
    strava.client_secret = config['Strava']['client_secret']

    if not strava.client_id:
        sys.exit("Emtpy client_id")
    if not strava.code:
        sys.exit("Emtpy code")
    if not strava.client_secret:
        sys.exit("Emtpy client_secret")


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config_filename = 'config.ini'
    strava_info = StravaInfo

    init_log()
    init_config(config_filename, config)
    load_strava_info(strava_info, config)
