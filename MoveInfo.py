import Position


class MoveInfo:
    def __init__(self, player_color: str, position: Position, outflanked: list[Position]):
        self.player_color = player_color
        self.position = position
        self.outflanked = outflanked
