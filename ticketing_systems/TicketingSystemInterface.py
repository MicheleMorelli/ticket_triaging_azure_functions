"""
The abstract Ticketing System Interface (TSI), which indicates all the 
functions that must be implemented by its concrete implementations.
The compulsory methods must be implemented in the concrete implementation's 
connector.py package.  
"""


import requests

Response = requests.models.Response

def put_to_ticketing_system(ticket: str) -> Response:
    """
    The function that sends a PUT request to the ticketing 
    system in order to update an existing ticket.
    """
    pass


def get_updated_ticket_payload(message: str) -> str:
    """
    Returns the actual ticketing system-dependent 
    payload to be passed with the PUT request.
    """
    pass


def get_from_ticketing_system(uri: str) -> Response:
    """
    {Optional}
    This function is only needed in case that the 
    ticketing system is not provided with webhooks. 
    It used to fetch the newly raised tickets 
    from the tikceting system.
    """
    pass
