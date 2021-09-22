import xml.etree.cElementTree as ET
import re

from classes import *

def ReadFromFiles(OFFERS_XML, IMPORT_XML, catalog_data):

    categories_list = []

    offers_et = ET.parse(OFFERS_XML)
    offers_root = offers_et.getroot()

    import_et = ET.parse(IMPORT_XML)
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

    def CheckOfferpic(product):
        if product.findall('{urn:1C.ru:commerceml_2}Картинка') == []:
            return False
        else:
            return True

    def size_finder(product_name):
        size_data = re.search(product_name, r'Р(\w[\w]*)(-|/)?(\w[\w]*)?\)')

        match size_data.groups(1):
            case None:
                return size_data.groups(0)
            case '/':
                return [size_data.groups(0), size_data.groups(2)]
            case '-':
                return None

    products = import_root[1][4]
    product_set = {}
    for product in products:
        if CheckOfferpic(product):
            productId = product[0].text
            product_set[productId] = OfferData()
            product_set[productId].id = productId
            product_set[productId].vendorCode = product[1].text
            product_set[productId].name = product[2].text
            product_set[productId].categoryId = product[2][4].text






