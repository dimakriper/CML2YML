import os
from configparser import ConfigParser
import re

config = ConfigParser()
config.read('settings.ini')
roots = config['ROOTS']
webdata_folder = roots['webdata_root']


def match_pairs(directory):
    list_of_pairs = []
    folder_string = ' '.join(os.listdir(directory))
    pattern = r'([A-Za-z]+)([\d]+_[\d]+).xml'
    matches = re.findall(pattern, folder_string)
    print(matches)


match_pairs(webdata_folder)
