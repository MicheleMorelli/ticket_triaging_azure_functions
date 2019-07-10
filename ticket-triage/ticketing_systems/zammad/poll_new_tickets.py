from typing import List, Dict, Any, Tuple
import connector as zamreq
import os
import json
import requests

'''
Returns all the tickets in the ticketing system that are marked as 'new'
'''
def get_new_tickets_from_ticketing_system_as_json() -> str:
    return json.dumps(zamreq.get_from_ticketing_system("tickets/search?query=state%3Anew").json())
    
'''
Makes a POST request to the azure function
'''
def post_to_azure(payload:str) -> requests.models.Response:
    content_type = 'application/json'
    uri = get_azure_uri()
    print(payload)
    params = {'Content-Type': content_type}
    req = requests.post(uri, headers=params, data=payload )
    return req

'''
Returns the Azure URI
'''
def get_azure_uri()->str:
    return os.getenv('AZURE_CLASSIFIER_URI')

'''
Sends all the new tickets to Azure for processing.
'''
def main()->None:
    payload = get_new_tickets_from_ticketing_system_as_json()
    resp = post_to_azure(payload)
    print(resp)
    print(resp.text)


if (__name__ == "__main__"):
    main()
