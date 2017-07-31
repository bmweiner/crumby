"""Default Settings."""

from os.path import join
from os.path import expanduser

DOMAIN = 'localhost:5000'
GEOIP2_DATABASE_NAME = join(expanduser('~'), 'GeoLite2-City.mmdb')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(expanduser('~'), 'crumby.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
