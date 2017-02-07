"""A web analytics application."""

import os
import datetime
from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from .utils import geo_ip

app = Flask(__name__)
app.config.from_object('config')
dev_config = os.path.join(app.instance_path, 'config.py')
app.config.from_pyfile(dev_config, silent=True)

db = SQLAlchemy(app)

geo = geo_ip.Geo(app.config.get('GEOIP2_DB_PATH', None))

from .views import general
from .views import reporting
from .views import tracking

db.create_all()

# build calendar table
from .models import Calendar

def get_dates():
    start = datetime.date(2016, 1, 1)
    end = datetime.date.today() + datetime.timedelta(days=365*3)
    delta = end - start
    return [start + datetime.timedelta(days=i) for i in range(delta.days)]

Calendar.query.delete()  # truncate
for d in get_dates():
    db.session.add(Calendar(datetime=d))
db.session.commit()

# custom JSONEncoder
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder
