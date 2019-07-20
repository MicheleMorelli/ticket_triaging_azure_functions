import nltk
import re
import string
from typing import List, Dict
from toolz import pipe

def clean_ticket_description(ticket_description:str):
    #to lower case
    ticket_description = ticket_description.lower()
    # separate based on white spaces
    all_words = re.split("\s+",ticket_description)
    #remove empty strings
    all_words = list(filter(lambda x: x != '', all_words))
    #remove numbers
    all_words = list(filter(lambda x: not is_number(x), all_words))
    #remove email addresses
    all_words = list(filter(lambda x: not is_potential_email_address(x), all_words))
    #remove  irrelevant URLs
    all_words = list(filter(lambda x: not is_a_URL(x), all_words))
    # remove stopwords
    all_words = remove_stopwords(all_words)
    # remove names
    all_words = remove_names(all_words)

    # find related urls and replace
    
    # lemmatize
    lem = nltk.WordNetLemmatizer()
    all_words = [lem.lemmatize(x, wordnet_pos_mapper(x)) for x in all_words]
    tokens = all_words
    return tokens


'''
Higher order function to be used in the sanitizer's pipeline. It takes a predicate
and a string list, and removes all the elements of the list where the predicate 
returns true.
'''
def remove_if(predicate, string_list):
    return list(filter(lambda x: not predicate(x), string_list))



'''
Removes empty strings from a list of strings.
'''
def remove_empty_strings(s_list:List[str])->List[str]:
    is_empty = lambda x: not x
    return remove_if(is_empty,s_list)


'''
Removes strings composed only by numbers from a list of strings
'''
def remove_numbers(s_list:List[str])->List[str]:
    num_regex = r'\d+'
    is_number = lambda x: re.search(num_regex,x)
    return remove_if(is_number, s_list)


'''
Removes email addresses from a list of strings
'''
def remove_email_addresses(s_list:List[str])->List[str]:
    email_regex = r'[a-z0-9_.-]+?@[a-z0-9_-]+\.[a-z0-9]'
    is_email_address = lambda x: re.search(email_regex,x)
    return remove_if(is_email_address, s_list)

'''
Checks if a string is a URL
TODO: improve regex
'''
def is_a_URL(s:str)->bool:
    URL_regex = r'(https?:\/\/?(www\.))?[a-z0-9./_-]+\.(com|ac\.uk|org|co\.uk|gov)'
    return re.search(URL_regex,s)



'''
Removes URLs from a list of strings
'''
def remove_URLs(s_list:List[str])->List[str]:
    return remove_if(is_a_URL, s_list)


'''
'''

'''
Removes English stopwords from a list of strings
'''
def remove_stopwords(s_list:List[str])->List[str]:
    is_a_stopword = lambda x: x in nltk.corpus.stopwords.words('english')
    return remove_if(is_a_stopword, s_list)
    

'''
Remove names from a list of strings.
'''
def remove_names(s_list:List[str])->List[str]:
    names = [x.lower() for x in nltk.corpus.names.words()]
    is_a_name = lambda x: x in names 
    return remove_if(is_a_name, s_list)


'''
Returns the nltk.wordnet POS_tag of the word passed as an argument.
This is used by the WordNet lemmatizer in the pipeline.
'''
def wordnet_pos_mapper(s:str):
    pos_map = {"n": "NOUN","v": "VERB","r": "ADV", "j":"ADV"}
    pos = nltk.pos_tag([s])[0][1][0].lower()
    pos = pos_map.get(pos,"NOUN") # Return 'n' in case it's anything that is not in pos_map
    tag = getattr(nltk.wordnet.wordnet,pos)
    return tag


s='''

'''

#cleaned = clean_ticket_description(s)
#print(cleaned)
#print(len(cleaned))
print(remove_URLs(re.split(r'\s+', s)))
