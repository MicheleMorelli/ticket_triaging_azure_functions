'''
A helper package that allows to import modules dynamically, and to perform 
dependency injection to keep the app flexible and ticketing-system independent.
'''
import importlib
import configparser
import sys


__IMPORTER_PATH = sys.path[0]
__CONF_FILE = f"{__IMPORTER_PATH}/../conf/conf.ini"
__PATH_TO_TICKETING_SYS = '../ticketing_systems'

'''
Allows to import a module dynamically by indicating its name as a string
'''
def import_from_string(module_name:str):
    module_name = f"{__PATH_TO_TICKETING_SYS}/{module_name}" 
    print(f"IMPORTING FROM {module_name}")
    return importlib.import_module(module_name, package=http_)


def import_from_config(section:str, key:str):
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    return import_from_string(conf[section][key])


def import_ticketing_system():
    print (import_from_config('ticketing_system','name'))


def main():
    print(type(import_ticketing_system()))

if __name__ == '__main__':
    main()
