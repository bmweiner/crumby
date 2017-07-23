#!/usr/bin/python
"""WSGI entry point."""

import os

activate_this = os.path.expanduser('~/.virtualenvs/crumby/bin/activate_this.py')

try:
    execfile(activate_this, dict(__file__=activate_this))
except IOError:
    pass

from crumby import app as application

if __name__ == '__main__':
    application.run()
