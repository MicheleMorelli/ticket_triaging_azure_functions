'''
A helper package that allows to import modules dynamically, and to perform 
dependency injection to keep the app flexible and ticketing-system independent.
'''
import importlib
import configparser
import sys
'''
Allows to import a module dynamically by indicating its name as a string
'''
def import_from_string(module_name:str):
    return importlib.import_module


def import_from_config(section:str, key:str):
    __IMPORTER_PATH = sys.path[0]
    __CONF_FILE = f"{__IMPORTER_PATH}/../conf/conf.ini"
    conf = configparser.ConfigParser()
    conf.read(__CONF_FILE)
    return conf[section][key]


def import_ticketing_system():
    print (import_from_config('ticketing_system','name'))

def main()->None:
    import_ticketing_system()


if __name__ == '__main__':
    main()
