import pytest
from user import User
from set import Set
from piece import Piece

@pytest.fixture
def sample_pieces():
    """Reusable pieces for testing."""
    return {
        Piece("3023", "blue"): 5,
        Piece("4286", "red"): 2,
        Piece("3001", "green"): 3,
    }

@pytest.fixture
def sample_user(sample_pieces):
    """A user with a small inventory."""
    return User(user_id=1, username="brickfan35", brick_count=10, inventory=sample_pieces)

def test_find_missing_pieces(sample_user):
    """Should return pieces that are missing or insufficient."""
    set_pieces = {
        Piece("3023", "blue"): 6,   # needs 1 more
        Piece("4286", "red"): 1,    # has enough
        Piece("3062b", "black"): 2  # completely missing
    }

    missing = sample_user.find_missing_pieces(set_pieces)
    assert len(missing) == 2
    assert missing[Piece("3023", "blue")] == 1
    assert missing[Piece("3062b", "black")] == 2

def test_get_all_pieces(sample_user):
    """Should return all pieces in the inventory."""
    pieces = sample_user.get_all_pieces()
    assert isinstance(pieces, list)
    assert len(pieces) == 3
    assert all(isinstance(p, Piece) for p in pieces)

def test_can_build_set_true(sample_user):
    """Should return True if user has all required pieces."""
    required = {
        Piece("3023", "blue"): 4,
        Piece("4286", "red"): 2,
    }
    assert sample_user.can_build_set(required) is True

def test_can_build_set_false(sample_user):
    """Should return False if any required piece is missing or insufficient."""
    required = {
        Piece("3023", "blue"): 6,  # not enough
        Piece("4286", "red"): 2,
    }
    assert sample_user.can_build_set(required) is False

def test_has_piece(sample_user):
    """Should return True if user has at least the required quantity."""
    piece = Piece("3023", "blue")
    assert sample_user.has_piece(piece, 3) is True
    assert sample_user.has_piece(piece, 6) is False

def test_find_buildable_sets(sample_user):
    """Should return names of sets that can be built."""
    set1 = Set(1, "Small Car", 7, {
        Piece("3023", "blue"): 2,
        Piece("4286", "red"): 1,
    })
    set2 = Set(2, "Big Plane", 10, {
        Piece("3023", "blue"): 6,
        Piece("4286", "red"): 2,
    })
    set3 = Set(3, "Green Garden", 3, {
        Piece("3001", "green"): 3,
    })

    all_sets = [set1, set2, set3]
    buildable = sample_user.find_buildable_sets(all_sets)

    assert set(buildable) == {"Small Car", "Green Garden"}
    assert "Big Plane" not in buildable

def test_find_collaborators():
    """Should identify users who can help complete missing pieces."""
    # Target set requires blue 5 + red 3
    target_set = Set(1, "Mini Ship", 8, {
        Piece("3023", "blue"): 5,
        Piece("4286", "red"): 3,
    })

    # Main user: has 3 blue, 1 red (missing 2 blue, 2 red)
    user_main = User(1, "builderA", 4, {
        Piece("3023", "blue"): 3,
        Piece("4286", "red"): 1,
    })

    user1 = User(2, "helper1", 5, {Piece("3023", "blue"): 5})  # can help with blue
    user2 = User(3, "helper2", 5, {Piece("4286", "red"): 3})   # can help with red
    user3 = User(4, "random", 3, {Piece("3001", "green"): 2})  # irrelevant

    collaborators = user_main.find_collaborators(target_set, [user1, user2, user3, user_main])

    assert set(collaborators) == {"helper1", "helper2"}
