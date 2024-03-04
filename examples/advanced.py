"""
********
Advanced
********

Lets simulate more real scenario. API requests and responses are often very complex
with many deeply nested keys. And when you need to check one of them it may
looks like: ``res.get('data', {}).get('service', {}).get('status', {}).get('current', False)``.

**It's awful!** All this empty dictionary fallback to dig in for current status!
"""

__authors__ = ["Joseph Hwang", "Pawel Zadrozny"]
__copyright__ = "Copyright (c) 2024, Joseph Hwang. Originally written by Pawel Zadrozny"


def api_request():
    """
    Make API request
    ================

    In this scenario we will send post request to create new user with superuser privileges.
    Below there is example response as dictionary, and then the way to check granted privileges.
    """

    def make_request(payload):
        """Fake request for example purpose.

        :param dict payload: Example payload
        :return dict: Example response
        """
        return {
            "status": {
                "code": 200,
                "msg": "User created",
            },
            "data": {
                "user": {
                    "id": 123,
                    "personal": {
                        "name": "Arnold",
                        "email": "arnold@dotty.dict",
                    },
                    "privileges": {
                        "granted": ["login", "guest", "superuser"],
                        "denied": ["admin"],
                        "history": {
                            "actions": [
                                ["superuser granted", "2018-04-29T17:08:48"],
                                ["login granted", "2018-04-29T17:08:48"],
                                ["guest granted", "2018-04-29T17:08:48"],
                                ["created", "2018-04-29T17:08:48"],
                                ["signup_submit", "2018-04-29T17:08:47"],
                            ],
                        },
                    },
                },
            },
        }

    from dotty_dictionary import dotty

    request = dotty()
    request["request.data.payload"] = {
        "name": "Arnold",
        "email": "arnold@dotty.dict",
        "type": "superuser",
    }
    request["request.data.headers"] = {"content_type": "application/json"}
    request["request.url"] = "http://127.0.0.1/api/user/create"

    response = dotty(make_request(request.to_dict()))

    assert response["status.code"] == 200
    assert "superuser" in response["data.user.privileges.granted"]
    # end of api_request


def list_embedded():
    """
    Access dict with embedded lists
    ===============================

    This scenario shows how to access subfield in a list.
    """
    from dotty_dictionary import dotty

    # dotty supports embedded lists
    # WARNING!
    # Dotty used to support lists only with dotty_l.
    # This feature is depreciated and was removed - now lists have native support.
    # If you need old functionality pass additional flag 'no_list' to dotty

    dot = dotty(
        {
            "annotations": [
                {"label": "app", "value": "webapi"},
                {"label": "role", "value": "admin"},
            ],
            "spec": {
                "containers": [
                    ["gpu", "tensorflow", "ML"],
                    ["cpu", "webserver", "sql"],
                ]
            },
        }
    )

    assert dot["annotations.0.label"] == "app"
    assert dot["annotations.0.value"] == "webapi"
    assert dot["annotations.1.label"] == "role"
    assert dot["annotations.1.value"] == "admin"
    assert dot["spec.containers.0.0"] == "gpu"
    assert dot["spec.containers.0.1"] == "tensorflow"
    assert dot["spec.containers.0.2"] == "ML"
    assert dot["spec.containers.1.0"] == "cpu"
    assert dot["spec.containers.1.1"] == "webserver"
    assert dot["spec.containers.1.2"] == "sql"
    # end of list_embedded


def list_slices():
    """
    Access multiple fields with list slices
    =======================================

    This scenario shows how to access multiple subfields in a list of dicts.
    """
    from dotty_dictionary import dotty

    # dotty supports standard Python slices for lists

    dot = dotty(
        {
            "annotations": [
                {"label": "app", "value": "webapi"},
                {"label": "role", "value": "admin"},
                {"label": "service", "value": "mail"},
                {"label": "database", "value": "postgres"},
            ],
        }
    )

    assert dot["annotations.:.label"] == ["app", "role", "service", "database"]
    assert dot["annotations.:2.label"] == ["app", "role"]
    assert dot["annotations.2:.label"] == ["service", "database"]
    assert dot["annotations.::2.label"] == ["app", "service"]
    # end of list_slices


def no_list_flag():
    """
    Access numeric fields as dict keys
    ==================================

    This scenario shows how to access numeric keys which should not be treated as list indices.
    """
    from dotty_dictionary import dotty

    # For special use cases dotty supports dictionary key only access
    # With additional flag no_list passed to dotty
    # all digits and slices will be treated as string keys

    dot = dotty({"special": {"1": "one", ":": "colon", "2:": "two colons"}})

    assert dot["special.1"] == "one"
    assert dot["special.:"] == "colon"
    assert dot["special.2:"] == "two colons"
    # end of no_list_flag


def escape_character():
    """
    Escape character
    =================

    In some cases we want to preserve dot in key name and do not treat it
    as keys separator. It can by done with escape character.
    """
    from dotty_dictionary import dotty

    dot = dotty(
        {
            "deep": {
                "key": "value",
            },
            "key.with.dot": {
                "deeper": "other value",
            },
        }
    )

    # how to access deeper value?
    assert dot[r"key\.with\.dot.deeper"] == "other value"
    # end of escape_character


def escape_the_escape_character():
    """
    Escape the escape character
    ===========================

    What if escape character should be preserved as integral key name,
    but it happens to be placed right before separator character?

    The answer is: Escape the escape character.

    .. warning:: Be careful because backslashes in Python require special treatment.
    """
    from dotty_dictionary import dotty

    dot = dotty(
        {
            "deep": {
                "key": "value",
            },
            "key.with_backslash\\": {  # backslash at the end of key
                "deeper": "other value",
            },
        }
    )

    # escape first dot and escape the escape character before second dot
    assert dot[r"key\.with_backslash\\.deeper"] == "other value"
    # end of escape_the_escape_character
