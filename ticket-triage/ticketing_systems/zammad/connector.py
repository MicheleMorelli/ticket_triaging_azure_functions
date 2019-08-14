from typing import List, Dict, Any, Tuple
import os
import json
import requests

'''
Get the values at a specified endpoint using the GET method
'''
def get_from_ticketing_system(endpoint: str) -> str:
    (usr,key,uri) = get_ticketing_system_usr_key_uri(endpoint)
    req = requests.get(uri, auth=(usr, key))
    return req

'''
used to create new entities on the ticketing system
'''
def post_to_ticketing_system(endpoint:str, payload:str) -> requests.models.Response:
    content_type = 'application/json'
    (usr,key,uri) = get_ticketing_system_usr_key_uri(endpoint)
    params = {'Content-Type': content_type}
    req = requests.post(uri, headers=params, auth=(usr, key), data=payload )
    return req


'''
used to update an entity on the ticketing system
'''
def put_to_ticketing_system(endpoint:str, payload:str) -> requests.models.Response:
    content_type = 'application/json'
    (usr,key,uri) = get_ticketing_system_usr_key_uri(endpoint)
    print(f"REQ URI IS {uri}")
    params = {'Content-Type': content_type}
    req = requests.put(uri, headers=params, auth=(usr, key), data=payload )
    return req


def get_updated_ticket_payload(message: str) -> Dict[str, Any]:
    """
    Returns the ticketing system-specific payload to upload the ticket
    """
    return {
            "state_id":8, # State 8 is the custom 'triaged' state on Zammad
            "article":{
                "body":message,
                "type":"note",
                "internal":False
                }
            }


def get_ticketing_system_usr_key_uri(endpoint:str) -> Tuple[str]:
    usr = get_ticketing_system_username()
    key = get_ticketing_system_key()
    uri = f"{get_ticketing_system_uri()}/{endpoint}"
    return (usr,key,uri)


def get_ticketing_system_username():
    return os.getenv('ZAMMAD_USERNAME')


def get_ticketing_system_key():
    return os.getenv('ZAMMAD_KEY')


def get_ticketing_system_uri():
    return os.getenv('ZAMMAD_URI')


def main()->None:
    print(globals())


if (__name__ == '__main__'):
    main()
