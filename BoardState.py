def nth_bit_set(number: int, n: int) -> bool:
    return (number & (1 << n)) == 0


def get_opponent(player_color: str):
    if player_color == 'W':
        return 'B'
    if player_color == 'B':
        return 'W'
    return None


def is_inside_board(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


class BoardState(object):
    black_board: int # Black player bitboard (64 * 1)
    white_board: int # White player bitboard (64 * 1)
    black_discs: int
    white_discs: int
    black_turn: bool = True
    game_over: bool = False
    winner: str = None
    available_moves: dict = {} # int (position) -> list[int (positions)]

    def toggle_white_bit(self, n: int):
        self.white_board  = self.white_board ^ (1 << n)
    def toggle_black_bit(self, n: int):
        self.black_board = self.black_board ^ (1 << n)

    def __init__(self):
        self.black_board = 0xFFFFFFFFFFFFFFFF
        self.white_board = 0xFFFFFFFFFFFFFFFF

        self.toggle_white_bit(27)
        self.toggle_black_bit(28)
        self.toggle_black_bit(35)
        self.toggle_white_bit(36)
        self.black_discs = 2
        self.white_discs = 2

        self.available_moves = self.get_legal_moves(self.black_turn)

    def make_move(self, position: int):
        if not self.available_moves.get(position) or position is None:
            return None

        outflanked = self.available_moves[position]

        if self.black_turn:
            self.toggle_black_bit(position)
        else:
            self.toggle_white_bit(position)
        self.flip_discs(outflanked)
        self.update_disc_counts(len(outflanked))
        self.pass_turn()

    def flip_discs(self, positions: list[int]):
        for position in positions:
            self.toggle_white_bit(position)
            self.toggle_black_bit(position)

    def update_disc_counts(self, count: int):
        if count == 0:
            return
        if self.black_turn:
            self.black_discs += count + 1
            self.white_discs -= count
        else:
            self.white_discs += count + 1
            self.black_discs -= count

    def swap_player(self):
        self.black_turn = not self.black_turn
        self.available_moves = self.get_legal_moves(self.black_turn)

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
        if len(self.available_moves) == 0:
            self.game_over = True
            self.winner = self.get_winner()

    def outflanked_in_direction(self, position: int, row_delta: int, column_delta: int, is_black: bool) -> list[int]:
        outflanked = []
        r = position // 8 + row_delta
        c = position % 8 + column_delta

        while is_inside_board(r, c) and (nth_bit_set(self.black_board, r * 8 + c) or nth_bit_set(self.white_board, r * 8 + c)):
            if is_black and nth_bit_set(self.white_board, r * 8 + c):
                    outflanked.append(r * 8 + c)
                    r += row_delta
                    c += column_delta
            elif not is_black and nth_bit_set(self.black_board, r * 8 + c):
                outflanked.append(r * 8 + c)
                r += row_delta
                c += column_delta
            else:
                return outflanked
        return []

    def calculate_outflanked(self, position: int, is_black: bool):
        outflanked = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                outflanked.extend(self.outflanked_in_direction(position, r, c, is_black))

        return outflanked

    def move_is_legal(self, position: int, is_black: bool) -> list[int]:
        if nth_bit_set(self.black_board, position) or nth_bit_set(self.white_board, position):
            return []

        return self.calculate_outflanked(position, is_black)

    def get_legal_moves(self, is_black: bool) -> dict: # -> int -> List[int]
        moves = {}
        for r in range(8):
            for c in range(8):
                position = r * 8 + c
                outflanked = self.move_is_legal(position, is_black)
                if len(outflanked) > 0:
                    moves.update({position: outflanked})

        return moves