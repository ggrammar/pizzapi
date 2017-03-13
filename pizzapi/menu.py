import json


# TODO: Get rid of this class
class MenuCategory(object):
    def __init__(self, menu_data={}, parent=None):
        self.menu_data = menu_data
        self.subcategories = []
        self.products = []
        self.parent = parent
        self.code = menu_data['Code']
        self.name = menu_data['Name']

    def get_category_path(self):
        path = '' if not self.parent else self.parent.get_category_path()
        return path + self.code


# TODO: Get rid of this class
class MenuItem(object):
    def __init__(self, data={}):
        self.code = data['Code']
        self.name = data['Name']
        self.menu_data = data
        self.categories = []


class Menu(object):
    def __init__(self, data={}):
        self.variants = data.get('Variants', {})
        self.menu_by_code = {}
        self.root_categories = {}
        if self.variants:
            self.products = self.parse_items(data['Products'])
            self.coupons = self.parse_items(data['Coupons'])
            self.preconfigured = self.parse_items(data['PreconfiguredProducts'])
            for key, value in data['Categorization'].iteritems():
                self.root_categories[key] = self.build_categories(value)

    # TODO: Reconfigure structure to show that Codes (not ProductCodes) matter
    def build_categories(self, category_data, parent=None):
        category = MenuCategory(category_data, parent)
        for subcategory in category_data['Categories']:
            new_subcategory = self.build_categories(subcategory, category)
            category.subcategories.append(new_subcategory)
        for product_code in category_data['Products']:
            if product_code not in self.menu_by_code:
                msg = 'PRODUCT NOT FOUND: %s %s'
                raise Exception(msg % (product_code, category.code))
            product = self.menu_by_code[product_code]
            category.products.append(product)
            product.categories.append(category)
        return category

    def parse_items(self, parent_data):
        items = []
        for code in parent_data.iterkeys():
            obj = MenuItem(parent_data[code])
            self.menu_by_code[obj.code] = obj
            items.append(obj)
        return items

    # TODO: Print codes that can actually be used to order items
    def display(self):
        def print_category(category, depth=1):
            indent = "  " * (depth + 1)
            if len(category.products) + len(category.subcategories) > 0:
                print indent + category.name
                for subcategory in category.subcategories:
                    print_category(subcategory, depth + 1)
                for product in category.products:
                    print indent + "  [%s]" % product.code, product.name
        print "************ Coupon Menu ************"
        print_category(self.root_categories['Coupons'])
        print "\n************ Preconfigured Menu ************"
        print_category(self.root_categories['PreconfiguredProducts'])
        print "\n************ Regular Menu ************"
        print_category(self.root_categories['Food'])

    # TODO: Find more pythonic way to format the menu
    # TODO: Format the menu after the variants have been filtered
    # TODO: Return the search results and print in different method
    # TODO: Import fuzzy search module or allow lists as search conditions
    def search(self, **conditions):
        max_len = lambda x: 2 + max(len(v[x]) for v in self.variants.values())
        for v in self.variants.itervalues():
            e = v.copy()
            e['Toppings'] = eval('dict(' + v['Tags']['DefaultToppings'] + ')')
            if all(y in e.get(x, '') for x, y in conditions.iteritems()):
                print e['Code'].ljust(max_len('Code')),
                print e['Name'].ljust(max_len('Name')),
                print ('$' + e['Price']).ljust(max_len('Price')),
                print e['SizeCode'].ljust(max_len('SizeCode')),
                print e['ProductCode'].ljust(max_len('ProductCode')),
                print e['Tags']['DefaultToppings']
