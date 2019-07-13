'''
Helper functions to manipulate and convert JSON files into csv.
Used to ingest the data from CW.
'''

import json
import csv
from typing import List, Dict, Any 

PATH_TO_JSON_FILES='../datasets'

def json_to_csv(filename:str):
    jsonfile = {}
    with open(filename,'r') as fh:
        jsonfile = json.load(fh)
    csv_file = csv.writer(open(f"{filename.replace('.json','.csv')}", "w"))
    csv_file.writerow(jsonfile['tickets'][0].keys())
    for ticket in jsonfile['tickets']:
        csv_file.writerow(ticket.values())




'''
Takes data from the 2 big json files and ensures that each ticket in the list 
has the following data:

id
summary
board_id
board_name
company_id
company_name

type_id
type_name
subtype_id
subtype_name

priority_id
priority_name

#####customFields#######

product
product_area
urgency

##### notes #####
description
'''
def collate_json_files():
    # Get tickets list and description list from the JSON files 
    all_tickets = []
    all_desc = []
    tickets_input_file = f"{PATH_TO_JSON_FILES}/all_tickets_formatted.json"
    desc_input_file = f"{PATH_TO_JSON_FILES}/all_descriptions.json"
    with open(tickets_input_file, 'r') as fh:
        json_file = json.load(fh)
        all_tickets = json_file['tickets']
    with open(desc_input_file, 'r') as fh:
        json_file = json.load(fh)
        all_desc = json_file['descriptions']
    
    # create the list of all tickets with the required attributes
    output_tickets_list = [] # the list with the final ticket info
    for ticket in all_tickets:
        # dealing with custom fields
        ticketid = ticket.get('id',None)
        cf = ticket['customFields']
        product = get_custom_field(cf,'Product') 
        product_area = get_custom_field(cf,'Product Area') 
        urgency = get_custom_field(cf,'Urgency') 
        #sorting all_desc to make things way quicker
        all_desc = sorted(all_desc, key = lambda t: t['ticketId'])
        desc = get_ticket_description(all_desc, ticketid)
        out_t = {
                'id': ticketid,
                'summary': ticket.get('summary',None),
                'description': desc,
                'board_id': ticket.get('board',{}).get('id',None),
                'board_name': ticket.get('board',{}).get('name',None),
                'company_id': ticket.get('company',{}).get('id',None),
                'company_identifier': ticket.get('company',{}).get('identifier',None),
                'company_name': ticket.get('company',{}).get('name',None),
                'type_id': ticket.get('type',{}).get('id',None),
                'type_name': ticket.get('type',{}).get('name',None),
                'subtype_id': ticket.get('subtype',{}).get('id',None),
                'subtype_name': ticket.get('subtype',{}).get('name',None),
                'priority_id': ticket.get('priority',{}).get('id',None),
                'priority_name': ticket.get('priority',{}).get('name',None),
                'product': product,
                'product_area': product_area,
                'urgency': urgency,
                }
        output_tickets_list.append(out_t)
    return output_tickets_list



'''
Returns the value of a CW custom field associated to a specified caption
'''
def get_custom_field(cf: List[Dict[str,str]], desired_field_caption: str):
    selected_field = list(filter(lambda x: x.get('caption',None) == desired_field_caption,cf))
    return selected_field[0].get('value', None) if len(selected_field) >0 else None


'''
Returns the description of a CW ticket based on the ticketid. Takes a list of
ticket descriptions dictionaries as an argument.
This function assumes that the list is sorted.
'''
def get_ticket_description(all_desc:List[Dict[str,str]], ticketid:str):
    if not ticketid: # ticketid is null
        return 
    selected_desc = None
    for desc in all_desc: # all_desc is sorted
        if desc['ticketId'] > ticketid:
            break # to speed up things!
        if desc.get('ticketId',None) == ticketid:
            selected_desc = desc.get('text', None)
            break
    return selected_desc




'''
Unifies all the small desc json files into a unique json file containing all 
descriptions
'''
def unite_desc_json_files():
    desc_json_files=[
            "desc_1_0_2999.json",
            "desc_2_3000_5999.json",
            "desc_3_6000_6499.json",
            "desc_4_6500_6999.json",
            "desc_5_7000_7193.json"
            ]
    all_descriptions = []
    for f in desc_json_files:
        with open(f"{PATH_TO_JSON_FILES}/{f}", 'r') as jf:
            d = json.load(jf)
            all_descriptions += d['descriptions']
    return json.dumps( {'descriptions':all_descriptions} )
        
        

def main():
    #json_file=f"{PATH_TO_JSON_FILES}/desc_5_7000_7193.json"
    #json_to_csv(json_file)
    #print(unite_desc_json_files())
    print(collate_json_files()[6000])

if __name__ == '__main__':
    main()

