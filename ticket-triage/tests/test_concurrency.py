"""
Testing concurrency non-functional requirement
"""

from threading import Thread
import os
import sys
import requests
sys.path.append('../')


def make_req() -> requests.models.Response:
    payload = '[{"ticket_id":30,"summary": "summary","description": "description"}]'
    return post_to_azure(payload).status_code

def test_concurrent() -> None:
    calls_num = 100
    for i in range(0,calls_num):
        t = Thread(target=make_req)
        t.start()


def post_to_azure(payload: str) -> requests.models.Response:
    """
    Makes a POST request to the azure function
    """
    content_type = 'application/json'
    uri = get_azure_uri()
    print(payload)
    params = {'Content-Type': content_type}
    req = requests.post(uri, headers=params, data=payload )
    return req


def get_azure_uri() -> str:
    """
    Returns the Azure URI
    """
    return os.getenv('AZURE_CLASSIFIER_URI')


if __name__ == '__main__':
    test_concurrent()
