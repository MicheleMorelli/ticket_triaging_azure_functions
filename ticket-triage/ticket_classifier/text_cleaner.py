import nltk
import re
import string

def clean_ticket_description(ticket_description:str):
    #to lower case
    ticket_description = ticket_description.lower()
    # separate based on white spaces
    all_words = re.split("\s+",ticket_description)
    # find related urls and replace
    # lemmatize
    tokens = all_words
    return tokens



def only_text(s):
    pass


'''
Returns the nltk.wordnet POS_tag used by the lemmatizer
'''
def wordnet_pos_mapper(s:str):
    pos_map = {"n": "NOUN","v": "VERB","r": "ADV", "j":"ADV"}
    pos = nltk.pos_tag([s])[0][1][0].lower()
    pos = pos_map.get(pos,"NOUN")
    tag = getattr(nltk.wordnet.wordnet,pos)
    return tag


def test(x):
    return str(x) + "!"
