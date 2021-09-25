import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

from classes import *

def create_subelem_with_text(parent, name, item):
    subelem = ET.SubElement(parent, f'{name}')
    subelem.text = item.name

def create_yml(header, body):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    data = ET.Element('yml_catalog')
    data.set('date', dt_string)
    shop = ET.SubElement(data, 'shop')
    create_subelem_with_text(shop, name, )
    company = ET.SubElement(shop, 'company')
    company.text = header.company
    url = ET.SubElement(shop, 'url')
    url.text = header.url
    currencies = ET.SubElement(shop, 'currencies')
    currency = currencies.makeelement('currency', header.currency)
    currencies.append(currency)
    categories = ET.SubElement(shop, 'categories')
    for cat in header.categories:
        category = ET.SubElement(categories, 'category')
        category.set('id', cat[0])
        category.text = cat[1]
    offers = ET.SubElement(shop, 'offers')
    offers_collection = body.values()
    for item in offers_collection:
        offer = ET.SubElement(offers, 'offer')
        offer.set('id', item.id)
        offer.set('available', item.available)
        url = ET.SubElement(offer, 'url')
        url.text = item.url
        item.set_price(item.prices.values[1]) # test
        price = ET.SubElement(offer, 'price')
        price.text = item.current_price
        quantity = ET.SubElement(offer, 'quantity')
        quantity.text = item.quantity
        currencyId = ET.SubElement(offer, 'currencyId')
        currencyId.text = item.currencyId
        categoryId = ET.SubElement(offer, 'categoryId')
        categoryId.text = item.categoryId
        for pic in item.pictures:
            picture = ET.SubElement(offer, 'picture')
            picture.text = pic
        delivery = ET.SubElement(offer, 'delivery')
        delivery.text = item.delivery
        dimensions = ET.SubElement(offer, 'dimensions')
        dimensions.text = item.dimensions

    mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent = '    ')
    with open ('test.xml', 'w', encoding='utf-8') as test:
        test.write(mydata)

