import nltk
import pandas as pd
import numpy as np
import sys
from  sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List
import pickle

import text_cleaner as tc

    
'''
Takes training data in form of a list of strings, and returns a new fitted TD-IDF vectoriser
'''
def get_new_fitted_vectoriser(dataset:List[str])->TfidfVectorizer:
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

def dump_fitted_vectoriser_to_pickle(field:str,series:pd.Series)->None:
    _PATH="../datasets/pickle"
    data = convert_pd_series_with_NaN_to_string_list(series)
    vect = get_new_fitted_vectoriser(data)
    pickle.dump(vect, open(f"{_PATH}/{field}_tfidf_vectoriser.pickle", 'wb'))
    print(f"Dumped fitted vectoriser to {_PATH}/{field}_tfidf_vectoriser.pickle!")


def dump_vectorised_data_to_pickle(vect:TfidfVectorizer,field:str,series:pd.Series)->None:
    _PATH="../datasets/pickle"
    data = convert_pd_series_with_NaN_to_string_list(series)
    pickle.dump(vect.transform(data), open(f"{_PATH}/{field}_vectorised_data.pickle", 'wb'))
    print(f"Dumped vectorised_data to {_PATH}/{field}_vectorised_data.pickle!")

def load_vectoriser_from_pickle(field:str)->TfidfVectorizer:
    _PATH="../datasets/pickle"
    return pickle.load( open( f"{_PATH}/{field}_tfidf_vectoriser.pickle", "rb" ) )


def load_vectorised_data_from_pickle(field:str):
    _PATH="../datasets/pickle"
    return pickle.load( open( f"{_PATH}/{field}_vectorised_data.pickle", "rb" ) )


'''
Dumps a pickled fitted vectoriser for each of the fields in the list passed as an argument
Useful when changing and testing the engineered features.
It may take quite long!
'''
def dump_all_vectorisers_to_pickle(full_dataset:pd.DataFrame, fields_list:List[str])->None:
    for field in fields_list:
        dump_fitted_vectoriser_to_pickle(f"{field}", full_dataset[field])


'''
Dumps a a vectorised dataset to pickle for each of the fields in the list passed as an argument
Useful when changing and testing the engineered features.
It may definitely take quite long!
'''
def dump_all_vectorised_data_to_pickle(vect:TfidfVectorizer,full_dataset:pd.DataFrame, fields_list:List[str])->None:
    for field in fields_list:
        dump_vectorised_data_to_pickle(vect, f"{field}", full_dataset[field])


if __name__ == '__main__':
    pd.set_option('display.max_colwidth',50)
    full_dataset = import_dataset_from_csv_as_panda_dataframe('14-07CLEANED_dataset.csv')
    field_list = ['summary','description']
    #dump_all_vectorisers_to_pickle(full_dataset, field_list)
    vect = load_vectoriser_from_pickle("description")
    dump_all_vectorised_data_to_pickle(vect, full_dataset, field_list)
    #vectorised_data = load_vectorised_data_from_pickle('summary')
    #print(vectorised_data.shape)


