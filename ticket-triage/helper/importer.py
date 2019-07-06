'''
A helper package that allows to import modules dynamically, and to perform 
dependency injection to keep the app flexible and ticketing-system independent.
'''
import importlib
import configparser


'''
Allows to import a module dynamically by indicating its name as a string
'''
def import_from_string(module_name:str):
    return importlib.import_module


def import_from_config(section:str, key:str):
    conf = configparser.ConfigParser()
    conf.read('')


