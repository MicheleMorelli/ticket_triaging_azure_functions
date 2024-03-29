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
    desc = "this is preposterous!"
    assert tc.functional_cleaner(desc) == ["preposterous"]


def test_functional_cleaner2():
    desc = "I am experiencing a problem with www.mybloomvle.ac.uk"
    assert tc.functional_cleaner(desc) == ["experience","problem", "BLOOMPOTENTIALURL"]


def test_functional_cleaner3():
    desc = "www.google.com is not working. Could you please look into it?"
    assert tc.functional_cleaner(desc) == ["work", "could", "please","look"]

def test_remove_strings_starting_with_numbers():
    lst_str = ["test1", "a4", "3test"]
    assert tc.remove_strings_starting_with_numbers(lst_str) == ["test1", "a4"]


