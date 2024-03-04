import pytest
from dotty_dictionary import Dotty, dotty


@pytest.fixture
def flat_dict():
    return {
        "a.b.c": 1,
        "a.b.d": 2,
        "a.e.0": 3,
        "a.e.1.f": 4,
        "a.e.2.0": 5,
        "a.e.2.1": 6,
        "a.e.2.2": 7,
        "g": 8,
    }


@pytest.fixture
def flat_dict_no_list():
    return {
        "a.b.c": 1,
        "a.b.d": 2,
        "a.e": [3, {"f": 4}, [5, 6, 7]],
        "g": 8,
    }


@pytest.fixture
def dot():
    return dotty(
        {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
                "e": [3, {"f": 4}, [5, 6, 7]],
            },
            "g": 8,
        }
    )


def test_from_flat_dict(flat_dict, dot):
    assert Dotty.from_flat_dict(flat_dict) == dot


def test_to_flat_dict(flat_dict, dot):
    assert dot.to_flat_dict() == flat_dict


def test_from_flat_dict_no_list(flat_dict_no_list, dot):
    assert Dotty.from_flat_dict(flat_dict_no_list, no_list=True) == dot


def test_to_flat_dict_no_list(flat_dict_no_list, dot):
    assert dot.to_flat_dict(no_list=True) == flat_dict_no_list
