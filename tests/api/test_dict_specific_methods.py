import pytest
from dotty_dictionary import dotty, Dotty


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


def test_access_keys(dot):
    keys = sorted(dot.keys())
    assert keys == ["deep", "flat_key"]


def test_access_keys_from_deeply_nested_structure(dot):
    keys = sorted(dot["deep.deeper"].keys())
    assert keys == ["ridiculous", "secret"]


def test_get_value_without_default(dot):
    result = dot.get("deep.nested")
    assert result == 12


def test_get_value_with_default(dot):
    result = dot.get("deep.other", False)
    assert not result


def test_return_dotty_length(dot):
    assert len(dot) == 2


def test_pop_from_dotty_flat(dot):
    result = dot.pop("flat_key")
    assert result == "flat value"
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


def test_pop_with_default_value(dot):
    result = dot.pop("not_existing", "abcd")
    assert result == "abcd"
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
    }


def test_pop_nested_key(dot):
    result = dot.pop("deep.nested")
    assert result == 12
    assert dot._data == {
        "flat_key": "flat value",
        "deep": {
            "deeper": {
                "secret": "abcd",
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
    }


def test_pop_nested_key_with_default_value(dot):
    result = dot.pop("deep.deeper.not_existing", "abcd")
    assert result == "abcd"
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
    }


def test_setdefault_flat_not_existing(dot):
    result = dot.setdefault("next_flat", "new default value")
    assert result == "new default value"
    assert dot._data == {
        "flat_key": "flat value",
        "next_flat": "new default value",
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


def test_setdefault_flat_existing(dot):
    dot["next_flat"] = "original value"
    result = dot.setdefault("next_flat", "new default value")
    assert result == "original value"
    assert dot._data == {
        "flat_key": "flat value",
        "next_flat": "original value",
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


def test_setdefault_nested_key_not_existing(dot):
    result = dot.setdefault("deep.deeper.next_key", "new default value")
    assert result == "new default value"
    assert dot._data == {
        "flat_key": "flat value",
        "deep": {
            "nested": 12,
            "deeper": {
                "next_key": "new default value",
                "secret": "abcd",
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
    }


def test_setdefault_nested_key_existing(dot):
    dot["deep.deeper.next_key"] = "original value"
    result = dot.setdefault("deep.deeper.next_key", "new default value")
    assert result == "original value"
    assert dot._data == {
        "flat_key": "flat value",
        "deep": {
            "nested": 12,
            "deeper": {
                "next_key": "original value",
                "secret": "abcd",
                "ridiculous": {
                    "hell": "is here",
                },
            },
        },
    }


def test_copy(dot):
    first = dotty({"a": 1, "b": 2})
    second = first.copy()

    assert isinstance(second, Dotty)
    assert first == second
    assert first is not second
    assert first._data is not second._data


def test_fromkeys(dot):
    dot = dotty().fromkeys({"a", "b", "c"}, value=10)
    assert dot.to_dict() == {"a": 10, "b": 10, "c": 10}
    assert isinstance(dot, Dotty)


def test_keys(dot):
    assert dot.keys() == {"flat_key", "deep"}


def test_values(dot):
    assert sorted(dot.values(), key=str) == sorted(["flat value", dot["deep"]], key=str)


def test_items(dot):
    assert sorted(dot.items(), key=str) == sorted(
        [("flat_key", "flat value"), ("deep", dot["deep"])],
        key=str,
    )


def test_update(dot):
    update_dict = {"a": 1, "b": {"c": "d", "e": ["f", "g"]}}
    dot.update(update_dict)
    assert dot.to_dict() == {
        **update_dict,
        "flat_key": "flat value",
        "deep": dot["deep"],
    }


def test_clear(dot):
    dot.clear()
    assert dot.to_dict() == {}
