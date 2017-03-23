#!/usr/bin/env python

import sys
from crumby import db
from crumby.models import User

try:
    sys.argv[1]
    sys.argv[2]
    db.session.add(User(username=sys.argv[1], password=sys.argv[2]))
    db.session.commit()
except IndexError as err:
    print('Bad args, try: "python add_user.py <username> <password>"')
