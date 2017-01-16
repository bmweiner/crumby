"""General routes."""

from .. import app

@app.route('/')
def index():
    """Serve index page."""
    return 'crumby'

@app.errorhandler(404)
def not_found(error):
    """Serve unknown route page."""
    return 'This page does not exist', 404
