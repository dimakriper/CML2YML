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
        assert groups.tag != '{urn:1C.ru:commerceml_2}Группы'
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
            if product.findall('{urn:1C.ru:commerceml_2}Картинка') != []:
                return True

        def check_description(product):
            description = product.find('{urn:1C.ru:commerceml_2}Описание')
            if description is not None:
                if len(description.text) > 0:
                    if description.text[-3:] != 'DEL':
                        return True

        def size_finder(product_name):
            size_data = re.search(r'Р(\w[\w]*)([-\/])?(\w[\w]*)?\)', product_name)
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

        # set sizes to sizes_available attrib
        # of every OfferData obj in set
        # depending on id, quantity and size
        # of every offer
        def set_sizes_available(product_obj_set):
            dict_of_available = {}  # id : [sizes]
            id_list = []
            # fill unique ids in dict_of_available as keys and assign to []
            for product_obj in product_obj_set.values():
                if product_obj.id not in id_list:
                    dict_of_available[product_obj.id] = []
                    id_list.append(product_obj.id)
            # fill id : [] with sizes
            for product_obj in product_obj_set.values():
                if product_obj.size is not None and product_obj.quantity_is_positive():
                    dict_of_available[product_obj.id].append(product_obj.size)
            # assign sizes_available attrib of every product_obj to list from dict_of_available by id
            for product_obj in product_obj_set.values():
                product_obj.sizes_available = dict_of_available[product_obj.id]

        # This code works with importX_X input file
        # It creates OfferData() objs dynamically with "product_set" dict
        # and sets most of their attribs by parsing importX_X
        # products: <Товары> tag in input file
        products = import_root[1][4]
        assert products.tag != '{urn:1C.ru:commerceml_2}Группы'
        product_set = {}  # offerId : OfferData() obj
        for product in products:
            if check_offerpic(product) and check_description(product):
                offerId = product.find('{urn:1C.ru:commerceml_2}Ид').text
                product_set[offerId] = OfferData()
                product_set[offerId].offerId = offerId
                product_set[offerId].vendorCode = product.find('{urn:1C.ru:commerceml_2}Артикул').text
                name = product.find('{urn:1C.ru:commerceml_2}Наименование').text
                # delete size information from name
                name = re.sub(r' *\( *[\w]* *Р *(\w[\w]*) *([-\/])? *(\w[\w]*)?\)', '', name)
                product_set[offerId].name = name
                product_set[offerId].categoryId = import_root[0][3][0][2][0][0].text
                assert not re.match(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', product_set[offerId].categoryId)
                product_set[offerId].vendor_id = product.find('{urn:1C.ru:commerceml_2}Группы')[0].text
                assert not re.match(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}', product_set[offerId].vendor_id)
                product_set[offerId].description = product.find('{urn:1C.ru:commerceml_2}Описание').text
                pictures = product.findall('{urn:1C.ru:commerceml_2}Картинка')
                for picture in pictures:
                    product_set[offerId].pictures.append('https://www.polyanka.pl/yml/webdata/' + picture.text)
                product_id = product.find('{urn:1C.ru:commerceml_2}ЗначенияРеквизитов')[0][1].text
                assert product.find('{urn:1C.ru:commerceml_2}ЗначенияРеквизитов')[0][0].text != 'Код'
                product_id = re.search(r'[\d]+', product_id).group()
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
        assert offers.tag != '{urn:1C.ru:commerceml_2}Предложения'
        for offer in offers:
            offerId = offer.find('{urn:1C.ru:commerceml_2}Ид').text
            if offerId in product_set:
                currencies = offer.find('{urn:1C.ru:commerceml_2}Цены')
                for currency in currencies:
                    product_set[offerId].prices[currency.find('{urn:1C.ru:commerceml_2}ИдТипаЦены').text] = currency.find('{urn:1C.ru:commerceml_2}ЦенаЗаЕдиницу').text
                product_set[offerId].quantity = offer[5].text
                if not product_set[offerId].quantity_is_positive():
                    product_set[offerId].available = 'false'
                size_data = size_finder(offer.find('{urn:1C.ru:commerceml_2}Наименование').text)
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









