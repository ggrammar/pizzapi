import requests

VALIDATE_URL = 'https://order.dominos.com/power/validate-order'
PRICE_URL = 'https://order.dominos.com/power/price-order'
PLACE_URL = 'https://order.dominos.com/power/place-order'


# TODO: Add add_coupon and remove_coupon methods
class Order(object):
    def __init__(self, store, customer):
        self.store = store
        self.customer = customer
        self.data = {'Coupons': [], 'CustomerID': '', 'Extension': '',
                     'OrderChannel': 'OLO', 'OrderID': '', 'NoCombine': True,
                     'OrderMethod': 'Web', 'OrderTaker': None, 'Payments': [],
                     'Products': [], 'Market': '', 'Currency': '',
                     'ServiceMethod': 'Delivery', 'Tags': {}, 'Version': '1.0',
                     'SourceOrganizationURI': 'order.dominos.com',
                     'LanguageCode': 'en', 'Partners': {}, 'NewUser': True,
                     'metaData': {}, 'Amounts': {}, 'BusinessDate': '',
                     'EstimatedWaitMinutes': '', 'PriceOrderTime': '',
                     'AmountsBreakdown': {}}

    # TODO: Find a more elegant way to copy a previous order
    def copy(self, prev_order):
        if self.customer.first_name:
            prev_order.data['FirstName'] = self.customer.first_name
        if self.customer.last_name:
            prev_order.data['LastName'] = self.customer.last_name
        if self.customer.email:
            prev_order.data['Email'] = self.customer.email
        if self.customer.phone:
            prev_order.data['Phone'] = self.customer.phone
        if self.customer.address:
            prev_order.data['Address'] = self.customer.address
        keys = ['Address', 'Email', 'Phone', 'FirstName', 'LastName',
                'OrderID', 'Products', 'Market', 'Currency', 'StoreID',
                'Amounts', 'BusinessDate', 'EstimatedWaitMinutes',
                'PriceOrderTime', 'AmountsBreakdown']
        self.data.update({k: v for k, v in prev_order.data.iteritems()
                          if k in keys})

    # TODO: Implement item options
    # TODO: Add exception handling for KeyErrors
    def add_item(self, code, qty=1, options=[]):
        item = self.store.get_menu().variants[code]
        item.update({'ID': 1, 'isNew': True, 'Qty': qty, 'AutoRemove': False})
        self.data['Products'].append(item)
        return item

    # TODO: Raise Exception when index isn't found
    def remove_item(self, code):
        codes = [x['Code'] for x in self.data['Products']]
        return self.data['Products'].pop(codes.index(code))

    def _send(self, url, merge):
        self.data['Address'] = self.customer.address.data
        self.data['Email'] = self.customer.email
        self.data['FirstName'] = self.customer.first_name
        self.data['LastName'] = self.customer.last_name
        self.data['Phone'] = self.customer.phone
        self.data['StoreID'] = self.store.id
        assert self.data['Products']
        assert self.data['StoreID']
        assert self.data['Address']
        headers = {'Referer': 'https://order.dominos.com/en/pages/order/',
                   'Content-Type': 'application/json'}
        r = requests.post(url, headers=headers, json={'Order': self.data})
        r.raise_for_status()
        response = r.json()
        if merge:
            self._merge_response(response)
        return response

    def _merge_response(self, response):
        for key, value in response['Order'].iteritems():
            if not (isinstance(value, list) and len(value) <= 0):
                self.data[key] = value

    # TODO: Figure out if this validates anything that PRICE_URL does not
    def validate(self):
        response = self._send(VALIDATE_URL, True)
        return response['Status'] != -1

    # TODO: Add self.price() and update whenever called and items were changed
    def get_price(self):
        response = self._send(PRICE_URL, True)
        return response['Status'] != -1

    # TODO: Actually test this
    def place(self, card):
        print 'Placing order...'
        self.pay_with(card)
        response = self._send(PLACE_URL, False)
        return response

    def pay_with(self, card):
        """Use this instead of self.place when testing"""
        assert self.get_price()
        self.credit_card = card
        info = {'Type': 'CreditCard'}
        info['Expiration'] = card.expiration
        info['Amount'] = self.data['Amounts'].get('Customer', 0)
        info['CardType'] = card.card_type
        info['Number'] = card.number
        info['SecurityCode'] = card.cvv
        info['PostalCode'] = card.zip
        self.data['Payments'] = [info]
