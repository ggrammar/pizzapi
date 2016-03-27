from pizzapi import *
import json

print 'Creating Customer...'
customer = Customer('Barack', 'Obama', 'barack@whitehouse.gov', '2024561111')
customer.set_address('700 Pennsylvania Avenue NW', 'Washington', 'DC', '20408')

print 'Finding closest Store...'
store = find_closest_store(customer.address)

print 'Creating Order...'
order = Order(store, customer)

print 'Searching the store\'s Menu for 12" Handmade pizzas...'
menu = store.get_menu()
menu.search(Name='Pan Pizza', SizeCode='12')
menu.search(Name='Marinara')
menu.search(Name='Coke')

order.add_item('P12IPAZA')
order.add_item('MARINARA')
order.add_item('2LCOKE')

order.remove_item('2LCOKE')
order.add_item('20BCOKE')

print 'Creating the PaymentObject...'
card = PaymentObject('4100123422343234', '0115', '777', '90210')

print 'Placing the order...'
order.pay_with(card)
data = order.data

# data = order.place(card)

# TODO: Add order tracking tests here

print'Success\n\norder.data:', json.dumps(data, indent=4)
