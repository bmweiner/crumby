#!/usr/bin/python
"""Generic WSGI entry point."""

from crumby import app as application

if __name__ == '__main__':
    application.run()
