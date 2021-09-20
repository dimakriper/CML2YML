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
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    data = ET.Element('yml_catalog')
    data.set('date', dt_string)
    shop = ET.SubElement(data, 'shop')
    name = ET.SubElement(shop, 'name')
    name.text = catalog_data.name
    company = ET.SubElement(shop, 'company')
    company.text = catalog_data.company
    url = ET.SubElement(shop, 'url')
    url.text = catalog_data.url
    currencies = ET.SubElement(shop, 'currencies')
    currency = currencies.makeelement('currency', catalog_data.currency)
    currencies.append(currency)
    categories = ET.SubElement(shop, 'categories')
    for cat in catalog_data.categories:
        category = ET.SubElement(categories, 'category')
        category.set('id', cat[0])
        category.text = cat[1]

    mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent = '    ')
    with open ('test.xml', 'w', encoding='utf-8') as test:
        test.write(mydata)


def ReadFromFiles(offers_xml, import_xml):

    offerslist = []
    categories_list = []

    offers_et = ET.parse(offers_xml)
    offers_root = offers_et.getroot()

    import_et = ET.parse(import_xml)
    import_root = import_et.getroot()

    def FindCategories(grougs):
        categories_list.append([grougs[0][0].text , grougs[0][1].text])
        try:
            groups = grougs[0][2]
            FindCategories(groups)
        except:
            pass

    FindCategories(import_root[0][3])
    catalog_data.categories = categories_list

catalog_data = CatalogData()

ReadFromFiles('webdata/offers0_1.xml','webdata/import0_1.xml')
WriteFile()
