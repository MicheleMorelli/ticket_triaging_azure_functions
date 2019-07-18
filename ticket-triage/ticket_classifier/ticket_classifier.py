from nltk import word_tokenize
import pandas as pd
import numpy as np

_PATH="../datasets/csv"

def main():
    #FILENAME='14-07CLEANED_dataset.csv'
    #dataset = pd.read_csv(f"{_PATH}/{FILENAME}") 
    #print(dataset.head())
    text="""Hello Mr. Smith, how are you doing today? The weather is great, and city is awesome.
    The sky is pinkish-blue. You shouldn't eat cardboard"""
    tokenized_text=word_tokenize(text)
    print(tokenized_text)


if __name__ == '__main__':
    main()
