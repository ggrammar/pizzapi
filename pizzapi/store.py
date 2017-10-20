from .menu import Menu
from .urls import Urls, COUNTRY_USA
from .utils import request_json


class Store(object):
    def __init__(self, data={}, country=COUNTRY_USA):
        self.id = str(data.get('StoreID', -1))
        self.country = country
        self.urls = Urls(country)
        self.data = data

    def get_details(self):
        details = request_json(self.urls.info_url(), store_id=self.id)
        return details

    def get_menu(self, lang='en'):
        response = request_json(self.urls.menu_url(), store_id=self.id, lang=lang)
        menu = Menu(response, self.country)
        return menu
