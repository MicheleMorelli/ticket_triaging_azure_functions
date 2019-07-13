'''
Helper functions to convert JSON files into csv.
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
    # headers
    #id,summary,board,company,type,subtype,priority,customFields
    #headers = ['id','summary','board', 'company','type','subtype','priority']
    #print(jsonfile['descriptions'][0].keys())
    csv_file.writerow(jsonfile['descriptions'][0].keys())
    for ticket in jsonfile['descriptions']:
        csv_file.writerow(ticket.values())

    


def main():
    json_file=f"{PATH_TO_JSON_FILES}/desc_5_7000_7193.json"
    json_to_csv(json_file)

if __name__ == '__main__':
    main()

