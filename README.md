# crumby

crumby is a self-hosted app for tracking and reporting your websites traffic.

## Tracking

### Visits

The following visitor data is captured:

  * General
    * Visitor ID (cookie)
    * IP address
    * Referrer
    * Date and time
    * Language
  * Page
    * Title
    * URI
    * Encoding
  * Hardware/Software
    * Platform
    * Browser
    * Browser version
    * Screen resolution
    * Screen depth
  * Geospatial
    * Continent
    * Country
    * Subdivisions
    * City
    * Latitude
    * Longitude
    * Geo accuracy
    * Time zone

### Events

Custom user events (e.g. clicks) can also be captured through cmb.event.

## Setup

### Deploy Crumby

#### OpenShift

    rhc app create -s crumby python-2.7 mysql-5.5 --from-code https://github.com/bmweiner/crumby.git

Geolocation data is obtained from the binary MaxMind DB:
[GeoLite2 City](https://dev.maxmind.com/geoip/geoip2/geolite2/).

A [pre_build](.openshift/action_hooks/pre_build) script will download the latest
database to the `$OPENSHIFT_DATA_DIR`. Upon subsequent builds, the existing
database will be updated every 30 days. To manually update the database, delete
the existing database and rebuild.

#### Other

Update config.py for your server environment and follow your hosts instructions
for deployment.

### Configure Website

#### Tracking Visitors

Add the following code to your page, replacing <app_url> with the crumby app
url:

    <script src="<app_url>/cmb.js" type="text/javascript"></script>

#### Tracking Events

To track events call `cmb.event` passing a name and value to track. For example:

    document.getElementById('button').addEventListener('click', function() {
      cmb.event('vote', 'thumbs-up');
    });

## Querying

### API

Add queries to `crumby/templates`

List all queries: `<app_url>/data`

Return visit data: `<app_url>/data/visits`

## Connecting to OpenShift Database

    $ rhc ssh crumby
    > mysql -u$OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -h$OPENSHIFT_MYSQL_DB_HOST

    mysql> use crumby;
    mysql> select * from visits;

or locally...

    $ rhc port-forward
    $ mysql -u <username> -p -h <host> -P <port>

## Testing

1. Create an [instance folder](http://flask.pocoo.org/docs/0.10/config/#instance-folders)
for local testing:

    mkdir instance && touch instance/config.py

2. Store local settings in config.py, for example:

    DOMAIN = 'localhost:5000'
    PKG = 'crumby/'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/crumby'
    GEO_DB_URI = 'GeoLite2-City.mmdb'
    SQLALCHEMY_ECHO = True
    DEBUG = True
    CROSSDOMAIN_ORIGIN = '\*'

3. start crumby `python wsgi.py`

4. Send crumby some test data

    curl localhost:5000/0.gif?t=visit&cid=123&doc_title=test
