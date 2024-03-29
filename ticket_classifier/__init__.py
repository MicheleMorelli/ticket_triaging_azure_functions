"""
This is the main script that composes the Azure Functions application.
"""

import logging
import json
from typing import Dict, List, Any, Union
import azure.functions as func
import requests
import configuration as di # Dependency injection via configuration
from predicter import predict_ticket_labels as predict

TS = di.import_ticketing_system()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('It looks like that I received some tickets!')
    tickets = req.get_json()
    titles = [x['summary'] for x in tickets]
    updates = list(map(lambda x: update_tickets(x), tickets))
    return func.HttpResponse(
         f"\n\nI found {len(tickets)} new tickets\nthe assets" 
         f" are {[x['ticket_id'] for x in tickets]}"
         f"\nUPDATES: {updates}",
         status_code=200
    )


def update_tickets(ticket: str) -> str:
    """
    Updates the ticket that was passed as an argument
    """
    fieldnames = di.import_config_list(
            "azure_classifier", 
            "target_fieldnames",
            ",")
    
    message = ""
    # !! FOR TESTING
    import datetime
    message += f"{datetime.datetime.now()}\nTEST- Original Message:\n{ticket['description']}\n\n"
    # !! END OF TESTING
    prediction = predict(
            ticket[di.get_config("azure_classifier", "field_for_prediction")], 
            fieldnames)
    for label in prediction:
        message += f"\n{label} => {prediction[label]}\n"
    body = TS.get_updated_ticket_payload(message) 
    put = getattr(TS,'put_to_ticketing_system')
    return put(f"tickets/{ticket['ticket_id']}", json.dumps(body))

