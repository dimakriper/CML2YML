import os
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.ini')
roots = config['ROOTS']
webdata_folder = roots['webdata_root']