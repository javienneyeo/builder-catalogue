from piece import Piece

class Set:
    def __init__(self, set_id, name, total_pieces, required_pieces):
        self.set_id = set_id
        self.name = name
        self.total_pieces = total_pieces
        self.required_pieces = required_pieces  # list of Piece objects

    def can_build(self, user) -> bool:
        """
        Check if this set can be built with the user's pieces.
        """
        user_inventory_dict = user.get_inventory_summary()
        for piece in self.required_pieces:
            if user_inventory_dict.get((piece.piece_id, piece.color_id), 0) < piece.count:
                return False
        return True
    
    def get_required_pieces_summary(self):
        required_pieces_dict = {}
        for piece in self.required_pieces:
            key = (piece.piece_id, piece.color_id)
            required_pieces_dict[key] = required_pieces_dict.get(key, 0) + piece.count

        return required_pieces_dict
