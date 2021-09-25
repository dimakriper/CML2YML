import writer
from classes import *
import copy
# from writer import *
# from reader import *

# tree = ET.parse('yml_1.xml')
# root = tree.getroot()
#
# for child in root.iter('offer'):
#     print(child.tag, child.attrib, child.text)








# catalog_data = CatalogData()
# catalog_data.name = '0'
# catalog_data1 = catalog_data
# catalog_data1.name = '1'
# print(catalog_data.name, catalog_data1.name)

# ReadFromFiles('webdata/offers0_1.xml','webdata/import0_1.xml', catalog_data)
writer.create_yml(CatalogData)

