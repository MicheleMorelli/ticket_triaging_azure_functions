import nltk
import re
import string
from typing import List, Dict

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
Checks if a string is a number
'''
def is_number(s:str)->bool:
    num_regex = r'\d+'
    return re.search(num_regex,s)

'''
Checks if a string is an email address
'''
def is_potential_email_address(s:str)->bool:
    email_regex = r'[a-z0-9_.-]+?@[a-z0-9_-]+\.[a-z0-9]'
    return re.search(email_regex,s)


'''
Checks if a string is a URL
'''
def is_a_URL(s:str)->bool:
    URL_regex = r'(https?:\/\/?(www\.))?[a-z0-9./_-]+\.(com|ac\.uk|org|co\.uk|gov)'
    return re.search(URL_regex,s)


'''
'''

'''
Removes English stopwords
'''
def remove_stopwords(string_list:List[str]):
    stopwords = nltk.corpus.stopwords.words('english')
    return [x for x in string_list if x not in stopwords]
    

'''
Remove names
'''
def remove_names(string_list:List[str]):
    names = [x.lower() for x in nltk.corpus.names.words()]
    return [x for x in string_list if x not in names]


'''
Returns the nltk.wordnet POS_tag used by the lemmatizer
'''
def wordnet_pos_mapper(s:str):
    pos_map = {"n": "NOUN","v": "VERB","r": "ADV", "j":"ADV"}
    pos = nltk.pos_tag([s])[0][1][0].lower()
    pos = pos_map.get(pos,"NOUN") # Return 'n' in case it's anything that is not in pos_map
    tag = getattr(nltk.wordnet.wordnet,pos)
    return tag


s='''

'''

cleaned = clean_ticket_description(s)
print(cleaned)
print(len(cleaned))

