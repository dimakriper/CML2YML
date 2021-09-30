import xml.etree.ElementTree as ET
import copy
import re

from classes import *

def collect_data(list_of_pairs, catalog_data):
    data = []

    # groups: <Группы> tag in input file
    # add categories (id, text) to CatalogData() obj
    # for every "import.xml" file
    # if obj.categories doesnt already content it
    def find_categories(groups):
        category_data = groups[0][0].text, groups[0][1].text
        if category_data not in catalog_data.categories:
            catalog_data.categories.append(category_data)
        try:
            groups = groups[0][2]
            find_categories(groups)
        except:
            pass

    def parse_pairs(OFFERS_XML, IMPORT_XML):

        offers_et = ET.parse(OFFERS_XML)
        offers_root = offers_et.getroot()

        import_et = ET.parse(IMPORT_XML)
        import_root = import_et.getroot()


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
            size_data = re.search(r'Р(\w[\w]*)([-/])?(\w[\w]*)?\)', product_name)
            mid_symbol = size_data.groups()[1]
            first_size = size_data.groups()[0]
            last_size = size_data.groups()[2]
            if mid_symbol is None:
                # M
                return first_size
            elif mid_symbol == '/':
                # M/L
                return [first_size, last_size]
            elif mid_symbol == '-':
                # M-XL
                return None

        def quantity_is_positive(product_obj):
            return True if product_obj.quantity != '0' else False

        # set sizes to sizes_available attrib
        # of every OfferData obj in set
        # depending on id, quantity and size
        # of every offer
        def set_sizes_available(product_obj_set):
            dict_of_available = {}  # id : [sizes]
            list_of_sizes = []
            current_id = None
            for product_obj in product_obj_set.values():
                if product_obj.size is not None:
                    if quantity_is_positive(product_obj):
                        # for the 1st object in queue set current id: add size to list
                        if current_id is None and product_obj.id is not None:
                            current_id = product_obj.id
                            list_of_sizes.append(product_obj.size)
                        # continue adding sizes to list
                        elif product_obj.id == current_id and product_obj.id is not None:
                            list_of_sizes.append(product_obj.size)
                        # push list to dict with current id and set next "current_id", add size to new list
                        elif product_obj.id != current_id and product_obj.id is not None:
                            dict_of_available[current_id] = list_of_sizes
                            current_id = product_obj.id
                            list_of_sizes = [product_obj.size]
            # set available sizes from dict to objs by suitable ids
            for product_obj in product_obj_set.values():
                if product_obj.id in dict_of_available:
                    product_obj.sizes_available = dict_of_available[product_obj.id]

        # This code works with importX_X input file
        # It creates OfferData() objs dynamically with "product_set" dict
        # and sets most of their attribs by parsing importX_X
        # products: <Товары> tag in input file
        products = import_root[1][4]
        product_set = {}  # offerId : OfferData() obj
        for product in products:
            if check_offerpic(product) and check_description(product):
                offerId = product[0].text
                product_set[offerId] = OfferData()
                product_set[offerId].offerId = offerId
                product_set[offerId].vendorCode = product[1].text
                name = product[2].text
                # delete size information from name
                name = re.sub(r' \(Р(\w[\w]*)([-/])?(\w[\w]*)?\)', '', name)
                product_set[offerId].name = name
                product_set[offerId].categoryId = import_root[0][3][0][2][0][0].text
                product_set[offerId].vendor_id = product[4][0].text
                product_set[offerId].description = product[5].text
                pictures = product.findall('{urn:1C.ru:commerceml_2}Картинка')
                for picture in pictures:
                    product_set[offerId].pictures.append('https://www.polyanka.pl/yml/webdata/' + picture.text)
                product_id = product.find('{urn:1C.ru:commerceml_2}ЗначенияРеквизитов')[0][1].text[2:]
                product_set[offerId].id = product_id
                for category in catalog_data.categories:
                    if category[0] == product_set[offerId].vendor_id:
                        product_set[offerId].vendor = category[1]
                        break

        # This code works with offersX_X input file
        # 1) get offerId from every subelement of "offers"
        # 2) check if offerid in "product_set" keys
        # 3) set attribs to suitable OfferData() obj
        # offers: <Предложения> tag in input file
        offers = offers_root[1][7]
        for offer in offers:
            offerId = offer[0].text
            if offerId in product_set:
                currencies = offer[4]
                for currency in currencies:
                    product_set[offerId].prices[currency[1].text] = currency[2].text
                product_set[offerId].quantity = offer[5].text
                size_data = size_finder(offer[2].text)
                if type(size_data) is list:
                    # create copy of current object but with another size
                    product_set[offerId+'_add_size'] = copy.deepcopy(product_set[offerId])
                    product_set[offerId].size = size_data[0]
                    product_set[offerId + '_add_size'].size = size_data[1]
                else:
                    product_set[offerId].size = size_data

        set_sizes_available(product_set)

        return product_set

    for pair in list_of_pairs:
        data.append(parse_pairs(pair[0], pair[1]))

    return data









