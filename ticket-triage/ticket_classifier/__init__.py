import logging
import json
from typing import Dict, List, Any
import azure.functions as func
import requests
from helper import importer as di # Dependency injection via configuration
from predicter import predict_ticket_labels as predict

TS = di.import_ticketing_system()

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('It looks like that I received some tickets!')
    tickets = req.get_json()
    titles = [x['summary'] for x in tickets]
    updates = list(map(lambda x: update_tickets(x), tickets))

    return func.HttpResponse(
         f"\n\nI found {len(tickets)} new tickets\nthe assets are {[x['ticket_id'] for x in tickets]}"
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

'''
Updates the ticket passed as an argument
'''
def update_tickets(ticket:str):
    fieldnames = ['board_name', "type_name", "subtype_name","product", "product_area"]
    message = ""
    prediction = predict(ticket['description'], fieldnames)
    for label in prediction:
        message += f"\n{label} => {prediction[label]}\n"
    body = {
            "state_id":8,
            "article":{
                "body":message, 
                "type":"note", 
                "internal":False
                }
            }
    put = getattr(TS,'put_to_ticketing_system')
    return put(f"tickets/{ticket['ticket_id']}", json.dumps(body))

