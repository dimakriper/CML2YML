import xml.etree.cElementTree as ET

from classes import *

def ReadFromFiles(OFFERS_XML, IMPORT_XML, catalog_data):

    offerslist = []
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

    # products = import_root[1][4]
    # for product in products:

