import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from dataset_vectoriser import import_dataset_from_csv_as_panda_dataframe as get_dataset
from dataset_vectoriser import convert_pd_series_with_NaN_to_string_list as get_as_str_list
import sys
sys.path.append('../')
from helper import importer as conf

PICKLE_PATH= conf.get_config("pickle_files","pickle_path")
PICKLE_VECTORISER=conf.get_config('pickle_files','vectoriser')
PICKLE_VECTORISED_DATASET=conf.get_config('pickle_files','vectorised_dataset')

if __name__ == '__main__':
    full_dataset = get_dataset(conf.get_config('classifier_datasets','full_dataset'))
    fieldnames = ['board_name', "type_name", "subtype_name","product", "product_area"]
    
    vect_pickle_filename = f"{PICKLE_PATH}/{PICKLE_VECTORISER}"
    vect = pickle.load(open(vect_pickle_filename, "rb"))
    features_pickle_filename = f"{PICKLE_PATH}/{PICKLE_VECTORISED_DATASET}"
    vectorised_dataset = pickle.load(open(features_pickle_filename, "rb"))
    
    for fieldname in fieldnames:
        target_class = get_as_str_list(full_dataset[fieldname])
        training_data, test_data, training_target, test_target = train_test_split(vectorised_dataset, target_class, test_size = 0.25)
        classifier = MultinomialNB().fit(training_data, training_target)
        # Vectoriser
        
        # ===============================================================
        #training accuracy tests
        #prediction = classifier.predict(test_data)
        #report = metrics.classification_report(test_target, prediction)
        #accuracy = metrics.accuracy_score(test_target, prediction)
        #print(f"TARGET LABEL {fieldname.upper()}:")
        #print(f"Accuracy: {round(accuracy*100,2)}%")
        #=================================================================

        new_ticket = ["contract expiring"]
        prediction = classifier.predict(vect.transform(new_ticket))
        print(f"TARGET LABEL {fieldname.upper()}: => {prediction[0]}")
