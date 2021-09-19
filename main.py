import xml.etree.cElementTree as ET
from xml.dom import minidom
import os
from datetime import datetime

# tree = ET.parse('yml_1.xml')
# root = tree.getroot()
#
# for child in root.iter('offer'):
#     print(child.tag, child.attrib, child.text)


class OfferData:
    def __init__(self):
        self.id = ''
        self.available = ''
        self.url = ''
        self.price = ''
        self.currencyId = ''
        self.categoryId = ''
        self.pictures = []
        self.delivery = ''
        self.dimensions = ''
        self.weight = ''
        self.vendor = ''
        self.vendorCode = ''
        self.name = ''
        self.description = ''


class CatalogData:
    def __init__(self):
        self.name = 'Polyanka PL'
        self.company = 'ИП Ковалева Екатерина Дмитриевна'
        self.url = 'https://www.polyanka.pl'
        self.currency = {'id': 'RUB', 'rate': '1'}
        self.categories = []


def WriteFile():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    catalog_data = CatalogData()

    data = ET.Element('yml_catalog')
    data.set('date', dt_string)
    shop = ET.SubElement(data, 'shop')
    name = ET.SubElement(shop, 'name')
    company = ET.SubElement(shop, 'company')
    url = ET.SubElement(shop, 'url')
    currencies =ET.SubElement(shop, 'currencies')
    currency = currencies.makeelement('currency', catalog_data.currency)
    currencies.append(currency)
    categories = ET.SubElement(shop, 'categories')

    mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent = '    ')
    with open ('test.xml', 'w', encoding='utf-8') as test:
        test.write(mydata)

WriteFile()