"""A web analytics application."""

import os
import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .extensions import geo_ip
from .extensions import encoding

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('crumby.default_settings')
app.config.from_envvar('CRUMBY_SETTINGS', silent=True)
app.config.from_pyfile('crumby.cfg', silent=True)

app.json_encoder = encoding.CustomJSONEncoder

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
geo = geo_ip.Geo(app.config.get('GEOIP2_DATABASE_NAME', ''))

from . import services
from . import models
from .views import reporting
from .views import tracking

db.create_all()

# init or update calendar table
Calendar = models.Calendar
Visit = models.Visit
end = datetime.datetime.today() + datetime.timedelta(3*365)

# calendar is empty
if not Calendar.query.first():
    start = datetime.datetime.today() - datetime.timedelta(365)
    services.update_calendar(start, end)

calendar_first = Calendar.query.order_by(Calendar.datetime.asc()).first()
calendar_last = Calendar.query.order_by(Calendar.datetime.desc()).first()
visit_first = Visit.query.order_by(Visit.datetime.asc()).first()

# visit before calendar min
if visit_first and visit_first.datetime < calendar_first.datetime:
    start = visit_first.datetime
    services.update_calendar(start, end)

# today after calendar max
if datetime.datetime.today() >= calendar_last.datetime:
    start = calendar_first.datetime
    services.update_calendar(start, end)
