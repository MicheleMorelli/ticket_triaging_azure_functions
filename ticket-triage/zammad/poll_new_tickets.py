from typing import List, Dict, Any, Tuple
import csv_to_json as ctj
import http_req_to_zammad as zamreq
import os
import json
import requests


def get_new_tickets_from_zammad_as_json() -> str:
    return json.dumps(zamreq.get_from_zammad("tickets/search?query=state%3Anew"))
    

def post_to_azure(payload:str) -> requests.models.Response:
    content_type = 'application/json'
    uri = get_azure_uri()
    print(payload)
    params = {'Content-Type': content_type}
    req = requests.post(uri, headers=params, data=payload )
    return req


def get_azure_uri():
    return os.getenv('AZURE_CLASSIFIER_URI')


def main():
    payload = get_new_tickets_from_zammad_as_json()
    resp = post_to_azure(payload)
    print(resp)
    print(resp.text)


if (__name__ == "__main__"):
    main()
