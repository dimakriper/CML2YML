import re


class OfferData:
    def __init__(self):
        self.id = ''                            #import
        self.offerId = ''                       #import
        self.available = 'true'
        self.url = 'https://www.polyanka.pl'
        self.current_price = ''                         #set_price
        self.prices = {}                            #offers
        self.currencyId = 'RUB'
        self.categoryId = ''                    #import
        self.pictures = []                      #import
        self.delivery = 'true'
        self.dimensions = '30/30/5'
        self.weight = '0.5'
        self.vendor = ''                        #import
        self.vendorCode = ''                    #import
        self.name = ''                          #import
        self.description = ''                   #import
        self.quantity = ''                          #offers
        self.size = None                              #offers
        self.sizes_available= ''                   #offers

    def set_price(self, priceId):
        self.current_price = self.prices[priceId]

    def simplify_description(self):
        simpl_des = self.description
        if re.search(r'Производство:.*', simpl_des) is not None:
            simpl_des = re.sub(r'Производство:.*', '', simpl_des)
        simpl_des = simpl_des + 'Размеры в наличии: ' + ''.join(self.sizes_available)
        return simpl_des


class CatalogData:
    def __init__(self):
        self.name = 'Polyanka PL'
        self.company = 'ИП Ковалева Екатерина Дмитриевна'
        self.url = 'https://www.polyanka.pl'
        self.currency = {'id': 'RUB', 'rate': '1'}
        self.categories = []
