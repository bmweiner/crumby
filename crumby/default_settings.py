"""Default Settings."""

from os.path import join
from os.path import expanduser

DOMAIN = 'localhost:5000'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(expanduser('~'), 'crumby.db')
