"""Geolocation of IP."""
import os
import warnings
import geoip2.database

class Geo(object):
    """Geolocate IP."""
    def __init__(self, filepath):
        """Init a Geo class.

        Args:
            filepath: The path to the GeoIP2 database, GeoLite2-City.mmdb.
        """
        self.conn = None
        if os.path.exists(filepath):
            try:
                self.conn = geoip2.database.Reader(filepath)
            except ValueError or IOError:
                warnings.warn('Unable to init GeoIP2 database: %s' % filepath)

    def query(self, ip):
        """Query DB for IP."""
        if not ip or not self.conn:
            warnings.warn('Unable to geolocate: %s' % ip)
            return {}

        data = {}
        try:
            resp = self.conn.city(ip)
        except geoip2.errors.AddressNotFoundError:
            warnings.warn('Unable to geolocate: %s' % ip)
            return {}

        if getattr(resp, 'continent', None):
            data['continent'] = getattr(resp.continent, 'code', None)
        if getattr(resp, 'country', None):
            data['country'] = getattr(resp.country, 'iso_code', None)
        if getattr(resp, 'subdivisions', None):
            data['subdivision_1'] = getattr(resp.subdivisions[0], 'name', None)
            try:
                data['subdivision_2'] = getattr(resp.subdivisions[1], 'name',
                                                None)
            except IndexError:
                pass
        if getattr(resp, 'city', None):
            data['city'] = getattr(resp.city, 'name', None)
        if getattr(resp, 'location', None):
            data['latitude'] = getattr(resp.location, 'latitude', None)
            data['longitude'] = getattr(resp.location, 'longitude', None)
            data['accuracy_radius'] = getattr(resp.location, 'accuracy_radius',
                                              None)
            data['time_zone'] = getattr(resp.location, 'time_zone', None)

        return data
