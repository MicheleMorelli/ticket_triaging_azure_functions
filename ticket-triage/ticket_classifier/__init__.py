import logging
import json
from typing import Dict, List, Any
import azure.functions as func
import requests
from helper import importer as di # Dependency injection via configuration

TS = di.import_ticketing_system()

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('It looks like that I received some tickets!')
    content = req.get_json()
    num = content["tickets_count"]
    assets = [x for x in content['assets']] # each x is a string
    tickets = sorted([x for x in content['assets']['Ticket']]) # each x is a string
    titles = [get_ticket_info(content, x, 'title') for x in tickets]
    updates = list(map(lambda x: update_tickets(x), tickets))

    return func.HttpResponse(
         f"\n\nI found {num} new tickets\nthe assets are {assets}"
         f"\nThe tickets are {list(zip(tickets,titles))}"
         f"\nGo check them on the browser!"
         f"\nThis was found in the config file: {TS}"
         f"\nUPDATES: {updates}",
         status_code=200
    )


'''
Returns a certain attricute related to a certain ticket
'''
def get_ticket_info(content: Dict[str,str], ticketid:str, attrib: str) -> str:
    return get_zammad_tickets(content)[ticketid][attrib] 


'''
Returns the Zammad-specific path to get to the tickets in the request message.
This is useful when the polling system is used instead of webhooks.
'''
def get_zammad_tickets(content: Dict[str,str]) -> Dict[str,str]:
    return content['assets']['Ticket']


def update_tickets(ticket):
    body = { "article": {"body": "some message of update"}}
    
    #func = getattr(TS,'put_to_ticketing_system')
    #return func('tickets/' + str(ticket), body)
    print(dir(TS))

