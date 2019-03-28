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
from logging.handlers import RotatingFileHandler
from pathlib import Path

from splinter import Browser
from stravalib.client import Client

LOG_NAME = 'strava'


def get_strava_code(api, login):
    """Use client id to get code"""
    logger = logging.getLogger(LOG_NAME)
    logger.debug('[get_strava_code]: client_id = %i', api['client_id'])

    if not login['username'] or not login['password_method']:
        logger.debug(
            '[get_strava_code]: no login info provided. using manual method')
        api['code'] = input('Please enter api code:\n')
        return

    browser = Browser()
    client = Client()
    url = client.authorization_url(
        client_id=api['client_id'],
        redirect_uri=api['redirect_uri'],
        scope=api['scope'])
    browser.visit(url)

    browser.fill('email', login['username'])
    browser.fill('password', login['password_method'])
    browser.find_by_id('login-button').click()
    time.sleep(0.5)
    #  There is an expected exception at this step
    try:
        browser.find_by_id('authorize').click()
    except:
        pass
    code = browser.url
    logger.debug('[get_strava_code]: raw_code = "%s"', code)
    browser.quit()
    api['code'] = parse_code_url(code)
    logger.debug('[get_strava_code]: code = "%s"', code)


def parse_code_url(raw_code):
    """Given a full http extract code"""
    logger = logging.getLogger(LOG_NAME)
    logger.debug('[parse_code_url]: raw_code: "%s"', raw_code)
    START_MAKER = "code="
    END_MARKER = "&"

    start = raw_code.find(START_MAKER) + len(START_MAKER)
    if not start:
        logger.fatal('[parse_code_url]: start: "%i"', start)
        sys.exit("Failed to find code")
    end = raw_code.rfind(END_MARKER)
    if not end:
        logger.fatal('[parse_code_url]: end: "%i"', end)
        sys.exit("Failed to find code")

    return raw_code[start:end]


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


def load_api_info(api, config):
    """Load and check info from config.ini"""

    api['client_id'] = int(config['ApiInfo']['client_id'])
    api['client_secret'] = config['ApiInfo']['client_secret']
    api['redirect_uri'] = config['ApiInfo']['redirect_uri']
    api['scope'] = config['ApiInfo']['scope']

    if not api['client_id']:
        sys.exit("Emtpy client_id")
    if not api['client_secret']:
        sys.exit("Emtpy client_secret")
    if not api['redirect_uri']:
        sys.exit("Emtpy redirect_uri")
    if not api['scope']:
        sys.exit("Emtpy scope")


def get_login_info(login, config):
    """Get configuration file login info"""

    logger = logging.getLogger(LOG_NAME)
    login['username'] = config['Login']['username']
    login['password_method'] = config['Login']['password_method']

    if not login['password_method']:
        return

    #  Attempt to get password
    cmd = login['password_method'].split(' ')
    logger.debug('[get_login_info]: cmd = "%s"', cmd)
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    login['password_method'] = result.stdout.decode('utf-8')
    if not login['password_method']:
        logger.fatal('[get_login_info]: failed to get password')
        sys.exit('failed to get password')


def get_access_token(api_info, token, config):
    """Exchanges temporary code for permanent access token"""
    logger = logging.getLogger(LOG_NAME)
    client = Client()
    access_token = client.exchange_code_for_token(
        client_id=api_info['client_id'],
        client_secret=api_info['client_secret'],
        code=api_info['code'])

    if not access_token:
        logger.critical('[get_access_token]: Failed to get access_token: "%s"',
                        access_token)
        sys.exit('Failed to get access_token')

    token = access_token.copy()
    logger.debug('[get_access_token]: access_token.access_token: "%s"',
                 token['access_token'])
    logger.debug('[get_access_token]: access_token.refresh_token: "%s"',
                 token['refresh_token'])
    logger.debug('[get_access_token]: access_token.expires_at: "%i"',
                 token['expires_at'])


def load_token(token, config):
    """Check to see if there is token info"""
    try:
        token['access_token'] = config['Token']['access_token']
        token['refresh_token'] = config['Token']['refresh_token']
        token['expires_at'] = config['Token']['expires_at']
    except:
        token['access_token'] = ''
        token['refresh_token'] = ''
        return


def write_access_token(token, config, filename):
    """Write access_token to config"""
    config['Token']['access_token'] = token['access_token']
    config['Token']['refresh_token'] = token['refresh_token']
    config['Token']['expires_at'] = token['expires_at']
    with open(filename, 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config_filename = 'config.ini'
    api_info = {
        'client_id': '',
        'client_secret': '',
        'redirect_uri': '',
        'scope': ''
    }
    login = {'username': '', 'password_method': ''}
    token = {'access_token': '', 'refresh_token': '', 'expires_at': ''}

    init_log()
    init_config(config_filename, config)
    load_token(token, config)
    if not token['access_token']:
        print('Loading token info...')
        load_api_info(api_info, config)
        get_login_info(login, config)
        print('Getting token code...')
        get_strava_code(api_info, login)
        get_access_token(api_info, token, config)
        print('Saving token...')
        write_access_token(token, config, config_filename)
    print('Got token info...')
