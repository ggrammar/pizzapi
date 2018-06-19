class Coupon(object):
    """Loose representation of a coupon - no logic. 

    This is a coupon - you can add it to an Order (order.add_item) and,
    if it fits, get some money off your purchase. I think. 

    This is another thing that's worth exploring - there are some sweet 
    coupons that would be awful without the coupon. 
    """
    def __init__(self, code, quantity=1):
        self.code = code
        self.quantity = quantity
        self.id = 1
        self.is_new = True
