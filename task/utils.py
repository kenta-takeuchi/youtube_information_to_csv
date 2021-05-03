import configparser
import datetime
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
config_ini = configparser.ConfigParser()
config_ini_path = os.path.join(BASE_DIR, 'config.ini')
config_ini.read(config_ini_path, encoding='utf-8')


def get_search_date_range():
    year = int(config_ini.get('YOUTUBE', 'YEAR'))
    month = int(config_ini.get('YOUTUBE', 'MONTH'))
    published_after = datetime.datetime(year=year, month=month, day=1).isoformat("T") + "Z"
    published_before = datetime.datetime(year=year, month=month + 1, day=1).isoformat("T") + "Z"
    return published_after, published_before


def iso_to_jstdt(iso_str):
    return datetime.datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SZ')
