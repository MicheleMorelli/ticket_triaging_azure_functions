import nltk
import pandas as pd
import numpy as np
import sys
from  sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List

import text_cleaner as tc

def get_vectoriser_and_vectorised_training_dataset(dataset:pd.DataFrame,fieldname:str):
    # the following list comprehension is to deal with the Pandas' NaN values
    all_rows = ["" if type(x) == float else x for x in dataset[fieldname]]
    vect = TfidfVectorizer(analyzer=tc.functional_cleaner)
    vectorised_dataset = vect.fit_transform(all_rows)
    return vect, vectorised_dataset 
    
def get_fit_vectoriser(dataset:pd.DataFrame)->List[str]:
    all_rows = ["" if type(x) == float else x for x in dataset[fieldname]]

'''
Takes a Pandas Series, and returns a list of strings. This was to solve the 
issues with the vectoriser with pd's NaN elements (which are of type float)
'''
def convert_pd_series_with_NaN_to_string_list(series:pd.Series)->List[str]:
    return ["" if type(x) == float else x for x in series]

def import_dataset_from_csv_as_panda_dataframe(filename:str)->pd.DataFrame:
    _PATH="../datasets/csv"
    FILENAME=filename
    return pd.read_csv(f"{_PATH}/{FILENAME}")


if __name__ == '__main__':
    pd.set_option('display.max_colwidth',50)
    dataset = import_dataset_from_csv_as_panda_dataframe('14-07CLEANED_dataset.csv')
    vect, vectorised_dataset = get_vectoriser_and_vectorised_training_dataset(dataset, 'summary')
    print(vectorised_dataset)
