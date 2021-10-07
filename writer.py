import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import copy
import os
from logger import  logger
from classes import *

"""
header = CatalogData() obj with categories
body: list of dicts of offers for every catalogue
scope: list with settings 
"""

def create_yml(header, body, scope):
    yml_name = scope[0] + '.xml'
    mode = scope[1]
    price_code = scope[2]

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    # create header
    data = ET.Element('yml_catalog')
    data.set('date', dt_string)
    shop = ET.SubElement(data, 'shop')
    name = ET.SubElement(shop, 'name')
    name.text = header.name
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
    # create body
    offers = ET.SubElement(shop, 'offers')

    # add offer to body
    # mode = '1' for regular yml, '2' for simplified
    for data_dict in body:
        for i in data_dict.values():
            if i.quantity =='':
                print(i.quantity, i.name, i.size, i.offerId)

        if mode == '1':
            offers_collection = data_dict.values()
        else:
            # only offers with unique ids
            offers_collection = []
            id_list = []
            for item in data_dict.values():
                try:
                    if item.id not in id_list:
                        item = copy.deepcopy(item)
                        for i in data_dict.values():
                            if i.id == item.id and i.quantity_is_positive():
                                item.available = 'true'
                                break
                        offers_collection.append(item)
                        id_list.append(item.id)
                except:
                    logger.error('%s raised an error' % item.name)
                    raise

        for item in offers_collection:
            if price_code in item.prices:
                try:
                    offer = ET.SubElement(offers, 'offer')
                    offer.set('id', item.id)
                    offer.set('available', item.available)
                    url = ET.SubElement(offer, 'url')
                    url.text = item.url
                    item.set_price(price_code) # test
                    price = ET.SubElement(offer, 'price')
                    price.text = item.current_price
                    if mode == '1':
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
                    weight = ET.SubElement(offer, 'weight')
                    weight.text = item.weight
                    vendor = ET.SubElement(offer, 'vendor')
                    vendor.text = item.vendor
                    vendorCode = ET.SubElement(offer, 'vendorCode')
                    vendorCode.text = item.vendorCode
                    name = ET.SubElement(offer, 'name')
                    name.text = item.name
                    description = ET.SubElement(offer, 'description')
                    if mode == '1':
                        description.text = item.description
                        if item.size is not None:
                            param = ET.SubElement(offer, 'param')
                            param.set('name', 'Размер')
                            param.text = item.size
                    else:
                        description.text = item.simplify_description()
                except:
                    logger.error('%s raised an error' % item.name)
                    raise

    mydata = minidom.parseString(ET.tostring(data)).toprettyxml(indent='    ')

    # os.mkdir('yml')
    with open(f'yml/{yml_name}', 'w', encoding='utf-8') as yml:
        yml.write(mydata)

