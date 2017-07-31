"""Database utils."""

import os
import datetime

def query(db, sql):
    """Query Flask-SQLAlchemy DB.

    Args:
        db: flask_sqlalchemy.SQLAlchemy.
        sql: str. Query

    Returns:
        dict: results of query
    """
    result = db.engine.execute(sql)
    payload = {'data':[list(row) for row in result.fetchall()],
               'columns':result.keys()}
    return payload

def parse_qstring(request, ndays=30):
    """Parse query string.

    Args:
        request: dict. Flask request context.

    Returns:
        (bool, obj): Tuple where first item is True if success, False otherwise
            and second item is a dict of the parsed context or a str error
            message.
    """
    args = {
        'days':request.args.get('days', type=int),
        't0':request.args.get('t0'),
        't1':request.args.get('t1'),
    }

    today = datetime.datetime.utcnow()
    strptime = datetime.datetime.strptime

    context = {}
    if args['t0'] or args['t1']:
        if not all((args['t0'], args['t1'])):
            raise ValueError('Both from and to required')

    if args['t0']:
        context['t0'] = strptime(args['t0'], '%Y-%m-%d')
    else:
        context['t0'] = today - datetime.timedelta(ndays)

    if args['t1']:
        context['t1'] = strptime(args['t1'], '%Y-%m-%d')
    else:
        context['t1'] = today

    if args['days'] is not None:
        context['t0'] = context['t1'] - datetime.timedelta(args['days'])

    if context['t0'] > context['t1']:
        raise ValueError("From > To")

    context['t0'] = context['t0'].strftime('%Y-%m-%d')
    context['t1'] = context['t1'].strftime('%Y-%m-%d')

    return context

def query_names(app, collection):
    file_path = os.path.join(app.root_path, 'templates', 'api', collection)
    return [t[:-4] for t in os.listdir(file_path) if t.endswith('.sql')]
