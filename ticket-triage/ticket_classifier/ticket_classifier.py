import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
from dataset_vectoriser import import_dataset_from_csv_as_panda_dataframe as get_dataset

PICKLE_PATH="../datasets/csv"

if __name__ == '__main__':
    full_dataset = get_dataset('14-07CLEANED_dataset.csv')


