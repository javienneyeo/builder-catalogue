from piece import Piece

class Set:
    def __init__(self, set_id, name, total_pieces, required_pieces):
        self.set_id = set_id
        self.name = name
        self.total_pieces = total_pieces
        self.required_pieces = required_pieces  # dictionary of piece --> quantity

    def __repr__(self):
        return self.name

    def can_build(self, user) -> bool:
        for piece, quantity in self.required_pieces.items():
            if user.inventory.get(piece, 0) < quantity:
                return False
        return True
    
    def buildable_percentage(self, user):
        total_required_pieces = 0
        missing_pieces = 0
        for piece, quantity in self.required_pieces.items():
            total_required_pieces += quantity
            user_quantity = user.inventory.get(piece, 0)
            if user_quantity < quantity:
                missing_pieces += (quantity - user_quantity)
        built_pieces = total_required_pieces - missing_pieces
        return (built_pieces/total_required_pieces) * 100
    
    @staticmethod
    def has_unique_color_assignment(piece_colors, used_colors_by_piece_id=None):
        if used_colors_by_piece_id is None:
            used_colors_by_piece_id = {}
        if not piece_colors:
            return True

        piece_id, colors = next(iter(piece_colors.items()))
        for color in colors:
            if color in used_colors_by_piece_id.values():
                continue

            new_assignments = used_colors_by_piece_id.copy()
            new_assignments[piece_id] = color

            remaining = {k: v for k, v in piece_colors.items() if k != piece_id}
            if Set.has_unique_color_assignment(remaining, new_assignments):
                return True
        return False


    def is_buildable_any_color(self, user_inventory):
        required_pieces_dict = {}
        user_inventory_dict = {}

        for u_piece, quantity in user_inventory.items():
            user_inventory_dict.setdefault(u_piece.piece_id, [])
            user_inventory_dict[u_piece.piece_id].append((u_piece.color_id, quantity))

        for s_piece, s_quantity in self.required_pieces.items():
            piece_id = s_piece.piece_id
            required_pieces_dict.setdefault(piece_id, set())
            if piece_id in user_inventory_dict:
                for user_color, user_quantity in user_inventory_dict[piece_id]:
                    if user_quantity >= s_quantity:
                        required_pieces_dict[piece_id].add(user_color)

        for colors in required_pieces_dict.values():
            if not colors:
                return False
        return Set.has_unique_color_assignment(required_pieces_dict)
    
    

