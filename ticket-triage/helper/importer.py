'''
A helper package that allows to import modules dynamically, and to perform 
dependency injection to keep the app flexible and ticketing-system independent.
'''
import importlib
from importlib import util
from typing import List, Dict, Any
import configparser
import sys
import os

__IMPORTER_PATH = os.path.dirname(__file__)
__CONF_FILE = os.path.join(__IMPORTER_PATH, '../conf/conf.ini')
__PATH_TO_TICKETING_SYS = os.path.join(__IMPORTER_PATH, '../ticketing_systems')

'''
Allows to import a module dynamically by indicating its name as a string
'''
def import_from_string(module_name:str):
    print(f"IMPORTING FROM {module_name}")
    sys.path.insert(0,__PATH_TO_TICKETING_SYS)
    connector = f"{module_name}.connector"
    return importlib.import_module(connector,package="connector")


def import_from_config(section:str, key:str) -> str:
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    print(f"CONF FILE FOUND AT: {__CONF_FILE}")
    with open(__CONF_FILE, 'r') as fh:
        print(fh.readlines())
    print(conf.sections())
    return import_from_string( conf[section][key])


def import_config_list(section:str, key:str) -> List[str]:
    """
    Imports a list of strings from the config file. The strings 
    in the config file must be comma separated, with no white space between 
    them.
    """
    return import_from_config(section,key).split(",") 


'''
Returns the value of a config string.
'''
def get_config(section:str, key:str)->str:
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    return conf[section][key]

def import_ticketing_system():
    return import_from_config('ticketing_system','name')


def main():
    #print(type(import_ticketing_system()))
    print(get_config("classifier_datasets", "csv_path"))

if __name__ == '__main__':
    main()
