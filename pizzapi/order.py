import requests

from .menu import Menu
from .urls import Urls, COUNTRY_USA 


# TODO: Add add_coupon and remove_coupon methods
class Order(object):
    """Core interface to the payments API.

    The Order is perhaps the second most complicated class - it wraps
    up all the logic for actually placing the order, after we've
    determined what we want from the Menu. 
    """
    def __init__(self, store, customer, address, country=COUNTRY_USA):
        self.store = store
        self.menu = Menu.from_store(store_id=store.id, country=country)
        self.customer = customer
        self.address = address
        self.urls = Urls(country)
        self.data = {
            'Address': {'Street': self.address.street,
                        'City': self.address.city,
                        'Region': self.address.region,
                        'PostalCode': self.address.zip,
                        'Type': 'House'},
            'Coupons': [], 'CustomerID': '', 'Extension': '',
            'OrderChannel': 'OLO', 'OrderID': '', 'NoCombine': True,
            'OrderMethod': 'Web', 'OrderTaker': None, 'Payments': [],
            'Products': [], 'Market': '', 'Currency': '',
            'ServiceMethod': 'Delivery', 'Tags': {}, 'Version': '1.0',
            'SourceOrganizationURI': 'order.dominos.com', 'LanguageCode': 'en',
            'Partners': {}, 'NewUser': True, 'metaData': {}, 'Amounts': {},
            'BusinessDate': '', 'EstimatedWaitMinutes': '',
            'PriceOrderTime': '', 'AmountsBreakdown': {}
            }

    # TODO: Implement item options
    # TODO: Add exception handling for KeyErrors
    def add_item(self, code, qty=1, options=[]):
        item = self.menu.variants[code]
        item.update(ID=1, isNew=True, Qty=qty, AutoRemove=False)
        self.data['Products'].append(item)
        return item

    # TODO: Raise Exception when index isn't found
    def remove_item(self, code):
        codes = [x['Code'] for x in self.data['Products']]
        return self.data['Products'].pop(codes.index(code))

    def add_coupon(self, code, qty=1):
        item = self.menu.variants[code]
        item.update(ID=1, isNew=True, Qty=qty, AutoRemove=False)
        self.data['Coupons'].append(item)
        return item

    def remove_coupon(self, code):
        codes = [x['Code'] for x in self.data['Coupons']]
        return self.data['Coupons'].pop(codes.index(code))

    def _send(self, url, merge):
        self.data.update(
            StoreID=self.store.id,
            Email=self.customer.email,
            FirstName=self.customer.first_name,
            LastName=self.customer.last_name,
            Phone=self.customer.phone,
            #Address=self.address.street

        )

        for key in ('Products', 'StoreID', 'Address'):
            if key not in self.data or not self.data[key]:
                raise Exception('order has invalid value for key "%s"' % key)

        headers = {
            'Referer': 'https://order.dominos.com/en/pages/order/',
            'Content-Type': 'application/json'
        }

        r = requests.post(url=url, headers=headers, json={'Order': self.data})
        r.raise_for_status()
        json_data = r.json()

        if merge:
            for key, value in json_data['Order'].items():
                if value or not isinstance(value, list):
                    self.data[key] = value
        return json_data

    # TODO: Figure out if this validates anything that self.urls.price_url() does not
    def validate(self):
        response = self._send(self.urls.validate_url(), True)
        return response['Status'] != -1

    # TODO: Actually test this
    def place(self, card=False):
        self.pay_with(card)
        response = self._send(self.urls.place_url(), False)
        return response

    # TODO: Add self.price() and update whenever called and items were changed
    def pay_with(self, card=False):
        """Use this instead of self.place when testing"""
        # get the price to check that everything worked okay
        response = self._send(self.urls.price_url(), True)
        
        if response['Status'] == -1:
            raise Exception('get price failed: %r' % response)

        if card == False:
            self.data['Payments'] = [
                {
                    'Type': 'Cash',
                }
            ]
        else:
            self.data['Payments'] = [
                {
                    'Type': 'CreditCard',
                    'Expiration': card.expiration,
                    'Amount': self.data['Amounts'].get('Customer', 0),
                    'CardType': card.card_type,
                    'Number': int(card.number),
                    'SecurityCode': int(card.cvv),
                    'PostalCode': int(card.zip)
                }
            ]

        return response
