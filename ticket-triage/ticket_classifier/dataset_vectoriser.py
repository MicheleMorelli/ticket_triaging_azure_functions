'''
The purpose of this module is to create the pickle files that contain the 
fitted vectoriser and the vectorised features. This is done to dramatically reduce
the processing times, especially when testing the classifier.
'''

import nltk
import pandas as pd
import numpy as np
import sys
from  sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List
import pickle
import time

import text_cleaner as tc
import sys
sys.path.append('../')
from helper import importer as conf

PICKLE_PATH= conf.get_config("pickle_files","pickle_path")

'''
Takes training data in form of a list of strings, and returns a new fitted TD-IDF vectoriser
'''
def get_new_fitted_vectoriser(dataset:List[str])->TfidfVectorizer:
    vect = TfidfVectorizer(analyzer=tc.functional_cleaner)
    vect.fit(dataset)
    return vect



'''
Takes a Pandas Series, and returns a list of strings. This was to solve the 
issues with the vectoriser, which does not like Pandas's NaN elements (which are of type float)
'''
def convert_pd_series_with_NaN_to_string_list(series:pd.Series)->List[str]:
    return ["" if type(x) == float else x for x in series]



def import_dataset_from_csv_as_panda_dataframe(filename:str)->pd.DataFrame:
    _PATH= conf.get_config("classifier_datasets","csv_path")
    FILENAME=filename
    return pd.read_csv(f"{_PATH}/{FILENAME}")


'''
Dumps a fitted vectoriser to a pickle file. It returns the name of the pickle file
'''
def dump_fitted_vectoriser_to_pickle(field:str,series:pd.Series)->str:
    data = convert_pd_series_with_NaN_to_string_list(series)
    vect = get_new_fitted_vectoriser(data)
    pickle_filename = f"{PICKLE_PATH}/{field}_tfidf_vectoriser_{time.strftime('%Y%m%d_%H%M')}.pickle"
    pickle.dump(vect, open(pickle_filename, 'wb'))
    print(f"Dumped fitted vectoriser to {pickle_filename}")
    return pickle_filename



'''
Dumps a vectorised features to a pickle file. It returns the name of the pickle file
'''
def dump_vectorised_data_to_pickle(vect:TfidfVectorizer,field:str,series:pd.Series)->str:
    data = convert_pd_series_with_NaN_to_string_list(series)
    pickle_filename = f"{PICKLE_PATH}/{field}_vectorised_data_{time.strftime('%Y%m%d_%H%M')}.pickle"
    pickle.dump(vect.transform(data), open(pickle_filename, 'wb'))
    print(f"Dumped vectorised_data to {pickle_filename}")
    return pickle_filename



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



'''
Dumps all vectorised features for both 'descriptions' and 'summaries'
'''
if __name__ == '__main__':
    start_time = time.time()
    
    full_dataset = import_dataset_from_csv_as_panda_dataframe(conf.get_config("classifier_datasets","full_dataset")
)
    # change the vect_field to fit the vectoriser on another column of the dataset
    vect_field = 'description' # ie: the column use to fit the vectoriser
    vect_pickle_filename = dump_fitted_vectoriser_to_pickle(vect_field,full_dataset[vect_field])
    vect = pickle.load(open(vect_pickle_filename, "rb")) # the TfIdf vectoriser
    field_list = ['description']
    dump_all_vectorised_data_to_pickle(vect, full_dataset, field_list)
    
    print("All vectorised data was dumped to pickle files!")
    processing_time= time.time() - start_time
    print(f"PROCESSING TIME: {processing_time} seconds (approximately {processing_time // 60} minutes)")
