import pytest
from dotty_dictionary import Dotty, dotty


@pytest.fixture
def dot():
    return dotty(
        {
            "flat_key": "flat value",
            "deep": {
                "nested": 12,
                "deeper": {
                    "secret": "abcd",
                    "ridiculous": {
                        "hell": "is here",
                    },
                },
            },
        }
    )


def test_access_flat_value(dot):
    assert dot["flat_key"] == "flat value"


def test_raise_key_error_if_key_does_not_exist(dot):
    with pytest.raises(KeyError):
        dot["not_existing"]


def test_access_deep_nested_value(dot):
    assert dot["deep.nested"] == 12


def test_access_middle_nested_value(dot):
    assert dot["deep.deeper.ridiculous"] == {"hell": "is here"}


def test_set_flat_value(dot):
    dot["new_flat"] = "super flat"
    assert "new_flat" in dot


def test_set_deep_nested_value(dot):
    dot["deep.new_key"] = "new value"
    assert "new_key" in dot["deep"]


def test_set_new_deeply_nested_value(dot):
    dot["other.chain.of.keys"] = True
    assert dot._data == {
        "flat_key": "flat value",
        "deep": {
            "nested": 12,
            "deeper": {
                "secret": "abcd",
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
        "other": {
            "chain": {
                "of": {
                    "keys": True,
                },
            },
        },
    }


def test_dotty_has_flat_key(dot):
    assert "flat_key" in dot


def test_dotty_has_deeply_nested_key(dot):
    assert "deep.nested" in dot


def test_dotty_has_not_flat_key(dot):
    assert "some_key" not in dot


def test_dotty_has_not_deeply_nested_key(dot):
    assert "deep.other.chain" not in dot


def test_has_in(dot):
    result = "deep.deeper.secret" in dot
    assert result


def test_has_not_in(dot):
    result = "deep.other" in dot
    assert not result


def test_delete_flat_key(dot):
    del dot["flat_key"]
    assert dot._data == {
        "deep": {
            "nested": 12,
            "deeper": {
                "secret": "abcd",
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
    }


def test_delete_nested_key(dot):
    del dot["deep.deeper.secret"]
    assert dot._data == {
        "flat_key": "flat value",
        "deep": {
            "nested": 12,
            "deeper": {
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
    }


def test_raise_key_error_on_delete_not_existing_key(dot):
    with pytest.raises(KeyError):
        del dot["deep.deeper.key"]


def test_set_value_with_escaped_separator(dot):
    dot[r"deep.deeper.escaped\.dot_key"] = "it works!"
    assert dot._data == {
        "flat_key": "flat value",
        "deep": {
            "nested": 12,
            "deeper": {
                "escaped.dot_key": "it works!",
                "secret": "abcd",
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
    }


def test_get_value_with_escaped_separator(dot):
    dot = dotty(
        {
            "flat_key": "flat value",
            "deep": {
                "nested": 12,
                "deeper": {
                    "escaped.dot_key": "it works!",
                    "secret": "abcd",
                    "ridiculous": {
                        "hell": "is here",
                    },
                },
            },
        }
    )
    result = dot[r"deep.deeper.escaped\.dot_key"]
    assert result == "it works!"


def test_get_value_with_escaped_escape_separator(dot):
    dot = dotty(
        {
            "flat_key": "flat value",
            "deep": {
                "nested": 12,
                "deeper": {
                    "escaped\\": {
                        "dot_key": "it works!",
                    },
                    "secret": "abcd",
                    "ridiculous": {
                        "hell": "is here",
                    },
                },
            },
        }
    )
    result = dot[r"deep.deeper.escaped\\.dot_key"]
    assert result == "it works!"


def test_use_custom_separator_and_custom_escape_char(dot):
    sep = ","
    esc = "$"
    dot = Dotty({}, separator=sep, esc_char=esc)
    dot["abcd,efg,hij"] = "test"
    dot["abcd,efg$,hij"] = "test2"
    dot[r"abcd,efg\$,hij"] = "test3"
    assert dot._data == {
        "abcd": {
            "efg": {
                "hij": "test",
            },
            "efg,hij": "test2",
            "efg$": {
                "hij": "test3",
            },
        },
    }


def test_string_digit_key(dot):
    dot = dotty({"field": {"1": "one", "5": "five"}})

    dict_one = dot["field.1"]
    dict_five = dot["field.5"]

    assert dict_one == "one"
    assert dict_five == "five"


def test_integer_keys(dot):
    dot = dotty({"field": {1: "one", 5: "five"}})

    dict_one = dot["field.1"]
    dict_five = dot["field.5"]

    assert dict_one == "one"
    assert dict_five == "five"


def test_data_gathering_with_int(dot):
    dot = dotty(
        {
            "2": "string_value",
            2: "int_value",
            "nested": {"2": "nested_string_value", 3: "nested_int_value"},
        }
    )

    dict_string = dot["2"]
    dict_int = dot[2]
    nested_dict_string = dot["nested.2"]
    nested_dict_int = dot["nested.3"]

    assert dict_string == "string_value"
    assert dict_int == "int_value"
    assert nested_dict_string == "nested_string_value"
    assert nested_dict_int == "nested_int_value"


def test_non_standard_key_types(dot):
    dot = Dotty(
        {3.3: "float", True: "bool", None: "None", "nested": {4.4: "nested_float"}},
        separator=",",
    )

    dict_float = dot[3.3]
    dict_bool = dot[True]
    dict_none = dot[None]
    nested_dict_float = dot["nested,4.4"]
    assert dict_float == "float"
    assert dict_bool == "bool"
    assert dict_none == "None"
    assert nested_dict_float == "nested_float"
