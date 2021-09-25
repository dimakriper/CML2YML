import xml.etree.cElementTree as ET
import re
import copy

from classes import *

def ReadFromFiles(OFFERS_XML, IMPORT_XML, catalog_data):

    offers_et = ET.parse(OFFERS_XML)
    offers_root = offers_et.getroot()

    import_et = ET.parse(IMPORT_XML)
    import_root = import_et.getroot()

    def find_categories(groups):
        category_data = groups[0][0].text , groups[0][1].text
        if category_data not in catalog_data.categories:
            catalog_data.categories.append(category_data)
        try:
            groups = groups[0][2]
            find_categories(groups)
        except:
            pass
        return

    find_categories(import_root[0][3])

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
        size_data = re.search(r'P(\w[\w]*)(-|/)?(\w[\w]*)?\)', product_name)

        match size_data.groups(1):
            case None:
                return size_data.groups(0)
            case '/':
                return [size_data.groups(0), size_data.groups(2)]
            case '-':
                return None

    def quantity_is_positive(product_obj):
        return True if product_obj.quantity != '0' else False

    def set_sizes_available(product_obj_set):
        dict_of_available = {}
        list_of_sizes = []
        current_id = None
        for product_obj in product_obj_set.values():
            if product_obj.size is not None:
                if quantity_is_positive(product_obj):
                    if current_id is None and product_obj.id is not None:
                        current_id = product_obj.id
                        list_of_sizes.append(product_obj.size)
                    elif product_obj.id == current_id and product_obj.id is not None:
                        list_of_sizes.append(product_obj.size)
                    elif product_obj.id != current_id and product_obj.id is not None:
                        dict_of_available[current_id] = list_of_sizes
                        current_id = product_obj.id
                        list_of_sizes = [product_obj.size]
        for product_obj in product_obj_set.values():
            if product_obj.id in dict_of_available:
                product_obj.sizes_available = dict_of_available[product_obj.id]

    products = import_root[1][4]
    product_set = {}
    for product in products:
        if check_offerpic(product) and check_description(product):
            offerId = product[0].text
            product_set[offerId] = OfferData()
            product_set[offerId].offerId = offerId
            product_set[offerId].vendorCode = product[1].text
            name = product[2].text
            name = re.sub(r' \(Р(\w[\w]*)(-|/)?(\w[\w]*)?\)', '', name)
            product_set[offerId].name = name
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

    offers = offers_root[1][7]
    for offer in offers:
        offerId = offer[0].text
        currencies = offer[4]
        for currency in currencies:
            product_set[offerId].prices[currency[1].text] = currency[2].text
        product_set[offerId].quantity = offer[5].text
        size_data = size_finder(offer[2].text)
        if type(size_data) is list:
            product_set[offerId+'_add_size'] = copy.deepcopy(product_set[offerId])
            product_set[offerId].size = size_data[0]
            product_set[offerId + '_add_size'].size = size_data[1]
        else:
            product_set[offerId].size = size_data

    set_sizes_available(product_set)
    return product_set










