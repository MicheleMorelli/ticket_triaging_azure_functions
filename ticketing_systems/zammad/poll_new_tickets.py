'''
This small script implements a polling process that checks whether new tickets have been 
raised on the ticketing system, and sends them to the classifier on Azure

to run it every 15 seconds with the watch command:
watch -n 15 -d python3 poll_new_tickets.py
'''

from typing import *
import os
import json
import requests
import time
import connector as zamreq

def get_new_tickets_from_ticketing_system_as_json() -> str:
    '''
    Returns all the tickets in the ticketing system that are marked as 'new'
    '''
    return json.dumps(
            zamreq.get_from_ticketing_system("tickets/search?query=state%3Anew").json())
 

def assemble_relevant_ticket_list(tickets: str) -> List[Dict[str,Any]]:
    '''
    Takes the json file about the open tickets, and returns a list of dictionaries
    that contain the relevant information about the open tickets:
    -initial description,
    -id, 
    -summary
    '''
    tickets = json.loads(tickets)
    ticket_list = []
    for ticket in tickets['tickets']:
        ticket = str(ticket)
        summary = tickets['assets']['Ticket'][ticket]['title']
        all_ticket_notes = zamreq.get_from_ticketing_system(f"ticket_articles/by_ticket/{ticket}")
        description = json.loads(all_ticket_notes.text)[0]['body']
        ticket_relevant_info = {
                'ticket_id':ticket,
                'summary': summary,
                'description': description 
                }
        ticket_list.append(ticket_relevant_info)
    return ticket_list


def post_to_azure(payload: str) -> requests.models.Response:
    '''
    Makes a POST request to the azure function
    '''
    content_type = 'application/json'
    uri = get_azure_uri()
    print(payload)
    params = {'Content-Type': content_type}
    req = requests.post(uri, headers=params, data=payload )
    return req


def get_azure_uri() -> str:
    '''
    Returns the Azure URI
    '''
    return os.getenv('AZURE_CLASSIFIER_URI')


def main() -> None:
    '''
    Fetches all the newly created tickets from the ticketing system, 
    and sends them to Azure for processing.
    '''
    starttime = time.time()
    tickets = get_new_tickets_from_ticketing_system_as_json()
    retrieved_tickets = assemble_relevant_ticket_list(tickets)
    if not retrieved_tickets:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\tNo new tickets found")
        return
    payload = json.dumps(retrieved_tickets)
    resp = post_to_azure(payload)
    print(resp)
    print(resp.text)
    print(f"Execution time (seconds): {time.time() - starttime}")


if (__name__ == "__main__"):
    main()
