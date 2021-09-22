from classes import *
from writer import *
from reader import *

# tree = ET.parse('yml_1.xml')
# root = tree.getroot()
#
# for child in root.iter('offer'):
#     print(child.tag, child.attrib, child.text)








catalog_data = CatalogData()

ReadFromFiles('webdata/offers0_1.xml','webdata/import0_1.xml', catalog_data)
WriteFile(catalog_data)

