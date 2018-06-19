import json
import os

from hamcrest import *
from mock import patch
from pytest import mark

from pizzapy.address import Address
from pizzapy.urls import Urls, COUNTRY_USA


fixture_path = os.path.join('tests', 'fixtures', 'stores.json')
with open(fixture_path) as fp:
    stores_fixture = json.load(fp)


address_params = mark.parametrize(
    argnames=('street', 'city', 'region', 'zip'),
    argvalues=[
        ('700 Pennsylvania Avenue NW', 'Washington', 'DC', '20408'),
        ('700 Pennsylvania Avenue NW ', ' Washington ', ' DC ', ' 20408 '),
        ('700 Pennsylvania Avenue NW', 'Washington', 'DC', 20408)
    ]
)


def mocked_request_json(url, **kwargs):

    assert_that(url, equal_to(Urls(COUNTRY_USA).find_url()))
    assert_that(kwargs, has_entries(
        line1='700 Pennsylvania Avenue NW',
        line2='Washington, DC, 20408',
        type='Delivery'
    ))
    return stores_fixture


@address_params
def test_address_init(street, city, region, zip):
    address = Address(street, city, region, zip)
    assert_that(address, has_properties(
        street='700 Pennsylvania Avenue NW',
        city='Washington',
        region='DC',
        zip='20408',
        line1='700 Pennsylvania Avenue NW',
        line2='Washington, DC, 20408',
        data=has_entries(
            Street='700 Pennsylvania Avenue NW',
            City='Washington',
            Region='DC',
            PostalCode='20408'
        )
    ))


@address_params
@patch('pizzapy.address.request_json', side_effect=mocked_request_json)
def test_address_closest_store(mocked, street, city, region, zip):
    address = Address(street, city, region, zip)
    assert_that(address, has_properties(
        line1='700 Pennsylvania Avenue NW',
        line2='Washington, DC, 20408'
    ))

    store = address.closest_store()
    assert_that(store, has_properties(
        id='4336',
        data=has_entries(
            AddressDescription='1300 L St Nw\nWashington, DC 20005',
            AllowCarryoutOrders=True,
            AllowDeliveryOrders=True,
            HolidaysDescription='',
            HoursDescription='Su-Th 10:00am-1:00am\nFr-Sa 10:00am-2:00am',
            IsDeliveryStore=True,
            IsNEONow=False,
            IsOnlineCapable=True,
            IsOnlineNow=True,
            IsOpen=True,
            IsSpanish=False,
            LanguageLocationInfo=has_entries(
                es=None
            ),
            LocationInfo=None,
            MaxDistance=0.8,
            MinDistance=0.8,
            Phone='202-639-8700',
            ServiceHoursDescription=has_entries(
                Carryout='Su-Sa 10:00am-10:00pm',
                Delivery='Su-Th 10:00am-1:00am\nFr-Sa 10:00am-2:00am'
            ),
            ServiceIsOpen=has_entries(
                Carryout=True,
                Delivery=True
            ),
            StoreID='4336'
        )
    ))


@address_params
@patch('pizzapy.address.request_json', side_effect=mocked_request_json)
def test_address_nearby_stores(mocked, street, city, region, zip):
    address = Address(street, city, region, zip)
    assert_that(address, has_properties(
        line1='700 Pennsylvania Avenue NW',
        line2='Washington, DC, 20408'
    ))

    stores = address.nearby_stores()
    assert_that(stores, has_length(12))
    assert_that([x.data for x in stores], equal_to(stores_fixture['Stores']))


# print 'Creating Order...'
# order = Order(store, customer)
#
# print 'Searching the store\'s Menu for 12" Handmade pizzas...'
# menu = Menu.from_store(store_id=store.id)
#
# menu.search(Name='Pan Pizza', SizeCode='12')
# menu.search(Name='Marinara')
# menu.search(Name='Coke')
#
# order.add_item('P12IPAZA')
# order.add_item('MARINARA')
# order.add_item('2LCOKE')
#
# order.remove_item('2LCOKE')
# order.add_item('20BCOKE')
#
# print 'Creating the PaymentObject...'
# card = PaymentObject('4100123422343234', '0115', '777', '90210')
#
# print 'Placing the order...'
# order.pay_with(card)
# data = order.data
#
# # data = order.place(card)
#
# # TODO: Add order tracking tests here
#
# print'Success\n\norder.data:', json.dumps(data, indent=4)
