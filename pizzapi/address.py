from store import Store
from utils import request_json
from urls import FIND_URL

class Address(object):
    def __init__(self, street, city, region='', zip=''):
        self.street = street.strip()
        self.city = city.strip()
        self.region = region.strip()
        self.zip = str(zip).strip()

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
        data = request_json(FIND_URL, line1=self.line1, line2=self.line2, type=service)
        return [Store(x) for x in data['Stores']
                if x['IsOnlineNow'] and x['ServiceIsOpen'][service]]

    def closest_store(self, service='Delivery'):
        stores = self.nearby_stores(service=service)
        if not stores:
            raise Exception('No local stores are currently open')
        return stores[0]
