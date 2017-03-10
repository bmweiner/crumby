"""Crumby prod configs."""

import os

SECRET_KEY = os.urandom(24)
#SESSION_COOKIE_SECURE = True
DOMAIN = os.environ.get('OPENSHIFT_APP_DNS')

db_url = os.environ.get('OPENSHIFT_MYSQL_DB_URL', '.')
SQLALCHEMY_DATABASE_URI = os.path.join(db_url, 'crumby')
SQLALCHEMY_TRACK_MODIFICATIONS = False

filepath = os.environ.get('OPENSHIFT_DATA_DIR', '.')
GEOIP2_DB_PATH = os.path.join(filepath, 'GeoLite2-City.mmdb')
PROXY_COUNT = 0

CROSSDOMAIN_ORIGIN = 'http://bmweiner.com'

