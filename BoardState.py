from Position import Position
from MoveInfo import MoveInfo


def get_opponent(player_color: str):
    if player_color == 'W':
        return 'B'
    if player_color == 'B':
        return 'W'
    return None


class BoardState:
    ROWS = 8
    COLUMNS = 8

    board: [list[list[str]]] = []
    black_discs: int = 0
    white_discs: int = 0
    current_player : str | None = None
    game_over: bool = False
    winner: str = None
    available_moves: dict = {} # Position -> list[Position]

    def __init__(self):
        for i in range(self.ROWS):
            row = []
            for j in range(self.COLUMNS):
                row.append(None)
            self.board.append(row)

        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.black_discs = 2
        self.white_discs = 2

        self.current_player = 'B'
        self.available_moves = self.get_legal_moves(self.current_player)

    def make_move(self, position: Position) -> MoveInfo | None:
        if not self.available_moves.get(position):
            return None

        move_player = self.current_player
        outflanked = self.available_moves[position]

        self.board[position.row][position.column] = move_player
        self.flip_discs(outflanked)
        self.update_disc_counts(self.current_player, len(outflanked))
        self.pass_turn()

        return MoveInfo(move_player, position, outflanked)


    def flip_discs(self, positions: list[Position]):
        for position in positions:
            self.board[position.row][position.column] = get_opponent(self.board[position.row][position.column])

    def update_disc_counts(self, player_color: str, count: int):
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

    def is_inside_board(self, r: int, c: int):
        return 0 <= r < self.ROWS and 0 <= c < self.COLUMNS

    def outflanked_in_direction(self, position: Position, player_color: str, row_delta: int, column_delta: int) -> list[Position]:
        outflanked = []
        r = position.row + row_delta
        c = position.column + column_delta

        while self.is_inside_board(r, c) and self.board[r][c] is not None:
            if self.board[r][c] == get_opponent(player_color):
                outflanked.append(Position(r, c))
                r += row_delta
                c += column_delta
            else:
                return outflanked
        return []

    def calculate_outflanked(self, position: Position, player_color: str):
        outflanked = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                outflanked.extend(self.outflanked_in_direction(position, player_color, r, c))

        return outflanked

    def move_is_legal(self, position: Position, player_color: str) -> list[Position]:
        if self.board[position.row][position.column] is not None:
            return []
        return self.calculate_outflanked(position, player_color)

    def get_legal_moves(self, player_color: str) -> dict: # -> Position -> List[Position]
        moves = {}
        for r in range(8):
            for c in range(8):
                position = Position(r, c)
                outflanked = self.move_is_legal(position, player_color)
                if len(outflanked) > 0:
                    moves.update({position: outflanked})

        return moves