import text_cleaner as tc


def test_remove_empty_strings():
    lst_str = ["test1", "test2", "", "", "test3"]
    assert tc.remove_empty_strings(lst_str) == ["test1", "test2", "test3"] 


def test_remove_empty_strings2():
    lst_str = ["test1", "test2", "", "", "test3"]
    assert len(tc.remove_empty_strings(lst_str)) == 3 


def test_remove_strings_containing_any_numbers():
    lst_str = ["test1", "test2", "NoNums", "test", "test3"]
    assert tc.remove_strings_containing_any_numbers(lst_str) == ["NoNums", "test"]


def test_remove_non_printable_hex():
    lst_str = ["test1", "\\x56", "\\x43"]
    assert tc.remove_non_printable_hex(lst_str) == ["test1"]


def test_remove_numbers():
    lst_str = ["test1", "\\x43", "234234", "r3242342"]
    assert tc.remove_numbers(lst_str) == ["test1", "\\x43", "r3242342"]

def test_functional_cleaner():
    pass


def test_is_a_URL():
    pass


def test_is_bloom_URL():
    pass


def test_is_relevant_URL():
    pass


def test_is_restech_URL():
    pass


def test_lemmatize_all():
    pass


def test_nltk():
    pass


def test_no_type_check():
    pass


def test_no_type_check_decorator():
    pass


def test_overload():
    pass


def test_pipe():
    pass


def test_re():
    pass


def test_remove_URLs():
    pass


def test_remove_email_addresses():
    pass


def test_remove_empty_strings():
    pass


def test_remove_if():
    pass


def test_remove_names():
    pass


def test_remove_non_ASCII_chars():
    pass


def test_remove_non_printable_hex():
    pass


def test_remove_numbers():
    pass


def test_remove_punctuation():
    pass


def test_remove_residual_URLs():
    pass


def test_remove_stopwords():
    pass


def test_remove_strings_containing_any_numbers():
    pass


def test_remove_strings_starting_with_numbers():
    pass


def test_remove_ticket_references():
    pass


def test_remove_twitter_contacts():
    pass


def test_remove_very_long_words():
    pass


def test_remove_very_short_words():
    pass


def test_string():
    pass


def test_transform_relevant_URLs_into_tags():
    pass


def test_turn_into_tag():
    pass

