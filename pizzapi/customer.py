class Customer(object):
    def __init__(self, fname='', lname='', email='', phone='', address=None):
        self.first_name = fname.strip()
        self.last_name = lname.strip()
        self.email = email.strip()
        self.phone = str(phone).strip()
        self.address = address
