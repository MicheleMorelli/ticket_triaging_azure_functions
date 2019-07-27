import nltk
import pandas as pd
import numpy as np
import sys
from  sklearn.feature_extraction.text import TfidfVectorizer

import text_cleaner as tc

def vectorise_dataset():
    pass



def import_dataset_from_csv_as_panda_dataframe(filename:str)->pd.DataFrame:
    _PATH="../datasets/csv"
    FILENAME=filename
    return pd.read_csv("{}/{}".format(_PATH,FILENAME))


if __name__ == '__main__':
    pd.set_option('display.max_colwidth',150)
    dataset = import_dataset_from_csv_as_panda_dataframe('14-07CLEANED_dataset.csv')
    print(dataset.count())



