import pytest
from dotty_dictionary import dotty


@pytest.fixture
def dot():
    return dotty(
        {
            "field1": [
                {"subfield1": "value01", "subfield2": "value02"},
                {"subfield1": "value11", "subfield2": "value12"},
                {"subfield1": "value21", "subfield2": "value22"},
                {"subfield1": "value31", "subfield2": "value32"},
            ],
            "field2": [
                {
                    "subfield1": [
                        {
                            "nestedsubfield1": "nestedvalue001",
                            "nestedsubfield2": "nestedvalue002",
                        },
                        {
                            "nestedsubfield1": "nestedvalue011",
                            "nestedsubfield2": "nestedvalue012",
                        },
                    ]
                },
                {
                    "subfield1": [
                        {
                            "nestedsubfield1": "nestedvalue101",
                            "nestedsubfield2": "nestedvalue102",
                        },
                        {
                            "nestedsubfield1": "nestedvalue111",
                            "nestedsubfield2": "nestedvalue112",
                        },
                    ]
                },
            ],
        }
    )


def test_whole_shallow_multiple_list(dot):
    expected_list = ["value01", "value11", "value21", "value31"]
    assert dot["field1.:.subfield1"] == expected_list


def test_whole_nested_multiple_list(dot):
    expected_list = [
        ["nestedvalue001", "nestedvalue011"],
        ["nestedvalue101", "nestedvalue111"],
    ]
    assert dot["field2.:.subfield1.:.nestedsubfield1"] == expected_list


def test_left_side_slice(dot):
    expected_list = ["value21", "value31"]
    assert dot["field1.2:.subfield1"] == expected_list


def test_right_side_slice(dot):
    expected_list = ["value01", "value11"]
    assert dot["field1.:2.subfield1"] == expected_list


def test_both_side_slice(dot):
    expected_list = ["value11", "value21"]
    assert dot["field1.1:3.subfield1"] == expected_list


def test_step_slice(dot):
    expected_list = ["value01", "value21"]
    assert dot["field1.::2.subfield1"] == expected_list


def test_return_whole_list(dot):
    expected_list = [
        {"subfield1": "value01", "subfield2": "value02"},
        {"subfield1": "value11", "subfield2": "value12"},
        {"subfield1": "value21", "subfield2": "value22"},
        {"subfield1": "value31", "subfield2": "value32"},
    ]
    assert dot["field1.:"] == expected_list
