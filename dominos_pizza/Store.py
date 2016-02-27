from utils import request_json
from Menu import Menu

INFO_URL = 'https://order.dominos.com/power/store/{storeID}/profile'
MENU_URL = ('https://order.dominos.com/power/store/{storeID}/menu?'
            'lang={lang}&structured=true')
FIND_URL = ('https://order.dominos.com/power/store-locator?'
            's={line1}&c={line2}&type={type}')


class Store(object):
    def __init__(self, data={}):
        self.id = data.get('StoreID')
        self.info = data

    def get_details(self):
        details = request_json(INFO_URL, storeID=self.id)
        return details

    def get_menu(self, lang='en'):
        response = request_json(MENU_URL, storeID=self.id, lang=lang)
        menu = Menu(response)
        return menu

# TODO: Accomodate addresses with less information
# TODO: Assert delivery method is either 'Delivery' or 'CarryOut'
def find_stores(address, method='Delivery'):
    line1 = address.data['Street']
    line2 = '{City}, {Region}, {PostalCode}'.format(**address.data)
    data = request_json(FIND_URL, line1=line1, line2=line2, type=method)
    is_online = lambda x: x['IsOnlineNow'] and x['ServiceIsOpen'][method]
    return [Store(x) for x in data['Stores'] if is_online(x)]

def find_closest_store(address):
    stores = find_stores(address)
    if not len(stores):
        raise Exception('No local stores are currently open')
    return stores[0]

if __name__ == '__main__':
    from Address import Address
    addr = Address('700 Pennsylvania Avenue', 'Washington', 'DC', '20408')
    store = find_closest_store(addr)
    print 'StoreId:', store.id
    menu = store.get_menu()
    print 'Menu:'
    menu.display()

