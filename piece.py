class Piece:
    def __init__(self, piece_id: str, color_id: str, count: int):
        self.piece_id = str(piece_id)
        self.color_id = str(color_id)
        self.count = count

    def __repr__(self):
        return f"Piece(id={self.piece_id}, color={self.color_id}, count={self.count})"
