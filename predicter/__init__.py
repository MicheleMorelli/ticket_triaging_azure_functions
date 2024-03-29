from typing import List,Dict
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics
import pickle
import sys
sys.path.append('./')
from vectoriser import import_dataset_from_csv_as_panda_dataframe as get_dataset
from vectoriser import convert_pd_series_with_NaN_to_string_list as get_as_str_list
import time
import os
import configuration as conf

PICKLE_PATH= conf.get_config("pickle_files","pickle_path")
PICKLE_CLASSIFIER_PATH = f"{PICKLE_PATH}/classifiers"


def get_vectoriser():
    """
    Retrieves the pickled vectoriser which (indicated in the config file.)
    """
    PICKLE_VECTORISER=conf.get_config('pickle_files','vectoriser')
    VECT_FILENAME = f"{PICKLE_PATH}/{PICKLE_VECTORISER}"
    return pickle.load(open(VECT_FILENAME, "rb"))


def get_vectorised_dataset():
    """
    Retrieves the pickled vectorised dataset which 
    (indicated in the config file.)
    """
    PICKLE_VECTORISED_DATASET=conf.get_config('pickle_files','vectorised_dataset')
    FEATURES_FILENAME = f"{PICKLE_PATH}/{PICKLE_VECTORISED_DATASET}"
    return pickle.load(open(FEATURES_FILENAME, "rb"))


def get_classifier(field: str) -> MultinomialNB:
    """
    Retrieves the pickled classifier that is indicated in the config
    """
    classifier_dir = conf.get_config('pickle_files','current_classifier')
    classifier_name = f"{PICKLE_CLASSIFIER_PATH}/{classifier_dir}/{field}_classifier.pickle"
    return pickle.load(open(classifier_name, "rb"))


def create_and_test_model(full_dataset, fieldnames: List[str]) -> None:
    """
    Provided with a dataset, this function splits the dataset
    (75% training, 25% testing), trains the classifier, tests
    its accuracy and stores the classifier as a .pickle file.
    """
    vect = get_vectoriser()
    vectorised_dataset = get_vectorised_dataset()
    # create directory for pickled classifiers
    CLASSIFIER_DIRNAME = f"{PICKLE_CLASSIFIER_PATH}/{time.strftime('%Y%m%d%H%M')}"
    if not os.path.exists(CLASSIFIER_DIRNAME):
            os.makedirs(CLASSIFIER_DIRNAME)
    for fieldname in fieldnames:
        target_class = get_as_str_list(full_dataset[fieldname])
        training_data, test_data, training_target, test_target = train_test_split(vectorised_dataset, target_class, test_size = 0.25)
        classifier = MultinomialNB().fit(training_data, training_target)
        #dump this classifier in the pickle dir
        pickle.dump(classifier, open(f"{CLASSIFIER_DIRNAME}/{fieldname}_classifier.pickle",'wb'))
        # ===============================================================
        #training accuracy tests
        prediction = classifier.predict(test_data)
        #report = metrics.classification_report(test_target, prediction)
        accuracy = metrics.accuracy_score(test_target, prediction)
        kfold_F1_score = metrics.f1_score(test_target, prediction, average='weighted')
        print(f"TARGET LABEL {fieldname.upper()}:")
        print(f"Accuracy: {round(accuracy*100,2)}%")
        print(f"f1-score (K fold): {round(kfold_F1_score*100,2)}%")
        #=================================================================


def test_existing_classifier(full_dataset, fieldnames: List[str]) -> None:
    """
    Prints the scores of both K-fold cross-validation and k-splits validation
    """
    import warnings
    warnings.filterwarnings('ignore') 
    vectorised_dataset = get_vectorised_dataset()
    print("K-Folds VALIDATION METRICS:")
    for fieldname in fieldnames:
        target_class = get_as_str_list(full_dataset[fieldname])
        accuracy = cross_val_score(get_classifier(fieldname), vectorised_dataset, target_class, cv=5)
        f1_score = cross_val_score(get_classifier(fieldname), vectorised_dataset, target_class, cv=5, scoring="f1_weighted")
        print(f"TARGET LABEL {fieldname.upper()}:")
        print(f"Accuracy: {round(accuracy.mean() *100,2)}%")
        print(f"F1-score: {round(f1_score.mean() *100,2)}%")
    
    print("\n\n"+ ("=" * 20) + "\n\n:")
    print("Train-test METRICS:")
    for fieldname in fieldnames:
        target_class = get_as_str_list(full_dataset[fieldname])
        classifier = get_classifier(fieldname)
        training_data, test_data, training_target, test_target = train_test_split(vectorised_dataset, target_class, test_size = 0.4)
        prediction = classifier.predict(test_data)
        accuracy = metrics.accuracy_score(test_target, prediction)
        f1_score = metrics.f1_score(test_target, prediction, average='weighted')
        print(f"TARGET LABEL {fieldname.upper()}:")
        print(f"Accuracy: {round(accuracy.mean() *100,2)}%")
        print(f"F1_score: {round(f1_score.mean() *100,2)}%")
    warnings.filterwarnings('always') 


def predict_ticket_labels(description: str, target_fields: List[str]) -> Dict[str,str]:
    """
    This function takes the classifier indicated in the conf.ini
    file, and produces a prediction over a given target set of fields.
    """
    labels = {}
    vect = get_vectoriser()
    for field in target_fields:
        #get the specific current classifier
        classifier = get_classifier(field)
        if classifier:
            prediction = classifier.predict(vect.transform([description]))
            labels[field] = prediction[0]
    return labels


if __name__ == '__main__':
    full_dataset = get_dataset(conf.get_config('classifier_datasets','full_dataset'))
    fieldnames = conf.import_config_list(
            "azure_classifier",
            "target_fieldnames",
            ",")
    test_ticket = '''
    Hi, 
    our Eprints repository does not work anymore.
    Thank you,
    Michele
    '''
    
    # Uncomment the next line to train and test the model
    #create_and_test_model(full_dataset,fieldnames)
    
    #uncomment the next line to test the new ticket prediction
    #print(predict_ticket_labels(test_ticket,fieldnames))

    # Uncomment the next line to test the model (using an unseen dataset passed 
    #via config)
    test_existing_classifier(full_dataset,fieldnames)
