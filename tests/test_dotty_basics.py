import pytest
from dotty_dictionary import dotty


def test_create_empty_instance():
    dot = dotty()
    assert dot == {}


def test_create_non_empty_instance():
    plain_dict = {"not": "empty"}

    dot = dotty(plain_dict)
    assert dot == plain_dict
    assert dot is not plain_dict


def test_raise_attr_error_if_input_is_not_dict():
    with pytest.raises(AttributeError):
        dotty(["not", "valid"])


def test_two_dotty_with_the_same_input_should_be_equal():
    first = dotty({"is": "valid"})
    second = dotty({"is": "valid"})

    assert first == second


def test_two_dotty_with_different_input_should_not_be_equal():
    first = dotty({"counter": 1})
    second = dotty({"counter": 2})

    assert first != second


def test_plain_dict_and_dotty_wrapper_should_be_equal():
    plain = {"a": 1, "b": 2}
    dot = dotty(plain)
    assert dot == plain


def test_dotty_and_not_mapping_instance_should_not_be_equal():
    dot = dotty({"a": 1, "b": 2})
    assert dot != [("a", 1), ("b", 2)]
    assert dot != ("a", 1)
    assert dot != {1, 2, 3}
    assert dot != 123
    assert dot != "a:1, b:2"


def test_pop_with_default_value():
    dot = dotty()
    assert dot.pop("does.not.exist", None) is None
    assert dot.pop("does.not.exist", 55) == 55
    assert dot.pop("does.not.exist", "my_value") == "my_value"
