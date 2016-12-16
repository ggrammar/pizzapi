# pizzapi

This is a Python wrapper for the Dominos Pizza API.  

It's a port of [the pizzapi node.js module](https://github.com/RIAEvangelist/node-dominos-pizza-api) written by [RIAEvangelist](https://github.com/RIAEvangelist).

## Quick Start

First construct a `Customer` object and set the customer's address.
```python
>>> customer = Customer('Barack', 'Obama', 'barack@whitehouse.gov', '2024561111')
>>> customer.set_address('700 Pennsylvania Avenue NW', 'Washington', 'DC', '20408')
```

Then, find a store that will deliver to the address.
```python
>>> store = find_closest_store(customer.address)
```

Create an `Order` object.
```python
>>> order = Order(store, customer)
```

In order to add items to your order, you'll need the items' product codes.  
To find the codes, get the menu from the store, then search for items you want to add.
```python
>>> menu = store.get_menu()
>>> menu.search(Name='Pan Pizza', SizeCode='12')
P12IPAZA   Medium (12") Handmade Pan Pizza   $9.99
>>> order.add_item('P12IPAZA')
>>> menu.search(Name='Marinara')
PINBBLMM   Italian Sausage Marinara BreadBowl Pasta   $7.99
PINPASMM   Italian Sausage Marinara Pasta             $6.99
MARINARA   Side Marinara Sauce Dipping Cup            $0.75
>>> order.add_item('MARINARA')
>>> menu.search(Name='Coke')
20BCOKE    20oz Bottle Coke®        $1.89
20BDCOKE   20oz Bottle Diet Coke®   $1.89
D20BZRO    20oz Bottle Coke Zero™   $1.89
2LDCOKE    2-Liter Diet Coke®       $2.99
2LCOKE     2-Liter Coke®            $2.99
>>> order.add_item('20BCOKE')
```

You can remove items as well!
```python
>>> order.remove_item('20BCOKE')
```

Wrap your credit card information in a `PaymentObject`:
```python
>>> card = PaymentObject('4100123422343234', '0115', '777', '90210')
```

And that's it! Now you can place your order.
```python
>>> order.place(card)
```

Or if you're just testing and don't want to actually order something, use `.pay_with`.
```python
>>> order.pay_with(card)
```
