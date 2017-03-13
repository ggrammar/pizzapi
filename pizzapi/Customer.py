from Address import Address


class Customer(object):
    def __init__(self, fname='', lname='', email='', phone='', address=None):
        self.first_name = fname.strip()
        self.last_name = lname.strip()
        self.email = email.strip()
        self.phone = str(phone).strip()
        self.address = None if not address else address.data

    def set_address(self, street, city, region='', zip=''):
        self.address = Address(street, city, region, zip)
