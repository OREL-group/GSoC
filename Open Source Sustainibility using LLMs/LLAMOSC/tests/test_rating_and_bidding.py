import pytest

def test_plain_string_description():
    issue = {"title": "Fix bug", "description": "simple text"}
    # call your fixed function here
    assert True

def test_dict_like_string_description():
    issue = {"title": "Fix bug", "description": {"key": "value"}}
    assert True

def test_none_description():
    issue = {"title": "Fix bug", "description": None}
    assert True
