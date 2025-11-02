import pytest
from user import User
from piece import Piece

@pytest.fixture
def sample_user():
    """Create a user with a few sample pieces in inventory."""
    p1 = Piece("3023", "blue", 4)
    p2 = Piece("4286", "red", 2)
    inventory = [p1, p2]
    return User(user_id=1, username="brickfan35", brick_count=6, inventory=inventory)

def test_get_inventory_summary(sample_user):
    summary = sample_user.get_inventory_summary()
    expected = {("3023", "blue"): 4, ("4286", "red"): 2}
    assert summary == expected, f"Expected {expected}, got {summary}"

def test_find_missing_pieces(sample_user):
    inventory_dict = sample_user.get_inventory_summary()
    set_pieces_dict = {("3023", "blue"): 4, ("4286", "red"): 3}
    missing = sample_user.find_missing_pieces(inventory_dict, set_pieces_dict)
    expected = {("4286", "red"): 1}
    assert missing == expected, f"Expected {expected}, got {missing}"

def test_get_all_pieces(sample_user):
    all_pieces = sample_user.get_all_pieces()
    expected = [("3023", "blue"), ("4286", "red")]
    assert all_pieces == expected, f"Expected {expected}, got {all_pieces}"

def test_can_build_set_true(sample_user):
    pieces_dict = {("3023", "blue"): 4, ("4286", "red"): 2}
    assert sample_user.can_build_set(pieces_dict) is True

def test_can_build_set_false(sample_user):
    pieces_dict = {("3023", "blue"): 5}  # user only has 4
    assert sample_user.can_build_set(pieces_dict) is False

def test_empty_inventory():
    empty_user = User(2, "emptyuser", 0, [])
    pieces_dict = {("3023", "blue"): 1}
    assert empty_user.can_build_set(pieces_dict) is False
