from classes import *
from writer import *
from reader import *
from manage import *
from logger import logger


"""
This script convert data from CMLs (1C commercial data XML docs)
to requested set of YMLs (Yandex Market format XML docs)

attension: some names may not represent the content
"""

logger.info('START')

try:
    # header with categories
    catalog_data = CatalogData()
    # list of tuples: ('offersX_X.path", 'importX_X.path") to parse
    list_of_pairs = match_pairs(webdata_folder)
    # get list of dicts: {offerid : OfferData()} and pass categories to catalog_data
    logger.info('Collecting data from pairs ....')
    dataset = collect_data(list_of_pairs, catalog_data)
    prepare_folder(pictures_dir)
    logger.info('yml/webdata/import_files updated')
    # list of lists: ['output_file_name', '1 or 2'(1=default, 2=simplified mode), 'currency_id']
    scopes = find_scopes(csv_file)
    # finally create some ymls from collected data
    for scope in scopes:
        logger.info('Creating YML with name : %s, type : %s, price type : %s settings ....' % (scope[0], scope[1], scope[2]))
        create_yml(catalog_data, dataset, scope)
except:
    logger.exception("Exception occurred")
    logger.info('END\n\n')
    raise

logger.info('Program finished successfully.')
logger.info('END\n\n')

# # test script

# pairs = [['XML/webdata/offers0_1.xml','XML/webdata/import0_1.xml']]
# dataset = collect_data(pairs, catalog_data)
# create_yml(catalog_data, dataset, ['test2', '1', '2613b2a7-c8df-11ea-9122-001c42b99c64'])
# create_yml(catalog_data, dataset, ['test2_simplified', '2', '2613b2a7-c8df-11ea-9122-001c42b99c64'])
