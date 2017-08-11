#!/usr/bin/env python
"""WSGI entry point."""

import os

os.environ['CRUMBY_SETTINGS'] = '/var/lib/crumby/crumby.cfg'

from crumby import app as application
