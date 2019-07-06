from typing import List, Dict, Any, Tuple
import csv_to_json as ctj
import os
import json
import requests

DATASET_PATH="../../zammad_admin/test_datasets/"

def main()->None:
    filename:str = f"{DATASET_PATH}/users.csv"
    #print(json.loads(ctj.convert_csv_into_json(filename))) 
    #create_organizations_from_csv(filename)
    create_users_from_csv(filename)
    #print(get_from_zammad("users"))


def get_from_zammad(endpoint: str) -> str:
    (usr,key,uri) = get_zammad_usr_key_uri(endpoint)
    req = requests.get(uri, auth=(usr, key))
    return req.json()

'''
used to create a ticket on Zammad
'''
def post_to_zammad(endpoint:str, payload:str) -> requests.models.Response:
    content_type = 'application/json'
    (usr,key,uri) = get_zammad_usr_key_uri(endpoint)
    params = {'Content-Type': content_type}
    req = requests.post(uri, headers=params, auth=(usr, key), data=payload )
    return req


'''
used to update a ticket on Zammad
'''
def put_to_zammad(endpoint:str, payload:str) -> requests.models.Response:
    content_type = 'application/json'
    (usr,key,uri) = get_zammad_usr_key_uri(endpoint)
    params = {'Content-Type': content_type}
    req = requests.put(uri, headers=params, auth=(usr, key), data=payload )
    return req


def create_zammad_entities_from_csv(csv_filename: str, endpoint: str) -> List[requests.models.Response]:
    all_rows:Dict = json.loads(ctj.convert_csv_into_json(csv_filename)) 
    resp_list = []
    print("Adding entities to Zammad:")
    for row in all_rows["elements"]:
        req = post_to_zammad(endpoint,json.dumps(row))
        resp_list.append(req)
        print(f"{req}\n{row}")
    return resp_list


def create_organizations_from_csv(csv_filename: str) -> List[requests.models.Response]:
    return create_zammad_entities_from_csv(csv_filename, "organizations")


def create_users_from_csv(csv_filename: str) -> List[requests.models.Response]:
    return create_zammad_entities_from_csv(csv_filename, "users")

def get_zammad_usr_key_uri(endpoint:str) -> Tuple[str]:
    usr = get_zammad_username()
    key = get_zammad_key()
    uri = f"{get_zammad_uri()}/{endpoint}"
    return (usr,key,uri)


def get_zammad_username():
    return os.getenv('ZAMMAD_USERNAME')


def get_zammad_key():
    return os.getenv('ZAMMAD_KEY')


def get_zammad_uri():
    return os.getenv('ZAMMAD_URI')


if (__name__ == '__main__'):
    main()
