

class OfferData:
    def __init__(self):
        self.id = ''
        self.available = 'true'
        self.url = 'https://www.polyanka.pl'
        self.current_price = ''
        self.prices = {}
        self.currencyId = 'RUB'
        self.categoryId = ''
        self.pictures = []
        self.delivery = 'true'
        self.dimensions = '30/30/5'
        self.weight = '0.5'
        self.vendor = ''
        self.vendorCode = ''
        self.name = ''
        self.description = ''
        self.quantity = ''
        self.size = ''

    def set_price(self, priceId):
        self.current_price = self.prices[priceId]


class CatalogData:
    def __init__(self):
        self.name = 'Polyanka PL'
        self.company = 'ИП Ковалева Екатерина Дмитриевна'
        self.url = 'https://www.polyanka.pl'
        self.currency = {'id': 'RUB', 'rate': '1'}
        self.categories = []
