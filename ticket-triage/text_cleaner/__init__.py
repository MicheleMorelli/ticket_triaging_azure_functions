import re
import string
import typing  # for TypeAliases/pseudotypes such as Match
from typing import *
import nltk
from toolz import pipe

_LEMMATISER = nltk.WordNetLemmatizer()


def functional_cleaner(ticket_description: str) -> List[str]:
    '''
    Takes a ticket description as an argument, and passes it though a functional 
    pipeline, that sanitises, tokenise and lemmatise it, and returns as a list of 
    strings.
    '''
    return pipe(
        # the input list (*TO LOWER CASE!*)
        re.split(r'\s+', ticket_description.lower()),
        transform_relevant_URLs_into_tags,
        remove_twitter_contacts,
        remove_email_addresses,
        remove_URLs,
        remove_non_printable_hex,
        remove_stopwords,
        remove_punctuation,
        remove_non_ASCII_chars,
        remove_ticket_references,
        # NUMBERS ===============================
        # remove_numbers,
        # remove_strings_starting_with_numbers,
        remove_strings_containing_any_numbers,  # may be too much!
        remove_very_long_words,
        remove_very_short_words,
        remove_empty_strings,  # don't pass empty strings to the lemmatizer!
        remove_names,
        remove_residual_URLs,
        lemmatize_all
    )


def remove_if(predicate, string_list):
    '''
    Higher order function to be used in the sanitizer's pipeline. It takes a predicate
    and a string list, and removes all the elements of the list where the predicate 
    returns true.
    '''
    return list(filter(lambda x: not predicate(x), string_list))


def remove_empty_strings(s_list: List[str]) -> List[str]:
    '''
    Removes empty strings from a list of strings.
    '''
    def is_empty(x): return not x
    return remove_if(is_empty, s_list)


def remove_strings_containing_any_numbers(s_list: List[str]) -> List[str]:
    '''
    Remove all the strings that contain a number. Might be too extreme!
    '''
    num_regex = r'[0-9]+'
    def is_number(x): return re.search(num_regex, x)
    return remove_if(is_number, s_list)


def remove_non_printable_hex(s_list: List[str]) -> List[str]:
    '''
    Removes escaped hexadecimals such as \x43
    '''
    hex_regex = r'\\x\d+'
    def is_hex(x): return re.search(hex_regex, x)
    return remove_if(is_hex, s_list)


def remove_numbers(s_list: List[str]) -> List[str]:
    '''
    Removes strings composed by *only* numbers from a list of strings
    '''
    num_regex = r'^[0-9]+$'
    def is_number(x): return re.search(num_regex, x)
    return remove_if(is_number, s_list)


def remove_strings_starting_with_numbers(s_list: List[str]) -> List[str]:
    '''
    Removes strings starting with numbers from a list of strings
    '''
    start_with_num_regex = r'^[0-9]+'
    def starts_with_number(x): return re.search(start_with_num_regex, x)
    return remove_if(starts_with_number, s_list)


def remove_punctuation(s_list: List[str]) -> List[str]:
    '''
    Removes all punctuation from the words in a list of strings
    '''
    return [x.translate(str.maketrans(" ", " ", string.punctuation)) for x in s_list]


def remove_non_ASCII_chars(s_list: List[str]) -> List[str]:
    '''
    Removes non-ascii characters. MIght be too aggressive
    '''
    return [x.encode('ascii', 'ignore').decode('ascii') for x in s_list]


def remove_very_long_words(s_list: List[str]) -> List[str]:
    '''
    Removes very long words. Especially useful to remove hashes, residual URLs and 
    other anomalies
    '''
    long_threshold = 25  # this is arbitrary, and has been adjusted by checking the results
    def is_a_very_long_word(x): return len(x) >= long_threshold
    return remove_if(is_a_very_long_word, s_list)


def remove_very_short_words(s_list: List[str]) -> List[str]:
    '''
    Removes very short words. 
    '''
    short_threshold = 2  # this is arbitrary, and has been adjusted by checking the results
    def is_a_very_short_word(x): return len(x) <= short_threshold
    return remove_if(is_a_very_short_word, s_list)


def remove_ticket_references(s_list: List[str]) -> List[str]:
    '''
    Removes ticket identifiers
    '''
    ticketid_regex = r'^inc\d+$'  # Service now format
    def is_a_ticket_identifier(x): return re.search(ticketid_regex, x)
    return remove_if(is_a_ticket_identifier, s_list)


def remove_email_addresses(s_list: List[str]) -> List[str]:
    '''
    Removes email addresses from a list of strings
    '''
    email_regex = r'[a-z0-9_.-]+?@[a-z0-9_-]+\.[a-z0-9]'
    def is_email_address(x): return re.search(email_regex, x)
    return remove_if(is_email_address, s_list)


def remove_twitter_contacts(s_list: List[str]) -> List[str]:
    '''
    Removes email addresses from a list of strings
    '''
    twitter_regex = r'^@[a-z0-9_-]+$'
    def is_twitter_contact(x): return re.search(twitter_regex, x)
    return remove_if(is_twitter_contact, s_list)


def transform_relevant_URLs_into_tags(s_list: List[str]) -> List[str]:
    '''
    Takes a list of strings, and checks whether any string contains a URL relevant
    to one of the services (Moodle or Open Access repositories), and if so, 
    it transforms it into a recognisable tag.
    '''
    def transform_relevant_URL(x): return turn_into_tag(
        x) if (is_relevant_URL(x)) else x
    return list(map(transform_relevant_URL, s_list))


def turn_into_tag(s: str) -> str:
    return "BLOOMPOTENTIALURL" if is_bloom_URL(s) else "RESTECHPOTENTIALURL"


def is_relevant_URL(s: str) -> Union[typing.Match[str], None, bool]:
    return re.search(r'\.ac\.uk$', s) and ((is_bloom_URL(s) or is_restech_URL(s)))


def is_bloom_URL(s: str) -> Optional[typing.Match[str]]:
    return re.search(r'bloom|vle|moodle|ble', s)


def is_restech_URL(s: str) -> Optional[typing.Match[str]]:
    return re.search(r'eprint|research|researchdata|repository|open|access|publications|data', s)


def is_a_URL(s: str) -> Optional[typing.Match[str]]:
    '''
    Checks if a string is a URL
    Using regex found at 
    Daveo (username), https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url 
    '''
    URL_regex = r'[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    return re.search(URL_regex, s)


def remove_URLs(s_list: List[str]) -> List[str]:
    '''
    Removes URLs from a list of strings
    '''
    return remove_if(is_a_URL, s_list)


def remove_residual_URLs(s_list: List[str]) -> List[str]:
    '''
    Removes residual URLs (which for some reason were not removed in previous steps)
    '''
    def is_residual_URL(x): return re.search(
        r'^www', x) or re.search(r'acuk$', x)
    return remove_if(is_residual_URL, s_list)


def remove_stopwords(s_list: List[str]) -> List[str]:
    '''
    Removes English stopwords from a list of strings
    '''
    def is_a_stopword(x): return x in nltk.corpus.stopwords.words('english')
    return remove_if(is_a_stopword, s_list)


def remove_names(s_list: List[str]) -> List[str]:
    '''
    Remove names from a list of strings.
    '''
    names = [x.lower() for x in nltk.corpus.names.words()]
    def is_a_name(x): return x in names
    return remove_if(is_a_name, s_list)


def lemmatize_all(s_list: List[str]) -> List[str]:
    '''
    Wrapper of the WordNet lemmatizer to be used in the pipeline.
    Lemmatises the words using the pos_mapper helper function below.
    '''
    lem = _LEMMATISER
    return [lem.lemmatize(x, wordnet_pos_mapper(x)) for x in s_list]


def wordnet_pos_mapper(s: str):
    '''
    Returns the nltk.wordnet POS_tag of the word passed as an argument.
    This is used by the WordNet lemmatizer in the pipeline.
    '''
    pos_map = {"n": "NOUN", "v": "VERB", "r": "ADV", "j": "ADV"}
    pos = nltk.pos_tag([s])[0][1][0].lower()
    # Return 'n' in case it's anything that is not in pos_map
    pos = pos_map.get(pos, "NOUN")
    tag = getattr(nltk.wordnet.wordnet, pos)
    return tag
