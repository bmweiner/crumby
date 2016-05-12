# crumby

crumby is a Flask app for tracking website traffic. crumby is configured for
deployment to OpenShift using the python-2.7 and mysql-5.5 cartridges.

## Setup

 1. Create and start the crumby app

        rhc app create -s crumby python-2.7 mysql-5.5 --from-code https://github.com/bmweiner/crumby.git

 2. Add the js code snippet to the `<head>` section of your site template.

        <script src="<app_url>/cmb.js" type="text/javascript"></script>

    **Note**: Replace `<app_url>` with the crumby app url.

### Geolocation Data

Geolocation data is obtained from the binary MaxMind DB:
[GeoLite2 City](https://dev.maxmind.com/geoip/geoip2/geolite2/).

A [pre_build](.openshift/action_hooks/pre_build) script will download the latest
database to the `$OPENSHIFT_DATA_DIR`. Upon subsequent builds, the existing
database will be updated if its last modification time is greater than 30 days.
To manually update the database, delete the existing database and rebuild.

## Browse Traffic

    $ rhc ssh crumby
    > mysql -u$OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -h$OPENSHIFT_MYSQL_DB_HOST

    mysql> use crumby;
    mysql> select * from crumbs;

or locally...

    $ rhc port-forward
    $ mysql -u <username> -p -h <host> -P <port>

## Testing

Create an [instance folder](http://flask.pocoo.org/docs/0.10/config/#instance-folders)
for local testing:

    mkdir instance && touch instance/config.py

Store local settings in config.py, for example:

    DOMAIN = 'localhost:5000'
    PKG = 'crumby/'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    GEO_DB_URI = 'GeoLite2-City.mmdb'
    SQLALCHEMY_ECHO = True
    DEBUG = True

Start crumby

    python wsgi.py

Send crumby some test data

    curl localhost:5000/0.gif?cid=123
