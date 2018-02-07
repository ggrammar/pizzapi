from .store import Store
from .utils import request_json
from .urls import Urls, COUNTRY_USA

class Address(object):
    """Create an address, for finding stores and placing orders.

    The Address object describes a street address in North America (USA or
    Canada, for now). Callers can use the Address object's methods to find
    the closest or nearby stores from the API. 

    Attributes:
        street (String): Street address
        city (String): North American city
        region (String): North American region (state, province, territory)
        zip (String): North American ZIP code
        urls (String): Country-specific URLs
        country (String): Country
    """

    def __init__(self, street, city, region='', zip='', country=COUNTRY_USA, *args):
        self.street = street.strip()
        self.city = city.strip()
        self.region = region.strip()
        self.zip = str(zip).strip()
        self.urls = Urls(country)
        self.country = country

    @property
    def data(self):
        return {'Street': self.street, 'City': self.city,
                'Region': self.region, 'PostalCode': self.zip}

    @property
    def line1(self):
        return '{Street}'.format(**self.data)

    @property
    def line2(self):
        return '{City}, {Region}, {PostalCode}'.format(**self.data)

    def nearby_stores(self, service='Delivery'):
        """Query the API to find nearby stores.

        nearby_stores will filter the information we receive from the API
        to exclude stores that are not currently online (!['IsOnlineNow']),
        and stores that are not currently in service (!['ServiceIsOpen']).

        (city and region) or (postalcode) is required to get a result from
        the API. This is enforced in the tests, but not in these methods,
        since the API might change in the future. 
        """
        data = request_json(
            self.urls.find_url(), 
            line1=self.line1, 
            line2=self.line2, 
            type=service
        )

        if data['Status'] == -1:
            # This is an error from the Domino's API. 
            raise Exception(data['StatusItems'])

        return [Store(x, self.country) for x in data['Stores']
                if x['IsOnlineNow'] and x['ServiceIsOpen'][service]]

    def closest_store(self, service='Delivery'):
        stores = self.nearby_stores(service=service)
        if not stores:
            raise Exception('No local stores are currently open')
        return stores[0]
