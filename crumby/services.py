"""Crumby services."""

import os
import warnings
import datetime
import urllib
import hashlib
import gzip
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from . import app
from . import db
from .models import User
from .models import Calendar


def view_env():
    return app.config

def update_geoip(path):
    url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.md5'
    md5 = urllib.urlopen(url).read()

    url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
    tempfile, headers = urllib.urlretrieve(url)

    with gzip.open(tempfile, 'rb') as f:
        file_content = f.read()

    if hashlib.md5(file_content).hexdigest() != md5:
        raise AssertionError('GeoLite2-City.mmdb MD5 check failed!')

    with open(path, 'wb') as f:
        f.write(file_content)

    os.remove(tempfile)

def view_users():
    return [user.username for user in User.query.all()]

def add_user(username, password):
    validate_username(username)
    validate_password(password)
    u = User(username=username, password=password)
    try:
        db.session.add(u)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        warnings.warn("Username '{}' already exists.".format(username))
        return
    return True

def delete_user(username):
    validate_username(username)
    u = User.query.filter_by(username=username).first()
    try:
        db.session.delete(u)
        db.session.commit()
    except UnmappedInstanceError as err:
        db.session.rollback()
        warnings.warn("Username '{}' does not exist.".format(username))
        return
    return True

def validate_username(username):
    root = 'Username must be '
    rules = [{'logic':username is None, 'err':'greater than 0 characters'}]
    for rule in rules:
        if rule['logic']:
            raise ValueError(root + rule['err'])

def validate_password(password):
    root = 'Password must be '
    rules = [{'logic':password is None, 'err':'greater than 0 characters'}]
    for rule in rules:
        if rule['logic']:
            raise ValueError(root + rule['err'])

def update_calendar(start, end):
    """Update calendar with dates between start and end.

    Args:
        start: datetime.
        end: datetime.
    """
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = end - start
    dates = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    Calendar.query.delete()  # truncate
    for d in dates:
        db.session.add(Calendar(datetime=d))
    db.session.commit()
