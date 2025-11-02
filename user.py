from piece import Piece

class User:
    def __init__(self, user_id, username, brick_count, inventory):
        self.user_id = user_id
        self.username = username
        self.brick_count = brick_count
        self.inventory = inventory  # list of Piece objects

    def get_inventory_summary(self):
        """
        Returns a dictionary of piece_id, color to quantity for quick lookup
        """
        summary = {}
        for piece in self.inventory:
            key = (piece.piece_id, piece.color_id)
            summary[key] = summary.get(key, 0) + piece.count
        return summary

    def find_missing_pieces(self, inventory_dict, set_pieces_dict):
        missing_pieces = {}
        for piece, set_quantity in set_pieces_dict.items():
            user_quantity = inventory_dict.get(piece, 0)
            if user_quantity < set_quantity:
                missing_pieces[piece] = set_quantity - user_quantity
        return missing_pieces
    
    def get_all_pieces(self):
        all_pieces = []
        for piece in self.inventory:
            key = (piece.piece_id, piece.color_id)
            all_pieces.append(key)
        return all_pieces
    
    def can_build_set(self, pieces_dict):
        user_inventory_dict = self.get_inventory_summary()
        for piece, required_quantity in pieces_dict.items():
            if user_inventory_dict.get(piece, 0) < required_quantity:
                return False
        return True

    