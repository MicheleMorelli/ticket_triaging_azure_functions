"""
A helper package that allows to read values from the conf.ini file, 
import modules dynamically, and to perform dependency injection to 
keep the app flexible and ticketing-system independent.
"""
import importlib
from importlib import util
from typing import List, Dict, Any
import types
import configparser
import sys
import os

__IMPORTER_PATH = os.path.dirname(__file__)
__CONF_FILE = os.path.join(__IMPORTER_PATH, 'conf.ini')
__PATH_TO_TICKETING_SYS = os.path.join(__IMPORTER_PATH, '../ticketing_systems')

def import_from_string(module_name: str) -> types.ModuleType:
    """
    Allows to import a module dynamically by indicating its name as a string
    """
    print(f"IMPORTING FROM {module_name}")
    sys.path.insert(0,__PATH_TO_TICKETING_SYS)
    connector = f"{module_name}.connector"
    return importlib.import_module(connector,package="connector")


def import_from_config(section: str, key: str) -> types.ModuleType:
    """
    Imports a module from config
    """
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    print(f"CONF FILE FOUND AT: {__CONF_FILE}")
    with open(__CONF_FILE, 'r') as fh:
        print(fh.readlines())
    print(conf.sections())
    return import_from_string( conf[section][key])


def import_config_list(section: str, key: str, separator: str) -> List[str]:
    """
    Imports a list of strings from the config file.
    """
    return get_config(section,key).split(separator) 


def get_config(section: str, key: str) -> str:
    """
    Returns the value of a config string.
    """
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    return conf[section][key]

def import_ticketing_system() -> types.ModuleType:
    """
    Imports a module related to a concrete implementation of a ticketing 
    system.
    """
    return import_from_config('ticketing_system','name')


if __name__ == '__main__':
    #print(type(import_ticketing_system()))
    print(get_config("classifier_datasets", "csv_path"))
