import pytest
from unittest.mock import patch, MagicMock
from data_handler import ApiDataHandler
from user import User
from set import Set
from piece import Piece
import requests

@pytest.fixture
def api_handler():
    return ApiDataHandler("https://fake-api.com")

@patch("data_handler.requests.get")
def test_get_json_success(mock_get, api_handler):
    """Test _get_json returns parsed JSON on success."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = api_handler._get_json("/api/test")
    assert result == {"ok": True}
    mock_get.assert_called_once_with("https://fake-api.com/api/test")

@patch("data_handler.requests.get")
def test_get_json_http_error(mock_get, api_handler, capsys):
    """Test handling of HTTP error."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
    mock_get.return_value = mock_response

    result = api_handler._get_json("/api/error")
    captured = capsys.readouterr()

    assert result is None
    assert "HTTP error" in captured.out or "Request exception" in captured.out

@patch("data_handler.requests.get")
def test_get_json_connection_error(mock_get, api_handler, capsys):
    """Test handling of connection error."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

    result = api_handler._get_json("/api/users")
    captured = capsys.readouterr()

    assert result is None
    assert "Connection error" in captured.out or "Request exception" in captured.out

@patch.object(ApiDataHandler, "_get_json")
def test_get_all_users(mock_get_json, api_handler):
    """Test that get_all_users returns list of User objects."""
    mock_get_json.side_effect = [
        # Response 1: list of users
        {"Users": [{"id": 1, "username": "brickfan35", "brickCount": 6}]},
        # Response 2: user by ID
        {
            "collection": [
                {"pieceId": "3023", "variants": [{"color": "blue", "count": 4}]},
                {"pieceId": "4286", "variants": [{"color": "red", "count": 2}]},
            ]
        },
    ]

    users = api_handler.get_all_users()
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, User)
    assert user.username == "brickfan35"
    assert len(user.inventory) == 2

    pieces = list(user.inventory.keys())
    assert all(isinstance(p, Piece) for p in pieces)
    assert user.inventory[Piece("3023", "blue")] == 4
    assert user.inventory[Piece("4286", "red")] == 2

@patch.object(ApiDataHandler, "_get_json")
def test_get_user_by_username(mock_get_json, api_handler):
    """Test that get_user_by_username returns a User object."""
    mock_get_json.side_effect = [
        # Response 1: user summary
        {"id": 1, "username": "brickfan35", "brickCount": 6},
        # Response 2: user full data
        {
            "collection": [
                {"pieceId": "3023", "variants": [{"color": "blue", "count": 4}]},
                {"pieceId": "4286", "variants": [{"color": "red", "count": 2}]},
            ]
        },
    ]

    user = api_handler.get_user_by_username("brickfan35")
    assert isinstance(user, User)
    assert user.username == "brickfan35"
    assert len(user.inventory) == 2
    assert user.inventory[Piece("3023", "blue")] == 4
    assert user.inventory[Piece("4286", "red")] == 2

@patch.object(ApiDataHandler, "_get_json")
def test_get_all_sets(mock_get_json, api_handler):
    """Test that get_all_sets returns list of Set objects."""
    mock_get_json.side_effect = [
        # Response 1: list of sets
        {"Sets": [{"id": 101, "name": "Tropical Island"}]},
        # Response 2: set by ID
        {
            "id": 101,
            "name": "Tropical Island",
            "totalPieces": 6,
            "pieces": [
                {"part": {"designID": "3023", "material": "blue"}, "quantity": 4},
                {"part": {"designID": "4286", "material": "red"}, "quantity": 2},
            ],
        },
    ]

    sets = api_handler.get_all_sets()
    assert len(sets) == 1
    l_set = sets[0]
    assert isinstance(l_set, Set)
    assert l_set.name == "Tropical Island"
    assert len(l_set.required_pieces) == 2
    assert l_set.required_pieces[Piece("3023", "blue")] == 4
    assert l_set.required_pieces[Piece("4286", "red")] == 2

@patch.object(ApiDataHandler, "_get_json")
def test_get_set_by_set_name(mock_get_json, api_handler):
    """Test that get_set_by_set_name returns a Set object."""
    mock_get_json.side_effect = [
        # Response 1: set summary
        {"id": 101, "name": "Tropical Island", "totalPieces": 6},
        # Response 2: full set details
        {
            "id": 101,
            "name": "Tropical Island",
            "totalPieces": 6,
            "pieces": [
                {"part": {"designID": "3023", "material": "blue"}, "quantity": 4},
                {"part": {"designID": "4286", "material": "red"}, "quantity": 2},
            ],
        },
    ]

    l_set = api_handler.get_set_by_set_name("Tropical Island")
    assert isinstance(l_set, Set)
    assert l_set.name == "Tropical Island"
    assert len(l_set.required_pieces) == 2
    assert l_set.required_pieces[Piece("3023", "blue")] == 4
    assert l_set.required_pieces[Piece("4286", "red")] == 2
