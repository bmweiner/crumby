# Crumby

Crumby is an open source application for tracking and reporting visitor usage of
a website. Crumby is a Flask application so it works with well known tools such
as Apache, MySQL, and Python. Crumby includes a simple web-based frontend and a
JSON compliant RESTful API for reporting. Queries are assigned to a public or
private endpoint. Private queries are only accessible by authenticated users.

## Architecture

![architecture diagram][architecture]

### Crumby Database (crumby.db)

A SQL database is required to store tracking data. Any database compatible with
SQLAlchemy can be used. The following tables will be initialized when crumby
first runs:

 * calendar - A range of dates available for queries
 * events - Visitor interactions with the website
 * users - Users permitted to access private queries
 * visits - Visitors to the website

#### calendar

| Column    | Category | Description                  |
|-----------|----------|------------------------------|
| datetime  | General  | Date and time                |


#### events

| Column    | Category | Description                  |
|-----------|----------|------------------------------|
| id        | General  | Unique record ID             |
| ip        | General  | IP address                   |
| cid       | General  | Visitor ID (cookie)          |
| datetime  | General  | Date and time event occurred |
| doc_title | Page     | Page title                   |
| doc_uri   | Page     | Page URI                     |
| name      | Action   | Name of the event            |
| value     | Action   | Value of the event           |

#### users

| Column   | Category | Description      |
|----------|----------|------------------|
| id       | General  | Unique record ID |
| username | Login    | Username         |
| password | Login    | Hashed password  |

#### visits

| Column          | Category          | Description                  |
|-----------------|-------------------|------------------------------|
| id              | General           | Unique record ID             |
| ip              | General           | IP address                   |
| cid             | General           | Visitor ID (cookie)          |
| datetime        | General           | Date and time page accessed  |
| doc_title       | Page              | Page title                   |
| doc_uri         | Page              | Page URI                     |
| doc_enc         | Page              | Encoding of page             |
| referrer        | General           | Referrer from client browser |
| \_referrer      | General           | Referrer from request header |
| platform        | Hardware/Software | Browser platform             |
| browser         | Hardware/Software | Browser name                 |
| version         | Hardware/Software | Browser version              |
| screen_res      | Hardware/Software | Browser screen resolution    |
| screen_depth    | Hardware/Software | Browser screen depth         |
| continent       | Geospatial        | Continent                    |
| country         | Geospatial        | Country                      |
| subdivision_1   | Geospatial        | Subdivisions                 |
| subdivision_2   | Geospatial        | Subdivisions                 |
| city            | Geospatial        | City                         |
| latitude        | Geospatial        | Latitude                     |
| longitude       | Geospatial        | Longitude                    |
| accuracy_radius | Geospatial        | Geo accuracy                 |
| time_zone       | Geospatial        | Time zone                    |
| lang            | General           | Language from client browser |
| \_lang          | General           | Language from request header |

### Command Line Interface (crumby CLI)


A visit is recorded when a user visits a page on the website and includes the
following data:



An event is recorded during a specific HTML event (e.g. button click) and
includes the following data:



A public facing API is automatically configured at <domain>/api/public. An
endpoint is created for each query that exists in `crumby/templates/api/public`.
Authenticated users can access a private API at <domain>/api/private. An endpoint
is created for each query that exists in `crumby/templates/api/private`.
See the [Setup](#add-queries-to-the-api) section for help on creating
queries.

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
|GEOIP2_DATABASE_NAME|GeoIP2 database (GeoLite2-City.mmdb) filepath|
|PROXY_COUNT|Number of proxy servers in front of the app|
|CROSSDOMAIN_ORIGIN|Domain(s) permitted to query the crumby service|

Store a secondary `config.py` in an
[instance folder](http://flask.pocoo.org/docs/0.10/config/#instance-folders)
to overwrite values declared in the base `config.py`. This is useful for local
testing, for example:

    DOMAIN = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>@localhost/crumby'
    GEOIP2_DATABASE_NAME = '/Path/to/GeoLite2-City.mmdb'
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

### Add Queries to the API

Crumby creates two tables to store interaction data: visits and events. The
following columns are included in each table:

#### Visits



#### Events



Queries can be added to `crumby/templates/api/public` or
`crumby/templates/api/private` depending on the access requirements. One file
should exist per query and must have the extension `.sql`. The name of the file
is the name of the query. Query results will be accessible through the public
endpoint: `<domain>/api/public/<query_name>` or private endpoint:
`<domain>/api/private/<query_name>` which requires authentication.

Queries are processed by Flask using the Jinja2 syntax. Currently, the following
variables are provided to the context when the query is processed:

  * t0: Start Time, default today - 30 days
  * t1: End Time, default: today

These variables originate from the query string (i.e. days, from, to). Browse to
`<domain>/api` for instructions on querying the public API including syntax,
query names, and available query strings.

For example, the following query would display the number of users and views
for each day during the last 30 days.

    SELECT date(datetime), count(distinct cid) as users, count(id) as views
    FROM visits
    GROUP BY datetime
    WHERE datetime between date("{{t0}}") and date("{{t1}}")

### Add Users

A script is included in the crumby package which adds a username and password to
the database. These users will be permitted access to crumby endpoints requiring
authentication.

    python add_user.py <username> <password>

## Deploy to a Platform as a Service

Reference the appropriate branch of crumby:

* [Openshift](https://github.com/bmweiner/crumby/tree/openshift)
* Heroku (pending)

[architecture]: https://raw.githubusercontent.com/bmweiner/crumby/master/static/architecture.png
