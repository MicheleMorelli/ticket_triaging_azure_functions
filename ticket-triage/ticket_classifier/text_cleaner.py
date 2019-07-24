import nltk
import re
import string
from typing import List, Dict
from toolz import pipe


'''
Takes a ticket description as an argument, and passes it though a functional 
pipeline, that sanitises, tokenise and lemmatise it, and returns as a list of 
strings.
'''
def functional_cleaner(ticket_description:str)->List[str]:
    return pipe( 
            re.split(r'\s+', ticket_description.lower()), # the input list (*TO LOWER CASE!*)
            transform_relevant_URLs_into_tags,
            remove_twitter_contacts,
            remove_email_addresses,
            remove_URLs,
            remove_stopwords,
            remove_punctuation,
            #remove_numbers,
            remove_strings_starting_with_numbers,
            remove_ticket_references,
            remove_very_long_words,
            remove_very_short_words,
            remove_empty_strings, # don't pass empty strings to the lemmatizer!
            remove_names,
            #lemmatize_all
            )



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
Removes strings composed by only numbers from a list of strings
'''
def remove_numbers(s_list:List[str])->List[str]:
    num_regex = r'^[0-9]+$'
    is_number = lambda x: re.search(num_regex,x)
    return remove_if(is_number, s_list)


'''
Removes strings composed by only numbers from a list of strings
'''
def remove_strings_starting_with_numbers(s_list:List[str])->List[str]:
    start_with_num_regex = r'^[0-9]+'
    starts_with_number = lambda x: re.search(start_with_num_regex,x)
    return remove_if(starts_with_number, s_list)
    

'''
Removes all punctuation from the words in a list of strings
'''
def remove_punctuation(s_list:List[str])->List[str]:
    return [x.translate(str.maketrans("", "", string.punctuation)) for x in s_list]


'''
Removes very long words. Especially useful to remove hashes, residual URLs and 
other anomalies
'''
def remove_very_long_words(s_list:List[str])-> List[str]:
    long_threshold = 25 # this is arbitrary, and has been adjusted by checking the results
    is_a_very_long_word = lambda x: len(x) >= long_threshold
    return remove_if(is_a_very_long_word, s_list)


'''
Removes very short words. 
'''
def remove_very_long_words(s_list:List[str])-> List[str]:
    short_threshold = 2 # this is arbitrary, and has been adjusted by checking the results
    is_a_very_short_word = lambda x: len(x) <= short_threshold
    return remove_if(is_a_very_short_word, s_list)


'''
Removes ticket identifiers
'''
def remove_ticket_references(s_list: List[str]) = > List[str]:
    ticketid_regex = r'^inc\d+$' # Service now format
    is_a_ticket_identifier = lambda x: re.search(ticketid_regex,x)
    return remove_if(is_a_ticket_identifier, s_list)



'''
Removes email addresses from a list of strings
'''
def remove_email_addresses(s_list:List[str])->List[str]:
    email_regex = r'[a-z0-9_.-]+?@[a-z0-9_-]+\.[a-z0-9]'
    is_email_address = lambda x: re.search(email_regex,x)
    return remove_if(is_email_address, s_list)


'''
Removes email addresses from a list of strings
'''
def remove_twitter_contacts(s_list:List[str])->List[str]:
    twitter_regex = r'^@[a-z0-9_-]+$'
    is_twitter_contact = lambda x: re.search(twitter_regex,x)
    return remove_if(is_twitter_contact, s_list)



'''
Takes a list of strings, and checks whether any string contains a URL relevant
to one of the services (Moodle or Open Access repositories), and if so, 
it transforms it into a recognisable tag.
'''
def transform_relevant_URLs_into_tags(s_list:List[str])->List[str]:
    transform_relevant_URL = lambda x: turn_into_tag(x) if (is_relevant_URL(x)) else x
    return list(map(transform_relevant_URL, s_list))


def turn_into_tag(s:str)->str:
    return "BLOOMPOTENTIALURL" if is_bloom_URL(s) else "RESTECHPOTENTIALURL"


def is_relevant_URL(s:str)->bool:
    return is_a_URL(s) and (is_bloom_URL(s) or is_restech_URL(s))
    

def is_bloom_URL(s:str)->bool:
    return any(filter(lambda x: re.search(re.escape(x), s), bloom_words()))
    

def is_restech_URL(s:str)->bool:
    return any(filter(lambda x: re.search(re.escape(x), s), restech_words()))

'''
Returns a list of Moodle-related words that are often used in URLs
TODO: Expand list!
'''
def bloom_words()->List[str]:
    return['bloom','vle','moodle','ble']


'''
Returns a list of Open Access repository-related words that are often used in URLs
TODO: Expand list!
'''
def restech_words()->List[str]:
    return[
            'eprint',
            'research',
            'researchdata',
            'repository', 
            'open', 
            'access',
            'publications',
            'data'
            ]


'''
Checks if a string is a URL
Using regex found at 
Daveo (username), https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url 
'''
def is_a_URL(s:str)->bool:
    URL_regex = r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)'
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
Wrapper of the WordNet lemmatizer to be used in the pipeline.
Lemmatises the words using the pos_mapper helper function below.
'''
def lemmatize_all(s_list:List[str])->List[str]:
    lem = nltk.WordNetLemmatizer()
    return [lem.lemmatize(x, wordnet_pos_mapper(x)) for x in s_list]



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
print(functional_cleaner(s))

#url1 = 'https://moodle.royalholloway.ac.uk/course/view.php?id=6477' 
#url2 = '[https://research.royalholloway.ac.uk/course/view.php?id=6477]'
#print(is_relevant_URL(url1))
#print(is_relevant_URL(url2))
#print(transform_relevant_URLs_into_tags([url1,url2,"asdas","sdfsdf"]))

