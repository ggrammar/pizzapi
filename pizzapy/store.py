from .menu import Menu
from .urls import Urls, COUNTRY_USA
from .utils import request_json



class Store(object):
    """The interface to the Store API

    You can use this to find store information about stores near an
    address, or to find the closest store to an address. 
    """
    def __init__(self, data={}, country=COUNTRY_USA):
        self.id = str(data.get('StoreID', -1))
        self.country = country
        self.urls = Urls(country)
        self.data = data

    def __repr__(self):
        return "Store #{}\nAddress: {}\n\nOpen Now: {}".format(
            self.id,
            self.data['AddressDescription'],
            'Yes' if self.data.get('IsOpen', False) else 'No',
        )

    def get_details(self):
        details = request_json(self.urls.info_url(), store_id=self.id)
        return details
    
    def place_order(self, order, card):
        print('Order placed for {}'.format(order.customer.first_name))
        return order.place(card=card)

    def get_menu(self, lang='en'):
        response = request_json(self.urls.menu_url(), store_id=self.id, lang=lang)
        menu = Menu(response, self.country)
        return menu


class StoreLocator(object):
    @classmethod
    def __repr__(self):
        return 'I locate stores and nothing else'

    @staticmethod
    def nearby_stores(address, service='Delivery'):
        """Query the API to find nearby stores.

        nearby_stores will filter the information we receive from the API
        to exclude stores that are not currently online (!['IsOnlineNow']),
        and stores that are not currently in service (!['ServiceIsOpen']).
        """
        data = request_json(address.urls.find_url(), line1=address.line1, line2=address.line2, type=service)
        return [Store(x, address.country) for x in data['Stores']
                if x['IsOnlineNow'] and x['ServiceIsOpen'][service]]

    @staticmethod
    def find_closest_store_to_customer(customer, service='Delivery'):
        stores = StoreLocator.nearby_stores(customer.address, service=service)
        if not stores:
            raise Exception('No local stores are currently open')
        return stores[0]

