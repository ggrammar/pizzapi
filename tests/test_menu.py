import json
import os

from hamcrest import *
from mock import patch
from pytest import mark

from pizzapi.menu import Menu
from pizzapi.urls import MENU_URL


fixture_path = os.path.join('tests', 'fixtures', 'menu.json')
with open(fixture_path) as fp:
    menu_fixture = json.load(fp)



def mocked_request_json(url, **kwargs):
    assert_that(url, equal_to(MENU_URL))
    assert_that(kwargs, has_items('store_id', 'lang'))
    return menu_fixture


@patch('pizzapi.address.request_json', side_effect=mocked_request_json)
def test_menu_from_store(store_id):
    pass
