import logging
import json
from typing import Dict, List, Any
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('It looks like that I received some tickets!')
    content = req.get_json()
    num = content["tickets_count"]
    assets = [x for x in content['assets']] # each x is a string
    tickets = [x for x in content['assets']['Ticket']] # each x is a string
    #titles = [assets['Ticket'][int(x)]['title'] for x in tickets]
    for i in tickets:
        print(get_ticket_info(content, i, 'title'))

    return func.HttpResponse(
         f"\n\nI found {num} new tickets\nthe assets are {assets}"
         f"\nThe tickets are {tickets}",
         #f"\nThe titles are {titles}",
         #f"\nOne ticket example is {content['assets']['Ticket']['8']['title']}",
         status_code=200
    )


'''
Returns a certain attricute related to a certain ticket
'''

def get_ticket_info(content: Dict[str,str], ticketid:str, attrib: str) -> str:
    return content['assets']['Ticket'][ticketid][attrib] 
