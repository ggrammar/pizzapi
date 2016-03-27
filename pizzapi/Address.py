class Address(object):
    def __init__(self, street, city, region='', zip=''):
        data = {'Street': street.strip(), 'City': city.strip(),
                'Region': region.strip(), 'PostalCode': str(zip).strip()}
        self.data = {k: v for k, v in data.items() if v}

class Coupon(object):
    def __init__(self, code, quantity=1):
        self.code = code
        self.quantity = quantity
        self.id = 1
        self.is_new = True

class Customer(object):
    def __init__(self, fname='', lname='', email='', phone='', address=None):
        self.first_name = fname.strip()
        self.last_name = lname.strip()
        self.email = email.strip()
        self.phone = str(phone).strip()
        self.address = None if not address else address.data

    def set_address(self, street, city, region='', zip=''):
        self.address = Address(street, city, region, zip)

# TODO: Find out why this occasionally hangs
def request_json(url, **kwargs):
    r = requests.get(url.format(**kwargs))
    r.raise_for_status()
    return r.json()

def request_xml(url, **kwargs):
    r = requests.get(url.format(**kwargs))
    r.raise_for_status()
    return xmltodict.parse(r.text)
