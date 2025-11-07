import pytest
from unittest.mock import patch, MagicMock
from data_handler import ApiDataHandler, ApiError
from user import User
from set import Set
from piece import Piece
import requests

def make_response(json_data, status=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status.return_value = None
    return mock_resp


@patch("data_handler.requests.get")
def test_get_json_success(mock_get):
    mock_get.return_value = make_response({"ok": True})

    api = ApiDataHandler("https://fake.com")
    result = api._get_json("/test")

    assert result == {"ok": True}
    mock_get.assert_called_once_with("https://fake.com/test")


@patch("data_handler.requests.get")
def test_get_json_http_error(mock_get):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mock_resp.status_code = 404
    mock_get.return_value = mock_resp

    api = ApiDataHandler("https://fake.com")

    with pytest.raises(ApiError):
        api._get_json("/bad")


@patch("data_handler.requests.get")
def test_get_json_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError()

    api = ApiDataHandler("https://fake.com")

    with pytest.raises(ApiError):
        api._get_json("/fail")


@patch("data_handler.requests.get")
def test_get_json_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()

    api = ApiDataHandler("https://fake.com")

    with pytest.raises(ApiError):
        api._get_json("/timeout")


@patch("data_handler.requests.get")
def test_get_all_users(mock_get):
    """
    ORDER OF CALLS:
    1. /api/users
    2. /api/user/by-id/1
    """

    # 1. Mock /api/users
    mock_users = make_response({
        "Users": [
            {"id": 1, "username": "dr_crocodile", "brickCount": 42}
        ]
    })

    # 2. Mock /api/user/by-id/1
    mock_user_data = make_response({
        "collection": [
            {
                "pieceId": "3023",
                "variants": [
                    {"color": "blue", "count": 4}
                ]
            }
        ]
    })

    mock_get.side_effect = [mock_users, mock_user_data]

    api = ApiDataHandler("https://fake.com")
    users = api.get_all_users()

    assert len(users) == 1
    user = users[0]

    assert isinstance(user, User)
    assert user.username == "dr_crocodile"
    assert user.brick_count == 42

    # Check inventory
    piece = Piece("3023", "blue")
    assert user.inventory[piece] == 4


@patch("data_handler.requests.get")
def test_get_user_by_username(mock_get):
    """
    ORDER OF CALLS:
    1. /api/user/by-username/...
    2. /api/user/by-id/...
    """

    summary = make_response({
        "id": 5,
        "username": "bricklover",
        "brickCount": 99
    })

    full_user = make_response({
        "collection": [
            {
                "pieceId": "3001",
                "variants": [{"color": "red", "count": 12}]
            }
        ]
    })

    mock_get.side_effect = [summary, full_user]

    api = ApiDataHandler("https://fake.com")
    user = api.get_user_by_username("bricklover")

    assert isinstance(user, User)
    assert user.user_id == 5
    assert user.username == "bricklover"
    assert user.brick_count == 99

    assert user.inventory[Piece("3001", "red")] == 12


@patch("data_handler.requests.get")
def test_get_all_sets(mock_get):

    # /api/sets
    sets_list = make_response({
        "Sets": [
            {"id": 100, "name": "Cool Castle", "totalPieces": 3}
        ]
    })

    # /api/set/by-id/100
    set_full = make_response({
        "id": 100,
        "name": "Cool Castle",
        "totalPieces": 3,
        "pieces": [
            {"part": {"designID": "3023", "material": "blue"}, "quantity": 2},
            {"part": {"designID": "3001", "material": "red"}, "quantity": 1}
        ]
    })

    mock_get.side_effect = [sets_list, set_full]

    api = ApiDataHandler("https://fake.com")

    sets = api.get_all_sets()
    assert len(sets) == 1

    s = sets[0]
    assert isinstance(s, Set)
    assert s.name == "Cool Castle"

    assert s.required_pieces[Piece("3023", "blue")] == 2
    assert s.required_pieces[Piece("3001", "red")] == 1


@patch("data_handler.requests.get")
def test_get_set_by_set_name(mock_get):

    # 1. summary call
    summary = make_response({
        "id": 200,
        "name": "Mega Tower",
        "totalPieces": 5
    })

    # 2. full details call
    full = make_response({
        "id": 200,
        "name": "Mega Tower",
        "totalPieces": 5,
        "pieces": [
            {"part": {"designID": "3069", "material": "black"}, "quantity": 3},
            {"part": {"designID": "3003", "material": "yellow"}, "quantity": 2}
        ]
    })

    mock_get.side_effect = [summary, full]

    api = ApiDataHandler("https://fake.com")

    s = api.get_set_by_set_name("Mega Tower")

    assert isinstance(s, Set)
    assert s.name == "Mega Tower"

    assert s.required_pieces[Piece("3069", "black")] == 3
    assert s.required_pieces[Piece("3003", "yellow")] == 2
