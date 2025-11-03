class Piece:
    def __init__(self, piece_id: str, color_id: str):
        self.piece_id = str(piece_id)
        self.color_id = str(color_id)

    def __eq__(self, other):
        return (self.piece_id, self.color_id) == (other.piece_id, other.color_id)

    def __hash__(self):
        return hash((self.piece_id, self.color_id))

    def __repr__(self):
        return f"Piece({self.piece_id}, {self.color_id})"
