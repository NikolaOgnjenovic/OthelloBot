def get_opponent(player_color: str):
    if player_color == 'W':
        return 'B'
    if player_color == 'B':
        return 'W'
    return None

def is_inside_board(r: int, c: int):
    return 0 <= r < 8 and 0 <= c < 8


class BoardState(object):
    board: list[str | None] = [] # index = board[row * 8 + j]
    black_discs: int = 0
    white_discs: int = 0
    current_player : str | None = None
    game_over: bool = False
    winner: str = None
    available_moves: dict = {} # int (position) -> list[int (positions)]

    def __init__(self):
        for i in range(8):
            for j in range(8):
                self.board.append(None)

        self.board[27] = 'W'
        self.board[28] = 'B'
        self.board[35] = 'B'
        self.board[36] = 'W'
        self.black_discs = 2
        self.white_discs = 2

        self.current_player = 'B'
        self.available_moves = self.get_legal_moves(self.current_player)

    def make_move(self, position: int):
        if not self.available_moves.get(position) or position is None:
            return None

        move_player = self.current_player
        outflanked = self.available_moves[position]

        self.board[position] = move_player
        self.flip_discs(outflanked)
        self.update_disc_counts(self.current_player, len(outflanked))
        self.pass_turn()

    def flip_discs(self, positions: list[int]):
        for position in positions:
            self.board[position] = get_opponent(self.board[position])

    def update_disc_counts(self, player_color: str, count: int):
        if count == 0:
            return
        if player_color == "B":
            self.black_discs += count + 1
            self.white_discs -= count
        elif player_color == "W":
            self.white_discs += count + 1
            self.black_discs -= count

    def swap_player(self):
        self.current_player = get_opponent(self.current_player)
        self.available_moves = self.get_legal_moves(self.current_player)

    def get_winner(self) -> str | None:
        if self.black_discs > self.white_discs:
            return "B"
        elif self.white_discs > self.black_discs:
            return "W"
        return None

    def pass_turn(self):
        self.swap_player()
        if len(self.available_moves) > 0:
            return

        self.swap_player()
        if len(self.available_moves) < 1:
            self.current_player = None
            self.game_over = True
            self.winner = self.get_winner()

    def outflanked_in_direction(self, position: int, player_color: str, row_delta: int, column_delta: int) -> list[int]:
        outflanked = []
        r = position // 8 + row_delta
        c = position % 8 + column_delta

        while is_inside_board(r, c) and self.board[r * 8 + c] is not None:
            if self.board[r * 8 + c] == get_opponent(player_color):
                outflanked.append(r * 8 + c)
                r += row_delta
                c += column_delta
            else:
                return outflanked
        return []

    def calculate_outflanked(self, position: int, player_color: str):
        outflanked = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                outflanked.extend(self.outflanked_in_direction(position, player_color, r, c))

        return outflanked

    def move_is_legal(self, position: int, player_color: str) -> list[int]:
        if self.board[position] is not None:
            return []
        return self.calculate_outflanked(position, player_color)

    def get_legal_moves(self, player_color: str) -> dict: # -> int -> List[int]
        moves = {}
        for r in range(8):
            for c in range(8):
                position = r * 8 + c
                outflanked = self.move_is_legal(position, player_color)
                if len(outflanked) > 0:
                    moves.update({position: outflanked})

        return moves