from piece import Piece

class Set:
    def __init__(self, set_id, name, total_pieces, required_pieces):
        self.set_id = set_id
        self.name = name
        self.total_pieces = total_pieces
        self.required_pieces = required_pieces  # dictionary of piece --> quantity

    def can_build(self, user) -> bool:
        """
        Check if this set can be built with the user's pieces.
        """
        for piece, quantity in self.required_pieces.items():
            if user.inventory.get(piece, 0) < quantity:
                return False
        return True
