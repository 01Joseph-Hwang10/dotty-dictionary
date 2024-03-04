import pytest
from dotty_dictionary import dotty


@pytest.fixture
def dot():
    return dotty(
        {
            "field1": {
                "1": "value1",
                "2": {"subfield1": "value2", "subfield2": "value3"},
                ":": "value4",
                "2:": "value5",
                "key": "value6",
            },
        },
        no_list=True,
    )


def test_simple_index(dot):
    assert dot["field1.1"] == "value1"


def test_whole_slice_index(dot):
    assert dot["field1.:"] == "value4"


def test_limit_slice_index(dot):
    assert dot["field1.2:"] == "value5"


def test_normal_key(dot):
    assert dot["field1.key"] == "value6"
