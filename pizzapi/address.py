class Address(object):
    def __init__(self, street, city, region='', zip=''):
        data = {'Street': street.strip(), 'City': city.strip(),
                'Region': region.strip(), 'PostalCode': str(zip).strip()}
        self.data = {k: v for k, v in data.items() if v}
