class Coupon(object):
    def __init__(self, code, quantity=1):
        self.code = code
        self.quantity = quantity
        self.id = 1
        self.is_new = True
