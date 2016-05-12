"""Geolocation of IP."""
import warnings
import geoip2.database

class Geo(object):
    """Geolocate IP."""
    def __init__(self, name, uri):
        """Init a Geo class.

        Args:
            db: str. Database URI.
            name: str. Database name, valid options: ['geolite2_city'].
        """
        self.name = name
        if self.name == 'geolite2_city':
            self.conn = self.geolite2_conn(uri)
        else:
            warnings.warn('Unsupported geolocation DB: %s' % self.name)
            self.conn = None

    def query(self, ip):
        """Query DB for IP."""
        if ip and self.conn:
            if self.name == 'geolite2_city':
                return self.geolite2_city(ip)
            else:
                warnings.warn('Unsupported geolocation DB: %s' % self.name)
                return {}
        else:
            warnings.warn('Unable to geolocate: %s' % ip)
            return {}

    def geolite2_conn(self, uri):
        """Setup connection to GeoLite2 City DB."""
        try:
            return geoip2.database.Reader(uri)
        except ValueError:
            warnings.warn('Unable to connect geolocation DB: %s' % uri)
            return None

    def geolite2_city(self, ip):
        """Query GeoLite2 City DB for IP."""
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
