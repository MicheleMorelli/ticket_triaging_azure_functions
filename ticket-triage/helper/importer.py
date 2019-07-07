'''
A helper package that allows to import modules dynamically, and to perform 
dependency injection to keep the app flexible and ticketing-system independent.
'''
import importlib
from importlib import util
import configparser
import sys

__IMPORTER_PATH = sys.path[0]
__CONF_FILE = f"{__IMPORTER_PATH}/../conf/conf.ini"
__PATH_TO_TICKETING_SYS = f"{__IMPORTER_PATH}/../ticketing_systems"

'''
Allows to import a module dynamically by indicating its name as a string
'''
def import_from_string(module_name:str):
    print(f"IMPORTING FROM {module_name}")
    sys.path.insert(0,__PATH_TO_TICKETING_SYS)
    return importlib.import_module(module_name,package="connector")




def import_from_config(section:str, key:str):
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    print(f"CONF FILE FOUND AT: {__CONF_FILE}")
    print(conf.sections())
    return import_from_string( conf[section][key])


def import_ticketing_system():
    return import_from_config('ticketing_system','name')


def main():
    print(type(import_ticketing_system()))

if __name__ == '__main__':
    main()
