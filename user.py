from piece import Piece

class User:
    def __init__(self, user_id, username, brick_count, inventory):
        self.user_id = user_id
        self.username = username
        self.brick_count = brick_count
        self.inventory = inventory  # dictionary of piece --> quantity

    def find_missing_pieces(self, set_pieces_dict):
        missing_pieces = {}
        for piece, set_quantity in set_pieces_dict.items():
            user_quantity = self.inventory.get(piece, 0)
            if user_quantity < set_quantity:
                missing_pieces[piece] = set_quantity - user_quantity
        return missing_pieces
    
    def get_all_pieces(self):
        return list(self.inventory.keys())
    
    def can_build_set(self, pieces_dict):
        for piece, required_quantity in pieces_dict.items():
            if self.inventory.get(piece, 0) < required_quantity:
                return False
        return True
    
    def has_piece(self, piece, quantity):
        return self.inventory.get(piece, 0) >= quantity
    
    def find_buildable_sets(self, all_sets):
        buildable_sets = []  
        for s in all_sets: 
            if s.can_build(self):  
                buildable_sets.append(s.name)  
        return buildable_sets
    
    def find_collaborators(self, target_set, all_users):
        missing_pieces = self.find_missing_pieces(target_set.required_pieces)
        if not missing_pieces:
            return []
        
        collaborators = []
        for u in all_users:
            if u.username == self.username:
                continue
            
            remaining_missing_pieces = u.find_missing_pieces(missing_pieces)
            if len(remaining_missing_pieces) < len(missing_pieces):
                collaborators.append(u.username)
                missing_pieces = remaining_missing_pieces

        if not missing_pieces:
            return collaborators
        return []

    