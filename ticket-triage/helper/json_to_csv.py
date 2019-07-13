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
Takes data from the 2 big json files and ensures that each ticket has the following data:

id
summary
board
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
    print(f"tickets: {len(all_tickets)}")
    print(f"DEscritpions: {len(all_desc)}")


    

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
    collate_json_files()

if __name__ == '__main__':
    main()

