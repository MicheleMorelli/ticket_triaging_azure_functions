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

def dump_fitted_vectoriser_to_pickle(pickle_filename:str,series:pd.Series)->None:
    _PATH="../datasets/pickle"
    data = convert_pd_series_with_NaN_to_string_list(series)
    vect = get_new_fitted_vectoriser(data)
    pickle.dump(vect, open(f"{_PATH}/{pickle_filename}", 'wb'))
    print(f"Dumped fitted vectoriser to {_PATH}/{pickle_filename}!")


def load_vectoriser_from_pickle(field:str)->TfidfVectorizer:
    _PATH="../datasets/pickle"
    return pickle.load( open( f"{_PATH}/{field}_tfidf_vectoriser.pickle", "rb" ) )

'''
Dumps a pickled fitted vectoriser for each of the fields in the list passed as an argument
Useful when changing and testing the engineered features.
It may take quite long!
'''
def dump_all_vectorisers_to_pickle(full_dataset:pd.DataFrame, fields_list:List[str])->None:
    for field in fields_list:
        dump_fitted_vectoriser_to_pickle(f"{field}_tfidf_vectoriser.pickle", full_dataset[field])


if __name__ == '__main__':
    pd.set_option('display.max_colwidth',50)
    full_dataset = import_dataset_from_csv_as_panda_dataframe('14-07CLEANED_dataset.csv')
    #dump_all_vectorisers_to_pickle(full_dataset, ['summary', 'description'])
    vect = load_vectoriser_from_pickle("description")
    vectorised_data = vect.transform(full_dataset['summary'][0:50])
    print(vectorised_data.shape)


