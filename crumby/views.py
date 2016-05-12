"""Crumby views."""

import os
import base64
from datetime import datetime
from flask import request, Response, abort
from . import app, db, geo
from .models import Crumb

# one pixel gif
val = 'R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
one_pxl = base64.b64decode(val)

# cmb.js template
with open(os.path.join(app.config['PKG'], 'templates/cmb.js')) as f:
    cmbjs = f.read().replace('\n','').replace('  ','') % app.config['DOMAIN']

@app.route('/<int:gif_id>.gif')
def traffic(gif_id):
    """Parse traffic from gif query string and stores in db."""
    if not request.args.get('cid'):
        abort(404)

    # Remove Proxies
    remote_addr = getattr(request, 'remote_addr', None)
    route = list(getattr(request, 'access_route', remote_addr))
    route.reverse()
    ip_addr = route[app.config.get('PROXY_COUNT', 0)]

    geo_data = geo.query(ip_addr)

    data = dict(ip=ip_addr,
                cid=request.args.get('cid'),
                datetime=datetime.utcnow(),
                doc_title=request.args.get('dt'),
                doc_uri=request.args.get('dl'),
                doc_enc=request.args.get('de'),
                referrer=request.args.get('dr'),
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

    db.session.add(Crumb(data))
    db.session.commit()

    return Response(one_pxl, mimetype='image/gif')

@app.route('/cmb.js')
def deliver_js():
    """Serve cmb.js script."""
    return Response(cmbjs, mimetype='text/javascript')

@app.route('/')
def index():
    """Serve index page."""
    return 'crumby'

@app.errorhandler(404)
def not_found(error):
    """Serve unknown route page."""
    return 'This page does not exist', 404
