import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

from classes import *

def WriteFile(catalog_data):
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
    offers = ET.SubElement(shop, 'offers')


    mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent = '    ')
    with open ('test.xml', 'w', encoding='utf-8') as test:
        test.write(mydata)

