import os
from configparser import ConfigParser
import re
from logger import logger
"""
This module is for getting paths to input data (CMLs in folder)
and settings for output files
"""

config = ConfigParser()
config.read('settings.ini')
roots = config['ROOTS']
webdata_folder = roots['webdata_root']
csv_file = roots['csv_root']
pictures_dir = roots['pictures_root']


# sort input files from directory into tuples by NUMBER_NUMBER in filename
# e.g. [("/../path/offers0_1.xml", "/../path/import0_1.xml)..]
def match_pairs(directory):
    list_of_pairs = []
    list_of_tails = []
    folder_string = ' '.join(os.listdir(directory))
    import_list = re.findall(r'import[\d]+_[\d]+.xml', folder_string)
    offers_list = re.findall(r'offers[\d]+_[\d]+.xml', folder_string)
    for import_file in import_list:
        for offers_file in offers_list:
            if re.search(r'[\d]+_[\d]+', import_file).group() == re.search(r'[\d]+_[\d]+', offers_file).group():
                list_of_pairs.append((os.path.join(directory, offers_file), os.path.join(directory, import_file)))
                list_of_tails.append((offers_file, import_file))
                break
    logger.info(f'Pairs found: {", ".join([" : ".join(pair) for pair in list_of_tails])}')
    return list_of_pairs


# extract settings from csv ( ":" - delimeter) to list
def find_scopes(table):
    scopes = []
    with open(table) as csv:
        for row in csv:
            scope = row.rstrip().split(':')
            if len(scope) == 3:
                scopes.append(scope)
    return scopes

def prepare_folder(pictures_dir):
    os.system(r'prepare_dirs.cmd %s' % pictures_dir)

prepare_folder(pictures_dir)

