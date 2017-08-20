# This script will install and configure crumby on: AWS with Amazon Linux
# AMI 2017.03.1 (HVM), SSD Volume Type. Set the domain and crossdomain_origin
# below before running.

domain='site.com'  # Domain name of the server where crumby is installed
crossdomain_origin='*'  # URL(s) permitted to access the crumby API.

# install packages
yum update -y
yum install -y gcc libffi-devel python-devel
yum install -y httpd24 mod24_ssl mysql56-server mod24_wsgi-python27.x86_64

# install crumby in a virtualenv
mkdir /var/lib/crumby
virtualenv /var/lib/crumby/virtenv
source /var/lib/crumby/virtenv/bin/activate
pip install crumby pymysql

# configure crumby
cd /var/lib/crumby
crumby geoip
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 24 > /var/lib/crumby/MYSQL_PASS
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 24 > /var/lib/crumby/SECRET_KEY
cat <<EOF > /var/lib/crumby/crumby.cfg
import os

base_path = '/var/lib/crumby'
with open(os.path.join(base_path, 'MYSQL_PASS')) as f:
    pw = f.read().strip('\n')
    db = 'mysql+pymysql://root:{}@localhost/crumby'.format(pw)

DOMAIN = '$domain'

SQLALCHEMY_DATABASE_URI = db

GEOIP2_DATABASE_NAME = '/var/lib/crumby/GeoLite2-City.mmdb'

with open(os.path.join(base_path, 'SECRET_KEY')) as f:
    SECRET_KEY = f.read().strip('\n')

SESSION_COOKIE_SECURE = True
CROSSDOMAIN_ORIGIN = '$crossdomain_origin'
EOF

# set crumby as owner
useradd -r crumby
chown -R crumby:crumby /var/lib/crumby

# configure mysql
service mysqld start
mysql_secure_installation <<EOF

y
$(cat /var/lib/crumby/MYSQL_PASS)
$(cat /var/lib/crumby/MYSQL_PASS)
y
y
y
y
EOF
mysql -uroot -p$(cat /var/lib/crumby/MYSQL_PASS) --execute="CREATE DATABASE crumby;"

# configure httpd
cat <<EOF >> /etc/httpd/conf/httpd.conf

<VirtualHost *:80>
  ServerName $domain
  ServerAdmin admin@$domain

  WSGIProcessGroup crumby
  WSGIDaemonProcess crumby python-home=/var/lib/crumby/virtenv
  WSGIScriptAlias / /var/www/wsgi-scripts/crumby.wsgi

  <Directory /var/www/wsgi-scripts>
    <Files crumby.wsgi>
      Require all granted
    </Files>
  </Directory>

</VirtualHost>

<VirtualHost *:443>
  ServerName $domain
  ServerAdmin admin@$domain

  WSGIProcessGroup crumby
  WSGIScriptAlias / /var/www/wsgi-scripts/crumby.wsgi

  <Directory /var/www/wsgi-scripts>
    <Files crumby.wsgi>
      Require all granted
    </Files>
  </Directory>

</VirtualHost>
EOF

# create WSGI entrypoint
mkdir /var/www/wsgi-scripts
cat <<EOF > /var/www/wsgi-scripts/crumby.wsgi
#!/usr/bin/env python
"""WSGI entry point."""

import os

os.environ['CRUMBY_SETTINGS'] = '/var/lib/crumby/crumby.cfg'

from crumby import app as application
EOF

# start services and enable on restart
service mysqld restart
service httpd restart
chkconfig httpd on
chkconfig mysqld on

# remove build dependencies
yum erase -y gcc libffi-devel python-devel
yum autoremove -y
