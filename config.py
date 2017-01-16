"""Crumby prod configs."""

import os

DOMAIN = os.environ.get('OPENSHIFT_APP_DNS')
PKG = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR', '.'), 'crumby/')

db_url = os.environ.get('OPENSHIFT_MYSQL_DB_URL', '.')
app_name = os.environ.get('OPENSHIFT_APP_NAME', 'crumby')
SQLALCHEMY_DATABASE_URI = os.path.join(db_url, app_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False

data_dir = os.environ.get('OPENSHIFT_DATA_DIR', '.')
GEO_DB_URI = os.path.join(data_dir, 'GeoLite2-City.mmdb')
PROXY_COUNT = 0

CROSSDOMAIN_ORIGIN = 'http://bmweiner.com/'
