import pytest
from set import Set
from piece import Piece


@pytest.fixture
def simple_set():
    required = {
        Piece("3023", "blue"): 2,
        Piece("3001", "red"): 1,
    }
    return Set(1, "SimpleSet", 3, required)


@pytest.fixture
def simple_user_inventory():
    return {
        Piece("3023", "blue"): 2,
        Piece("3001", "red"): 1,
    }


def test_repr(simple_set):
    assert repr(simple_set) == "SimpleSet"


def test_can_build_true(simple_set, simple_user_inventory):
    class User:
        inventory = simple_user_inventory
    assert simple_set.can_build(User()) is True


def test_can_build_false(simple_set):
    class User:
        inventory = {
            Piece("3023", "blue"): 1,  # not enough
            Piece("3001", "red"): 1,
        }
    assert simple_set.can_build(User()) is False


def test_buildable_percentage_100(simple_set, simple_user_inventory):
    class User:
        inventory = simple_user_inventory
    assert simple_set.buildable_percentage(User()) == 100.0


def test_buildable_percentage_partial(simple_set):
    class User:
        inventory = {
            Piece("3023", "blue"): 1,  # missing 1
            Piece("3001", "red"): 1,
        }
    # total = 3, built = 2 → 66.666%
    assert simple_set.buildable_percentage(User()) == pytest.approx(66.666, rel=0.01)


def test_required_pieces_without_color(simple_set):
    result = simple_set.required_pieces_without_color()
    assert result == {
        "3023": 2,
        "3001": 1,
    }


def test_unique_assignment_simple_true():
    piece_colors = {
        "3023": {"blue", "red"},
        "3001": {"yellow"},
    }
    assert Set.has_unique_color_assignment(piece_colors) is True


def test_unique_assignment_same_piece_id_reuse():
    piece_colors = {
        "3023": {"blue"},
    }
    assert Set.has_unique_color_assignment(piece_colors) is True


def test_unique_assignment_conflict_false():
    piece_colors = {
        "3023": {"blue"},
        "3001": {"blue"},  # conflict
    }
    assert Set.has_unique_color_assignment(piece_colors) is False


def test_unique_assignment_complex_valid():
    piece_colors = {
        "3023": {"blue", "red"},
        "3001": {"red", "green"}
    }
    assert Set.has_unique_color_assignment(piece_colors) is True


def test_unique_assignment_empty():
    assert Set.has_unique_color_assignment({}) is True


def test_is_buildable_any_color_true():
    required = {
        Piece("3023", "blue"): 1,
        Piece("3001", "red"): 1,
    }
    s = Set(10, "ColorSet", 2, required)

    user_inventory = {
        Piece("3023", "yellow"): 5,  # blue -> yellow
        Piece("3001", "green"): 5,   # red  -> green
    }

    assert s.is_buildable_any_color(user_inventory) is True


def test_is_buildable_any_color_quantity_too_low():
    required = {
        Piece("3023", "blue"): 4,
    }
    s = Set(10, "ColorSet", 4, required)

    user_inventory = {
        Piece("3023", "yellow"): 3,  # not enough quantity
    }

    assert s.is_buildable_any_color(user_inventory) is False


def test_is_buildable_any_color_conflict():
    required = {
        Piece("3023", "blue"): 1,
        Piece("3001", "red"): 1,
    }
    s = Set(10, "ConflictSet", 2, required)

    user_inventory = {
        Piece("3023", "yellow"): 5,
        Piece("3001", "yellow"): 5,  # conflict: both map to yellow
    }

    assert s.is_buildable_any_color(user_inventory) is False


def test_is_buildable_any_color_reuse_same_piece_id():
    required = {
        Piece("3023", "blue"): 2,
    }
    s = Set(10, "ReuseSet", 2, required)

    user_inventory = {
        Piece("3023", "yellow"): 10,  # same piece_id → same color allowed
    }

    assert s.is_buildable_any_color(user_inventory) is True


def test_is_buildable_any_color_complex_valid():
    required = {
        Piece("3023", "blue"): 1,
        Piece("3001", "red"): 1,
        Piece("2456", "green"): 1,
    }
    s = Set(10, "ComplexSet", 3, required)

    user_inventory = {
        Piece("3023", "yellow"): 5,
        Piece("3001", "blue"): 5,
        Piece("2456", "red"): 5,
    }

    # Valid mapping:
    # blue  -> yellow
    # red   -> blue
    # green -> red
    assert s.is_buildable_any_color(user_inventory) is True
