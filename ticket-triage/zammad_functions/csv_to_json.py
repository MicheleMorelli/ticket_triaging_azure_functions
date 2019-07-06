'''
Helper functions to convert CSV into json
'''

import json
import csv
from typing import List, Dict, Any 

def import_csv_as_dict(filename:str) -> Dict[str,str]:
    csv_dict: Dict[str,List[str]] = {"elements":[]}
    with open(filename, 'r') as fh:
        labels:List[str] = get_csv_headers(filename)
        for row in csv.DictReader(fh):
            d:Dict[str,str] = {}
            d = {label:row[label] for label in labels}
            csv_dict["elements"].append(d)
    return csv_dict


def convert_csv_into_json(filename:str)->str:
    return json.dumps(import_csv_as_dict(filename))


def get_csv_headers(filename:str)->List[str]:
    headers = []
    with open(filename, 'r') as fh:
        headers = csv.reader(fh).__next__()
    return headers
