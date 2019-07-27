import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from dataset_vectoriser import import_dataset_from_csv_as_panda_dataframe as get_dataset
from dataset_vectoriser import convert_pd_series_with_NaN_to_string_list as get_as_str_list

PICKLE_PATH="../datasets/pickle"

if __name__ == '__main__':
    full_dataset = get_dataset('14-07CLEANED_dataset.csv')
    fieldname = 'board_name'
    target_class = get_as_str_list(full_dataset[fieldname])
    features_pickle_filename = f"{PICKLE_PATH}/description_vectorised_data_20190727_1507.pickle"
    vectorised_dataset = pickle.load(open(features_pickle_filename, "rb"))
    training_data, test_data, training_target, test_target = train_test_split(vectorised_dataset, target_class, test_size = 0.25, random_state = 23)
    classifier = MultinomialNB().fit(training_data, training_target)
    predicter = classifier.predict(test_data)
    report = metrics.classification_report(test_target, predicter)
    print(report)

