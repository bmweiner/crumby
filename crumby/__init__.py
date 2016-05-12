"""A Flask based web analytics app."""

__version__ = '0.2'

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils import geo_ip

app = Flask(__name__)
app.config.from_object('config')
dev_config = os.path.join(app.instance_path, 'config.py')
app.config.from_pyfile(dev_config, silent=True)

db = SQLAlchemy(app)

geo = geo_ip.Geo('geolite2_city', app.config.get('GEO_DB_URI', None))

import views

db.create_all()
