from .address import Address

class Customer:
    """The Customer who orders a pizza."""

    def __init__(self, fname='', lname='', email='', phone='', address=None):
        self.first_name = fname.strip()
        self.last_name = lname.strip()
        self.email = email.strip()
        self.phone = str(phone).strip()
        self.address = Address(*address.split(','))

    def __repr__(self):
        return "Name: {} {}\nEmail: {}\nPhone: {}\nAddress: {}".format(
            self.first_name,
            self.last_name,
            self.email,
            self.phone,
            self.address,
        )
