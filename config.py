"""Crumby prod configs."""

import os

data_dir = os.environ.get('OPENSHIFT_DATA_DIR', '.')

try:
    with open(os.path.join(data_dir, 'key')) as f:
        SECRET_KEY = f.read().strip(r'\n')

except IOError:
    pass

SESSION_COOKIE_SECURE = True
DOMAIN = os.environ.get('OPENSHIFT_APP_DNS')

db_url = os.environ.get('OPENSHIFT_MYSQL_DB_URL', '.')
SQLALCHEMY_DATABASE_URI = os.path.join(db_url, 'crumby')
SQLALCHEMY_TRACK_MODIFICATIONS = False

GEOIP2_DB_PATH = os.path.join(data_dir, 'GeoLite2-City.mmdb')
PROXY_COUNT = 0

CROSSDOMAIN_ORIGIN = 'http://bmweiner.com'
