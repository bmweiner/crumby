"""Routes for reporting."""

import os
import datetime
from flask import request
from flask import jsonify
from flask import render_template
from .. import app
from .. import db
from ..utils.extensions import crossdomain

def query(db, sql):
    """Query Flask-SQLAlchemy DB.

    Args:
        db: flask_sqlalchemy.SQLAlchemy.
        sql: str. Query

    Returns:
        dict: results of query
    """
    result = db.engine.execute(sql)
    return [dict(zip(result.keys(), rows)) for rows in result.fetchall()]

@app.route('/data/')
@app.route('/data/<name>')
@crossdomain(origin=app.config.get('CROSSDOMAIN_ORIGIN', '*'))
def data(name=None):
    """Return dataset."""
    ndays = 30
    templates = os.listdir(os.path.join(app.root_path, 'templates'))
    queries = [t[:-4] for t in templates if t.endswith('.sql')]
    if not name:  # return list of queries
        query_strings = ['days', 'from', 'to']
        info = [
            "syntax: /data/query_name?query_string",
            "default date range is last {} days".format(ndays),
            "specify a custom date range with 'days' or 'from' & 'to'",
            "'days' accepts unsigned int",
            "'from'/'to' accepts str of format YYYY-MM-DD",
            "examples:",
            "/data/visits?days=120",
            "/data/platforms?from=2016-09-01&to=2017-02-20"
            ]
        return jsonify(queries=queries, query_strings=query_strings, info=info)
    if name not in queries:  # query name does not exist
        return jsonify(error="query '{}' does not exist.".format(name))

    context = {
        'days':request.args.get('days', type=int),
        't0':request.args.get('from'),
        't1':request.args.get('to'),
    }
    # validate and set time args
    if all([context['t0'], context['t1'], context['days']]):  # bad args
        return jsonify(error="Provided both from/to and days.")
    elif context['t0'] and not context['t1']:  # bad args
        return jsonify(error="Missing to date.")
    elif context['t1'] and not context['t0']:  # bad args
        return jsonify(error="Missing from date.")
    elif all([context['t0'], context['t1']]):
        strptime = datetime.datetime.strptime
        try:
            context['t0'] = strptime(context['t0'], '%Y-%m-%d')
            context['t1'] = strptime(context['t1'], '%Y-%m-%d')
        except ValueError as err:
            return jsonify(error=err)
    else:
        today = datetime.datetime.utcnow().date()
        if context['days']:
            days = context['days']
        else:
            days = ndays
        try:
            context['t0'] = today - datetime.timedelta(days)
        except ValueError as err:
            return jsonify(error=err)
        context['t1'] = today

    # convert time args
    if context['t0'] > context['t1']:
        return jsonify(error="Time error: from > to.")
    else:
        context['t0'] = context['t0'].strftime('%Y-%m-%d')
        context['t1'] = context['t1'].strftime('%Y-%m-%d')

    sql = render_template(name + '.sql', **context)
    return 	jsonify(name=name, data=query(db, sql))
