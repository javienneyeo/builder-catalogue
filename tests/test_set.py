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

def test_buildable_any_color_true_with_unique_colors():
    """User can build set when each piece has at least one unique color option."""
    pieces_needed = {
        Piece("3001", "red"): 1,
        Piece("3002", "blue"): 1,
        Piece("3003", "green"): 1
    }
    set_obj = Set(201, "Rainbow Car", 3, pieces_needed)

    user_inventory = {
        Piece("3001", "yellow"): 2,
        Piece("3002", "purple"): 1,
        Piece("3003", "orange"): 1
    }
    user = MockUser(user_inventory)

    assert set_obj.is_buildable_any_color(user.inventory) is True


def test_buildable_any_color_false_with_color_conflicts():
    """User has pieces but all share the same color, violating uniqueness."""
    pieces_needed = {
        Piece("3001", "red"): 1,
        Piece("3002", "blue"): 1,
        Piece("3003", "green"): 1
    }
    set_obj = Set(202, "Monochrome House", 3, pieces_needed)

    user_inventory = {
        Piece("3001", "black"): 2,
        Piece("3002", "black"): 2,
        Piece("3003", "black"): 2
    }
    user = MockUser(user_inventory)

    assert set_obj.is_buildable_any_color(user.inventory) is False


def test_buildable_any_color_false_with_insufficient_quantity():
    """User lacks sufficient quantity for a required piece, even with color flexibility."""
    pieces_needed = {
        Piece("3001", "red"): 2,
        Piece("3002", "blue"): 1
    }
    set_obj = Set(203, "Short Supply", 3, pieces_needed)

    user_inventory = {
        Piece("3001", "yellow"): 1,  # not enough
        Piece("3002", "green"): 2
    }
    user = MockUser(user_inventory)

    assert set_obj.is_buildable_any_color(user.inventory) is False

def test_buildable_any_color_partial_overlap():
    """
    User has overlapping color options:
      piece 1: ['1']
      piece 2: ['2', '3']
      piece 3: ['1', '2']
    Expected: True (e.g., assign 1→piece1, 3→piece2, 2→piece3)
    """
    pieces_needed = {
        Piece("p1", "red"): 1,
        Piece("p2", "blue"): 1,
        Piece("p3", "green"): 1
    }
    set_obj = Set(204, "Overlap Color Set", 3, pieces_needed)

    user_inventory = {
        Piece("p1", "1"): 1,       # only color '1'
        Piece("p2", "3"): 1,
        Piece("p2", "2"): 1,       # two options for p2
        Piece("p3", "1"): 1,
        Piece("p3", "2"): 1        # two options for p3
    }
    user = MockUser(user_inventory)

    assert set_obj.is_buildable_any_color(user.inventory) is True

def test_is_buildable_any_color_true_simple():
    # --- User inventory ---
    user_inventory = {
        Piece("p1", "red"): 2,
        Piece("p2", "blue"): 1,
        Piece("p2", "green"): 3,
        Piece("p3", "yellow"): 1,
        Piece("p3", "red"): 2,
    }

    # --- Required pieces ---
    required_pieces = {
        Piece("p1", "red"): 1,
        Piece("p2", "green"): 1,
        Piece("p3", "yellow"): 1,
    }

    lego_set = Set(1, "Color Flex Test", 3, required_pieces)

    # should return True (has enough of all, colors don't clash)
    assert lego_set.is_buildable_any_color(user_inventory) is True

def test_is_buildable_any_color_false_conflict():
    user_inventory = {
        Piece("p1", "red"): 1,
        Piece("p2", "red"): 1,
    }

    required_pieces = {
        Piece("p1", "blue"): 1,
        Piece("p2", "yellow"): 1,
    }

    lego_set = Set(3, "Conflict Test", 2, required_pieces)

    # Both pieces only have "red" available → cannot assign unique colors
    assert lego_set.is_buildable_any_color(user_inventory) is False


def test_is_buildable_any_color_false_missing_piece():
    user_inventory = {
        Piece("p1", "red"): 1,
        Piece("p2", "blue"): 1,
    }

    required_pieces = {
        Piece("p1", "red"): 1,
        Piece("p2", "blue"): 1,
        Piece("p3", "green"): 1,  # user doesn't have piece3
    }

    lego_set = Set(4, "Missing Piece Test", 3, required_pieces)

    # Missing one piece entirely
    assert lego_set.is_buildable_any_color(user_inventory) is False
