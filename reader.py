import xml.etree.cElementTree as ET
import re

from classes import *

def ReadFromFiles(OFFERS_XML, IMPORT_XML, catalog_data):

    categories_list = []

    offers_et = ET.parse(OFFERS_XML)
    offers_root = offers_et.getroot()

    import_et = ET.parse(IMPORT_XML)
    import_root = import_et.getroot()

    def find_categories(grougs):
        categories_list.append([grougs[0][0].text , grougs[0][1].text])
        try:
            groups = grougs[0][2]
            find_categories(groups)
        except:
            pass

    find_categories(import_root[0][3])
    catalog_data.categories = categories_list


    def check_offerpic(product):
        if product.findall('{urn:1C.ru:commerceml_2}Картинка') == []:
            return False
        else:
            return True

    def check_description(product):
        if product[5].text[-3:] == 'DEL':
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
        if check_offerpic(product) and check_description(product):
            offerId = product[0].text
            product_set[offerId] = OfferData()
            product_set[offerId].offerId = offerId
            product_set[offerId].vendorCode = product[1].text
            product_set[offerId].name = product[2].text
            product_set[offerId].categoryId = product[4][0].text
            product_set[offerId].description = product[5].text
            pictures = product.findall('{urn:1C.ru:commerceml_2}Картинка')
            for picture in pictures:
                product_set[offerId].pictures.append(picture.text)
            product_id = product.find('{urn:1C.ru:commerceml_2}ЗначенияРеквизитов')[0][1].text[2:]
            product_set[offerId].id = product_id
            for category in catalog_data.categories:
                if category[0] == product_set[offerId].categoryId:
                    product_set[offerId].vendor = category[1]
                    break






