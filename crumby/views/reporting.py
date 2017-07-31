"""Routes for reporting."""

import datetime
import os
from flask import request
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash
from flask import abort
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from jinja2.exceptions import TemplateNotFound
from .. import app
from .. import db
from .. import login_manager
from ..models import User
from ..extensions.security import is_safe_url
from ..extensions.security import crossdomain
from ..extensions.database import query
from ..extensions.database import parse_qstring
from ..extensions.database import query_names

login_manager.login_view = 'login'
login_manager.login_message = 'Login required.'
login_manager.login_message_category = "info"

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            url = request.args.get('next')
            if not is_safe_url(url):
                return abort(400)
            flash(u'Welcome {}'.format(username), 'success')
            print('Login Passed:', username)
            return redirect(url or url_for('index'))
        else:
            print('Login Failed:', username)
            flash(u'Invalid login, please try again', 'warning')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    """Serve index page."""
    context = dict(
        private=query_names(app, 'private'),
        public=query_names(app, 'public')
    )
    return render_template("index.html", **context)

@app.route('/api/')
def api():
    return render_template('api.html')

@app.route('/api/public')
@app.route('/api/public/<name>')
@crossdomain(origin=app.config.get('CROSSDOMAIN_ORIGIN', '*'))
def api_public(name=None):
    if not name:
        return api_collection('public')
    return api_query('public', name, request)

@app.route('/api/private')
@app.route('/api/private/<name>')
@crossdomain(origin=app.config.get('CROSSDOMAIN_ORIGIN', '*'))
@login_required
def api_private(name=None):
    if not name:
        return api_collection('private')
    return api_query('private', name, request)

def api_collection(collection):
    queries = query_names(app, collection)
    context = dict(
        current_user=current_user,
        collection=collection,
        queries=queries
        )
    return render_template('api.html', **context)

def api_query(collection, name, request):
    try:
        context = parse_qstring(request)
    except ValueError as err:
        return jsonify(error=err)

    file_path = os.path.join('api', collection, name + '.sql')
    try:
        sql = render_template(file_path, **context)
    except TemplateNotFound as err:
        return jsonify(error="query '{}' does not exist.".format(name))

    return 	jsonify(query(db, sql))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(u'You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    """Serve unknown route page."""
    return 'This page does not exist', 404
