import nltk
import pandas as pd
import numpy as np
import sys
from  sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List

import text_cleaner as tc

    
'''
Gets a training as a list of strings, and returns a fitted TD-IDF vectoriser
'''
def get_fitted_vectoriser(dataset:List[str])->TfidfVectorizer:
    vect = TfidfVectorizer(analyzer=tc.functional_cleaner)
    vect.fit(dataset)
    return vect

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
    full_dataset = import_dataset_from_csv_as_panda_dataframe('14-07CLEANED_dataset.csv')
    vect = get_fitted_vectoriser(convert_pd_series_with_NaN_to_string_list(full_dataset['summary']))
    vectorised_data = vect.transform(full_dataset['summary'])

