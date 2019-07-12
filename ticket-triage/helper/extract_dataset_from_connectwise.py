import json
import requests
from typing import List, Any, Dict
import os

'''
Utility functions to extract the tickets dataset from CoSector's Connectwise
'''


'''
Returns all the 7194 tickets that are currently on Cosector's CW
'''
def get_all_tickets()->List[Any]:
    all_tickets_list = []
    for page_number in range(0,8): # currently there are 7194 tickets in the system
        fields ='id,summary,board,company,type,subtype,priority,customFields' 
        uri = f"{get_connectwise_URI()}/service/tickets/?page={page_number}&pagesize=1000&fields={fields}"
        all_tickets_list += get_request(uri)
    return all_tickets_list


'''
Returns all the ticket IDs from a JSON file as a list
'''
def get_all_tickets_ids()-> List[int]:
    all_tickets = get_all_tickets()
    return [x['id'] for x in all_tickets]


'''
Makes a get_request to CW.
'''
def get_request(uri:str)->Dict:
    hdrs = {'content-type': _'application/json', 'accept': _'application/json'} 
    this_req = requests.get( 
            uri, 
            headers=hdrs, 
            auth=(get_connectwise_user(), get_connectwise_key()))
    return this_req.json()


'''
prints all the tickets as a JSON string
'''
def print_all_tickets_as_JSON():
    all_tickets = get_all_tickets()
    tickets_dict = {'tickets':all_tickets}
    json_string = json.dumps(tickets_dict)
    print(json_string)


'''
prints all the descriptions as a JSON string
'''
def print_all_descriptions_as_JSON():
    all_desc = get_all_ticket_descriptions()
    desc_dict = {'descriptions':all_desc}
    json_string = json.dumps(desc_dict)
    print(json_string)


'''
Takes a JSON file name and returns all the ticket IDs in it
'''
def get_all_ticket_ids_from_json_file(filename):
    id_list = []
    with open(filename,'r') as json_file:
        json_dict = json.load(json_file)
        id_list = [x['id'] for x in json_dict['tickets']]
    return id_list

'''
Makes an GET request for every ticket in the JSON file and gets the ticket's 
descriptionm and returns them as a list.
'''
def get_all_ticket_descriptions():
    all_descriptions_list = []
    all_ids = get_all_ticket_ids_from_json_file('all_tickets.json')
    start = 0
    limit = start + 3000 # 3000 tickets per go
    for n in range(start,limit):
        fields ='ticketId,text' 
        uri = f"{get_connectwise_URI()}/service/tickets/{all_ids[n]}/notes?pageSize=1&fields={fields}"
        all_descriptions_list += get_request(uri)
    return all_descriptions_list

'''
Get CW key
'''
def get_connectwise_key():
    return os.getenv('CW_KEY')


'''
Get CW username
'''
def get_connectwise_user():
    return os.getenv('CW_USER')


'''
Get CW URI
'''
def get_connectwise_URI():
    return os.getenv('CW_URI')



def main():
    #print_all_descriptions_as_JSON() # CAREFUL! This one takes ages


if __name__ == '__main__':
    main()
