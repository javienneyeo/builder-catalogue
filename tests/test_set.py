import pytest
from piece import Piece
from user import User
from set import Set

@pytest.fixture
def sample_user():
    """Create a sample user with a few pieces in inventory."""
    p1 = Piece("3023", "blue", 4)
    p2 = Piece("4286", "red", 2)
    inventory = [p1, p2]
    return User(user_id=1, username="brickfan35", brick_count=6, inventory=inventory)

@pytest.fixture
def sample_set():
    """Create a sample LEGO set with required pieces."""
    r1 = Piece("3023", "blue", 4)
    r2 = Piece("4286", "red", 2)
    required = [r1, r2]
    return Set(set_id=1001, name="tropical-island", total_pieces=6, required_pieces=required)

@pytest.fixture
def partial_set():
    """Create a set that requires more pieces than the user has."""
    r1 = Piece("3023", "blue", 5)
    r2 = Piece("4286", "red", 2)
    required = [r1, r2]
    return Set(set_id=1002, name="desert-house", total_pieces=7, required_pieces=required)

def test_get_required_pieces_summary(sample_set):
    summary = sample_set.get_required_pieces_summary()
    expected = {("3023", "blue"): 4, ("4286", "red"): 2}
    assert summary == expected, f"Expected {expected}, got {summary}"

def test_can_build_true(sample_user, sample_set):
    assert sample_set.can_build(sample_user) is True, "User should be able to build this set."

def test_can_build_false(sample_user, partial_set):
    assert partial_set.can_build(sample_user) is False, "User should NOT be able to build this set."

def test_can_build_with_empty_user_inventory():
    """Edge case: user with no pieces"""
    empty_user = User(user_id=2, username="empty", brick_count=0, inventory=[])
    required_piece = Piece("3023", "blue", 1)
    s = Set(set_id=1003, name="mini-build", total_pieces=1, required_pieces=[required_piece])
    assert s.can_build(empty_user) is False, "Empty user cannot build any set."
