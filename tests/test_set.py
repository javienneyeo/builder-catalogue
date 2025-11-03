import pytest
from set import Set
from piece import Piece

class MockUser:
    def __init__(self, inventory):
        # inventory is a dict of Piece -> quantity
        self.inventory = inventory

def test_can_build_true_when_user_has_all_pieces():
    """User has all required pieces in sufficient quantities."""
    pieces_needed = {
        Piece("3023", "blue"): 2,
        Piece("4286", "red"): 1,
    }
    set_obj = Set(101, "Mini Car", 3, pieces_needed)

    user_inventory = {
        Piece("3023", "blue"): 3,  # has more than needed
        Piece("4286", "red"): 1,
        Piece("3001", "green"): 5,  # irrelevant extra piece
    }
    user = MockUser(user_inventory)

    assert set_obj.can_build(user) is True

def test_can_build_false_when_missing_piece():
    """User missing one required piece."""
    pieces_needed = {
        Piece("3023", "blue"): 2,
        Piece("4286", "red"): 1,
    }
    set_obj = Set(101, "Mini Car", 3, pieces_needed)

    user_inventory = {
        Piece("3023", "blue"): 2,
        # Missing the red one
    }
    user = MockUser(user_inventory)

    assert set_obj.can_build(user) is False

def test_can_build_false_when_not_enough_quantity():
    """User has the piece but not enough quantity."""
    pieces_needed = {
        Piece("3023", "blue"): 4,
        Piece("4286", "red"): 2,
    }
    set_obj = Set(101, "Mini Car", 6, pieces_needed)

    user_inventory = {
        Piece("3023", "blue"): 3,  # less than needed
        Piece("4286", "red"): 2,
    }
    user = MockUser(user_inventory)

    assert set_obj.can_build(user) is False

def test_can_build_true_with_empty_required_pieces():
    """If no pieces are required, user should always be able to build."""
    set_obj = Set(102, "Empty Set", 0, {})
    user = MockUser({})  # Empty inventory
    assert set_obj.can_build(user) is True

def test_can_build_false_with_empty_user_inventory():
    """User cannot build if they have no pieces but the set requires some."""
    pieces_needed = {
        Piece("3023", "blue"): 1,
    }
    set_obj = Set(103, "Simple Build", 1, pieces_needed)
    user = MockUser({})
    assert set_obj.can_build(user) is False
