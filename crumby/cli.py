"""crumby shell interface."""

import sys
import os
import logging
import warnings
import argparse
import subprocess
from datetime import datetime
import pkg_resources

import crumby
from crumby import services


def init(**kwargs):
    filename = pkg_resources.resource_filename('crumby', 'data/example.cfg')
    with open(filename) as f:
        txt = f.read()

    filename = os.path.join(os.getcwd(), 'crumby.cfg')
    with open(filename, 'wb') as f:
        f.write(txt)

    print('Template config file created: {}'.format(filename))
    print('1. Edit this config file with your preferences')
    print('2. Move the config file to your preferred location')
    print('3. Set an environment variable named: CRUMBY_SETTINGS to the path')
    print('   For example: export CRUMBY_SETTINGS={}'.format(filename))
    print('4. Restart crumby')

def geoip(**kwargs):
    if kwargs['upgrade']:
        path = crumby.app.config.get('GEOIP2_DATABASE_NAME')
    else:
        path = os.path.join(os.getcwd(), 'GeoLite2-City.mmdb')

    services.update_geoip(path)
    print('Saved to: {}'.format(path))

def env(**kwargs):
    for item in sorted(services.view_env().items()):
        print(item)

def users(**kwargs):
    print(os.getcwd())
    print(services.view_users())

def adduser(username, password, **kwargs):
    services.add_user(username, password)

def deluser(username, **kwargs):
    services.delete_user(username)

def run(**kwargs):
    crumby.app.config['DEBUG'] = True
    crumby.app.config['SQLALCHEMY_ECHO'] = True
    os.environ['FLASK_APP'] = 'crumby'
    os.environ['FLASK_DEBUG'] = '1'
    subprocess.call(["flask", "run"])

if __name__ == '__main__':
    args = dict(
        prog='crumby',
        description='A command line interface for the crumby web analytics app.',
        epilog='https://github.com/bmweiner/crumby'
       )
    parser = argparse.ArgumentParser(**args)
    subparsers = parser.add_subparsers(dest='command')

    commands = [
        dict(
            name='init',
            func=init,
            help='create template config file',
            args={}
        ),
        dict(
            name='geoip',
            func=geoip,
            help='download latest geoip database',
            args={
                '-upgrade':dict(help='upgrade existing geoip database',
                                action='store_true')
            }
        ),
        dict(
            name='env',
            func=env,
            help='display Flask configuration values',
            args={}
        ),
        dict(
            name='users',
            func=users,
            help='view list of users',
            args={}
            ),
        dict(
            name='adduser',
            func=adduser,
            help='add user - grant private query access',
            args={
                'username':dict(help='a valid username'),
                'password':dict(help='a valid password')
            }
        ),
        dict(
            name='deluser',
            func=deluser,
            help='delete user - revoke private query access',
            args={
                'username':dict(help='a valid username')
            }
        ),
        dict(
            name='run',
            func=run,
            help='launch crumby in development server',
            args={}
        )
    ]
    commands.sort(key=lambda x: x['name'])

    for cmd in commands:
        subparser = subparsers.add_parser(cmd['name'], help=cmd['help'])
        subparser.set_defaults(func=cmd['func'])
        for name, kwargs in cmd['args'].items():
            subparser.add_argument(name, **kwargs)

    ns = parser.parse_args()
    kwargs = vars(ns)

    ns.func(**kwargs)
