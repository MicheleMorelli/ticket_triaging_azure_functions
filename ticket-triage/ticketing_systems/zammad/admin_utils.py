import importlib
from typing import List, Dict, Any, Tuple
import os
import json
import requests
from connector import *

# TODO: import dataset path via conf.ini
#DATASET_PATH="../../zammad_admin/test_datasets/"


def main()->None:
    filename:str = f"{DATASET_PATH}/users.csv"
    #print(json.loads(ctj.convert_csv_into_json(filename))) 
    #create_organizations_from_csv(filename)
    #create_users_from_csv(filename)

'''
Generic method to create entitities on the ticketing system
'''
def create_entities_from_csv(csv_filename: str, endpoint: str) -> List[requests.models.Response]:
    ctj = importlib.import_module("../../helper", package='csv_to_json')
    all_rows:Dict = json.loads(ctj.convert_csv_into_json(csv_filename)) 
    resp_list = []
    print("Adding entities to Zammad:")
    for row in all_rows["elements"]:
        req = post_to_ticketing_system(endpoint,json.dumps(row))
        resp_list.append(req)
        print(f"{req}\n{row}")
    return resp_list

'''
Create companies on the ticketing system for testing
'''
def create_organizations_from_csv(csv_filename: str) -> List[requests.models.Response]:
    return create_entities_from_csv(csv_filename, "organizations")


'''
Create users on the ticketing system for testing
'''
def create_users_from_csv(csv_filename: str) -> List[requests.models.Response]:
    return create_entities_from_csv(csv_filename, "users")

if (__name__ == '__main__'):
    main()
