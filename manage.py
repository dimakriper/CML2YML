import os
from configparser import ConfigParser
import re

config = ConfigParser()
config.read('settings.ini')
roots = config['ROOTS']
webdata_folder = roots['webdata_root']
csv_file = roots['csv_root']


def match_pairs(directory):
    list_of_pairs = []
    folder_string = ' '.join(os.listdir(directory))
    # pattern = r'([A-Za-z]+)([\d]+_[\d]+).xml'
    import_list = re.findall(r'import[\d]+_[\d]+.xml', folder_string)
    offers_list = re.findall(r'offers[\d]+_[\d]+.xml', folder_string)
    for import_file in import_list:
        for offers_file in offers_list:
            if re.search(r'[\d]+_[\d]+', import_file).group() == re.search(r'[\d]+_[\d]+', offers_file).group():
                list_of_pairs.append((os.path.join(directory, offers_file), os.path.join(directory, import_file)))
                break
    return list_of_pairs


def find_scopes(table):
    scopes = []
    with open(table) as csv:
        for row in csv:
            scope = row.rstrip().split(':')
            if len(scope) == 3:
                scopes.append(scope)
    return scopes
