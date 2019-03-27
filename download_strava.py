# File:           download_strava.py
# Description:    Download strava data
# Author:		    Reinaldo Molina
# Email:          rmolin88 at gmail dot com
# Revision:	    0.0.0
# Created:        Wed Mar 27 2019 12:12
# Last Modified:  Wed Mar 27 2019 12:12

import configparser
import time
from splinter import Browser
import os
import logging
from logging.handlers import RotatingFileHandler

CONFIG_FILENAME = 'config.ini'
LOG_NAME = 'strava'
BROWSER = Browser()
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
from stravalib.client import Client
import pandas as pd

client = Client()
code = ''
client_id = 12345
client_secret = ''

year = 2018
resolution = 'high'
types = ['time', 'altitude', 'heartrate', 'temp', 'distance', 'watts']

access_token = client.exchange_code_for_token(
    client_id=client_id, client_secret=client_secret, code=code)

client = Client(access_token=access_token)
df_overview = pd.DataFrame()
activities = dict()

for activity in client.get_activities(
        after='{}-01-01T00:00:00Z'.format(str(year)),
        before='{}-01-01T00:00:00Z'.format(str(year + 1))):
    streams = client.get_activity_streams(
        activity.id, types=types, series_type='time', resolution=resolution)
    for key, value in streams.items():
        streams[key] = value.data

    df_overview = df_overview.append(
        pd.DataFrame(
            [{
                'Name': activity.name,
                'Date': activity.start_date,
                'Moving Time [min]': int(activity.moving_time.seconds / 60),
                'Distance [km]': round(activity.distance.num / 1000, 1),
                'Measurements': list(streams.keys())
            }],
            index=[activity.id]))

    activities[activity.id] = pd.DataFrame(streams)

writer = pd.ExcelWriter(
    'strava_export_{}.xlsx'.format(str(year)), engine='openpyxl')
df_overview.to_excel(writer, "Overview")

for activity_id, df in activities.items():
    df.to_excel(
        writer, ' '.join([
            str(df_overview.loc[activity_id]['Date'].date()),
            df_overview.loc[activity_id]['Name']
        ])[:30])

    writer.save()


def get_code():
    """Use client id to get code"""
    pass


def get_config():
    """Read client id and client secret from config"""
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILENAME)
    except:
        print('[]')


def init_log():
    """
    Initialize logging.
    Uses by default DIRECTORY
    """

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


if __name__ == '__main__':
    init_log()
    get_config()
    get_code()
