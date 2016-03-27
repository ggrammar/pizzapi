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
menu.search(SizeCode='12', Name='Handmade')

print 'Prompting for Items to order...'
for item in raw_input('Add Items: ').split():
    added = order.add_item(item.upper())
    print 'Added item:', added['Name']

print 'Creating the PaymentObject...'
card = PaymentObject('4100123422343234', '0115', '777', '90210')

print 'Placing the order...'
order.pay_with(card)
data = order.data

# data = order.place(card)

# TODO: Add order tracking tests here

print'Success\n\norder.data:', json.dumps(data, indent=4)
