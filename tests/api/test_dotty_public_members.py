from dotty_dictionary import dotty


def test_to_dict():
    plain_dict = {"very": {"deeply": {"nested": {"thing": "spam"}}}}
    dot = dotty(plain_dict)
    assert isinstance(dot.to_dict(), dict)
    assert sorted(dot.to_dict().items()) == sorted(plain_dict.items())


def test_nested_dotty_object_to_dict():
    expected_dict = {"hello": {"world": 1}, "nested": {"dotty": {"wazaa": 3}}}
    top_dot = dotty({"hello": {"world": 1}})
    nested_dot = dotty({"wazaa": 3})
    top_dot["nested.dotty"] = nested_dot
    assert top_dot.to_dict() == expected_dict


def test_nested_dotty_in_list_to_dict():
    expected_dict = {"testlist": [{"dot1": 1}, {"dot2": 2}]}
    dot_list = [dotty({"dot1": 1}), dotty({"dot2": 2})]
    top_dot = dotty({"testlist": dot_list})
    assert top_dot.to_dict() == expected_dict
