class Customer(object):
    """The Customer orders a pizza.

    You need a Customer to create an Order. The proprietors of the API
    use this information, presumably for nefarious Pizza Purposes.
    """

    def __init__(self, fname='', lname='', email='', phone=''):
        self.first_name = fname.strip()
        self.last_name = lname.strip()
        self.email = email.strip()
        self.phone = str(phone).strip()

