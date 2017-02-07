# Crumby

Crumby is a web analytics service. It performs data collection and reporting
on the interactions between a user and a website. Crumby offers two mechanisms
for tracking interactions: visits and events.

A visit is recorded when a user visits a page on the website and includes the
following data:

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

An event is recorded during a specific HTML event (e.g. button click) and
includes the following data:

  * General
    * Visitor ID (cookie)
    * IP address
    * Date and time
  * Page
    * Title
    * URI
  * Event
    * Name
    * Value

A public facing API is automatically configured at <domain>/data. An endpoint
is created for each query that exists in `crumby/templates/api/`. See the
[Setup](#add-queries-to-the-public-api) section for help on creating queries.

## Setup

### Install SQL Database

Crumby stores interaction data in an SQL database. Install a database supported
by [SQL Alchemy](http://docs.sqlalchemy.org/en/latest/dialects/index.html) and
specify the database URI in `config.py`.

### Download GeoIP2 Database

Crumby geolocates visits with the MaxMind geoip2 library and the
[GeoLite2 City](https://dev.maxmind.com/geoip/geoip2/geolite2/) database.
Download the latest binary file and specify the path to `GeoLite2-City.mmdb` in
`config.py`.

### Update Configuration File

The following values must be set in a
[config.py](http://flask.pocoo.org/docs/0.12/config/) file located in the base
directory.

|Value|Purpose|
|---|---|
|DOMAIN|The fully-qualified domain namespace of the application|
|SQLALCHEMY_DATABASE_URI|The SQL database URI|
|GEOIP2_DB_PATH|GeoIP2 database (GeoLite2-City.mmdb) filepath|
|PROXY_COUNT|Number of proxy servers in front of the app|
|CROSSDOMAIN_ORIGIN|Domain(s) permitted to query the crumby service|

Store a secondary `config.py` in an
[instance folder](http://flask.pocoo.org/docs/0.10/config/#instance-folders)
to overwrite values declared in the base `config.py`. This is useful for local
testing, for example:

    DOMAIN = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>@localhost/crumby'
    GEOIP2_DB_PATH = '/Path/to/GeoLite2-City.mmdb'
    SQLALCHEMY_ECHO = True
    DEBUG = True
    CROSSDOMAIN_ORIGIN = '\*'

### Run crumby

    python run.py

### Add Tracking Code

Add the following snippet to the webpage html, replacing <domain> with the
fully qualified domain of the crumby application:

    <script src="<domain>/cmb.js" type="text/javascript"></script>

To track events, make a call to `cmb.event(name, value)` in the webpage JS. For
example:

    document.getElementById('button').addEventListener('click', function() {
      cmb.event('vote', 'thumbs-up');
    });

### Add Queries to the Public API

Crumby creates two tables to store interaction data: visits and events. The
following columns are included in each table:

#### Visits

  * id
  * ip
  * cid
  * datetime
  * doc_title
  * doc_uri
  * doc_enc
  * referrer
  * \_referrer
  * platform
  * browser
  * version
  * screen_res
  * screen_depth
  * continent
  * country
  * subdivision_1
  * subdivision_2
  * city
  * latitude
  * longitude
  * accuracy_radius
  * time_zone
  * lang
  * \_lang

#### Events

  * id
  * ip
  * cid
  * datetime
  * doc_title
  * doc_uri
  * name
  * value

Queries can be added to `crumby/templates/api/` to query these tables. One file
should exist per query and must have the extension `.sql`. The name of the file
is the name of the query. Queries will be accessible through the public
endpoint: `<domain>/data/<query_name>`.

Queries are processed by Flask using the Jinja2 syntax. Currently, the following
variables are provided to the context when the query is processed:

  * t0: Start Time, default today - 30 days
  * t1: End Time, default: today

These variables originate from the query string (i.e. days, from, to). Browse to
`<domain>/data` for instructions on querying the public API including syntax,
query names, and available query strings.

For example, the following query would display the number of users and views
for each day during the last 30 days.

    SELECT date(datetime), count(distinct cid) as users, count(id) as views
    FROM visits
    GROUP BY datetime
    WHERE datetime between date("{{t0}}") and date("{{t1}}")

## Deploy to a Platform as a Service

Reference the appropriate branch of crumby:

* [Openshift](https://github.com/bmweiner/crumby/tree/openshift)
* Heroku (pending)
