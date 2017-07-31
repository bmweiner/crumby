"""Routes for tracking."""

import os
import base64
from datetime import datetime
from urllib import unquote
from flask import request
from flask import Response
from flask import render_template
from flask import abort
from .. import app
from .. import db
from .. import geo
from ..models import Visit
from ..models import Event
from ..extensions import security

# cmb.js
with app.app_context():
    cmbjs = render_template('cmb.js', domain=app.config['DOMAIN'])
    cmbjs = cmbjs.replace('\n','').replace('  ','')

@app.route('/cmb.js')
def serve_cmbjs():
    """Serve cmb.js script."""
    response = Response(cmbjs, mimetype='text/javascript')
    response.cache_control.max_age = 900  # 15 minutes
    return response

# one pixel gif
val = 'R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
one_pxl = base64.b64decode(val)

@app.route('/<int:gif_id>.gif')
def parse_query_string(gif_id):
    """Parse gif query string and store in db."""
    if not request.args.get('cid'):
        abort(404)

    query_type = request.args.get('t')
    ip = security.real_ip(request, app.config.get('PROXY_COUNT', 0))

    if query_type == 'visit':
        geo_data = geo.query(ip)
        data = dict(ip=ip,
                    cid=request.args.get('cid'),
                    datetime=datetime.utcnow(),
                    doc_title=unquote(request.args.get('dt')),
                    doc_uri=unquote(request.args.get('dl')),
                    doc_enc=request.args.get('de'),
                    referrer=unquote(request.args.get('dr')),
                    _referrer=getattr(request, 'referrer', None),
                    platform=getattr(request.user_agent, 'platform', None),
                    browser=getattr(request.user_agent, 'browser', None),
                    version=getattr(request.user_agent, 'version', None),
                    screen_res=request.args.get('sr'),
                    screen_depth=request.args.get('sd'),
                    continent=geo_data.get('continent', None),
                    country=geo_data.get('country', None),
                    subdivision_1=geo_data.get('subdivision_1', None),
                    subdivision_2=geo_data.get('subdivision_2', None),
                    city=geo_data.get('city', None),
                    latitude=geo_data.get('latitude', None),
                    longitude=geo_data.get('longitude', None),
                    accuracy_radius=geo_data.get('accuracy_radius', None),
                    time_zone=geo_data.get('time_zone', None),
                    lang=request.args.get('ul'),
                    _lang=getattr(request.user_agent, 'language', None),)
        db.session.add(Visit(**data))
        db.session.commit()
    elif query_type == 'event':
        data = dict(ip=ip,
                    cid=request.args.get('cid'),
                    datetime=datetime.utcnow(),
                    doc_title=request.args.get('dt'),
                    doc_uri=request.args.get('dl'),
                    name=request.args.get('en'),
                    value=request.args.get('ev'),
                    )
        db.session.add(Event(**data))
        db.session.commit()
    else:
        print('Invalid request type: {}'.format(query_type))

    return Response(one_pxl, mimetype='image/gif')
