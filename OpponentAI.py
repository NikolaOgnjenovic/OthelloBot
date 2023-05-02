import copy

from BoardState import BoardState
from math import inf
import time

class Node:
    def __init__(self, position: int | None):
        self.children = []
        self.value = None
        self.position = position

    def add_child(self, node):
        self.children.append(node)


weights = [20, -3, 11, 8, 8, 11, -3, 20,
               -3, -7, -4, 1, 1, -4, -7, -3,
               11, -4, 2, 2, 2, 2, -4, 11,
               8, 1, 2, -3, -3, 2, 1, 8,
               8, 1, 2, -3, -3, 2, 1, 8,
               11, -4, 2, 2, 2, 2, -4, 11,
               -3, -7, -4, 1, 1, -4, -7, -3,
               20, -3, 11, 8, 8, 11, -3, 20
               ]
x_weights = [-1, -1, 0, 1, 1, 1, 0, -1]
y_weights = [0, 1, 1, 1, 0, -1, -1, -1]

# Piece difference, frontier disks and disk squares
def piece_difference(board: list[str | None], player_color: str, opponent_color: str) -> (float, float):

    player_tiles = 0
    opponent_tiles = 0
    player_front_tiles = 0
    opponent_front_tiles = 0
    d = 0
    for i in range(8):
        for j in range(8):
            if board[i * 8 + j] == player_color:
                d += weights[i * 8 + j]
                player_tiles += 1
            elif board[i * 8 + j] == opponent_color:
                d -= weights[i * 8 + j]
                opponent_tiles += 1

            if board[i * 8 + j] is not None:
                for k in range(8):
                    x = i + x_weights[k]
                    y = j + y_weights[k]
                    if 0 <= x < 8 and 0 <= y < 8 and board[i * 8 + j] is None:
                        if board[i * 8 + j] == player_color:
                            player_front_tiles += 1
                        else:
                            opponent_front_tiles += 1
                        break
    if player_tiles > opponent_tiles:
        p = (100.0 * player_tiles) / (player_tiles + opponent_tiles)
    elif player_tiles < opponent_tiles:
        p = -(100.0 * opponent_tiles) / (player_tiles + opponent_tiles)
    else:
        p = 0

    if player_front_tiles > opponent_front_tiles:
        f = -(100.0 * player_front_tiles) / (player_front_tiles + opponent_front_tiles)
    elif player_front_tiles < opponent_front_tiles:
        f = (100.0 * opponent_front_tiles) / (player_front_tiles + opponent_front_tiles)
    else:
        f = 0

    return p, f, d


def corner_occupancy(board: list[str | None], player_color: str, opponent_color: str) -> float:
    player_tiles = opponent_tiles = 0
    if board[0] == player_color:
        player_tiles += 1
    elif board[0] == opponent_color:
        opponent_tiles += 1

    if board[7] == player_color:
        player_tiles += 1
    elif board[7] == opponent_color:
        opponent_tiles += 1

    if board[21] == player_color:
        player_tiles += 1
    elif board[21] == opponent_color:
        opponent_tiles += 1

    if board[28] == player_color:
        player_tiles += 1
    elif board[28] == opponent_color:
        opponent_tiles += 1

    return 25 * (player_tiles - opponent_tiles)


def corner_closeness(board: list[str | None], player_color: str, opponent_color: str) -> float:
    player_tiles = opponent_tiles = 0
    if board[0] is None:
        if board[1] == player_color:
            player_tiles += 1
        elif board[1] == opponent_color:
            opponent_tiles += 1

        if board[4] == player_color:
            player_tiles += 1
        elif board[4] == opponent_color:
            opponent_tiles += 1

        if board[3] == player_color:
            player_tiles += 1
        elif board[3] == opponent_color:
            opponent_tiles += 1

    if board[7] == '-':
        if board[6] == player_color:
            player_tiles += 1
        elif board[6] == opponent_color:
            opponent_tiles += 1

        if board[9] == player_color:
            player_tiles += 1
        elif board[9] == opponent_color:
            opponent_tiles += 1

        if board[10] == player_color:
            player_tiles += 1
        elif board[10] == opponent_color:
            opponent_tiles += 1

    if board[7] == '-':
        if board[22] == player_color:
            player_tiles += 1
        elif board[22] == opponent_color:
            opponent_tiles += 1

        if board[19] == player_color:
            player_tiles += 1
        elif board[19] == opponent_color:
            opponent_tiles += 1

        if board[18] == player_color:
            player_tiles += 1
        elif board[18] == opponent_color:
            opponent_tiles += 1

    if board[28] == '-':
        if board[25] == player_color:
            player_tiles += 1
        elif board[25] == opponent_color:
            opponent_tiles += 1

        if board[24] == player_color:
            player_tiles += 1
        elif board[24] == opponent_color:
            opponent_tiles += 1

        if board[27] == player_color:
            player_tiles += 1
        elif board[27] == opponent_color:
            opponent_tiles += 1

    return -12.5 * (player_tiles - opponent_tiles)


def mobility(board_state: BoardState, player_color: str, opponent_color: str) -> float:
    player_tiles = len(board_state.get_legal_moves(player_color))
    opponent_tiles = len(board_state.get_legal_moves(opponent_color))

    if player_tiles > opponent_tiles:
        m = (100.0 * player_tiles) / (player_tiles + opponent_tiles)
    elif opponent_tiles < player_tiles:
        m = -(100.0 * opponent_tiles) / (player_tiles + opponent_tiles)
    else:
        m = 0

    return m


def heuristic(board_state: BoardState, player_color: str, opponent_color: str, heuristic_strength: int):
    p = c = l = m = f = d = 0

#if heuristic_strength > 0:
    p, f, d = piece_difference(board_state.board, player_color, opponent_color)
#if heuristic_strength > 1:
    l = corner_closeness(board_state.board, player_color, opponent_color)
# if heuristic_strength > 2:
    m = mobility(board_state, player_color, opponent_color)
#if heuristic_strength > 3:
    c = corner_occupancy(board_state.board, player_color, opponent_color)

    #print(f'p {p} c {c} l {l} m {m} f {f} d {d}')
    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10.0 * d)
    return score


class OpponentAI:
    board_state: BoardState

    state_hash: dict = {} # Hash map of already calculated state branch values (transposition table)
    player: str
    opponent: str
    heuristic_strength: int
    max_depth: int
    end_time: float

    def __init__(self, heuristic_strength: int, player: str):
        self.player = player
        self.opponent = 'B'
        if self.player == 'B':
            self.opponent = 'W'

        self.heuristic_strength = heuristic_strength
        if heuristic_strength == 4:
            self.max_depth = 20
        elif heuristic_strength == 3:
            self.max_depth = 10
        elif heuristic_strength == 2:
            self.max_depth = 5
        else:
            self.max_depth = 3

    def get_next_move(self, board_state: BoardState) -> int | None:
        root = Node(None)

        for move in board_state.available_moves:
            root.add_child(Node(move))

        depth = 4
        end_time = time.time() + 2.9
        self.end_time = end_time
        option = None
        while depth < self.max_depth and time.time() < end_time:
            #print('Depth: ', depth, ' Time - end: ' + str(time.time() - end_time))

            # Minimax each child
            for child in root.children:
                child.value = self.minimax(depth, True, -inf, inf, board_state, child.position)

            if len(root.children) < 1:
                return None

            option = root.children[0]
            for i in range(1, len(root.children)):
                if root.children[i].value > option.value:
                    option = root.children[i]

            depth += 1

        print('Max depth reached: ', depth)
        if option is not None:
            return option.position
        else:
            return None

    def minimax(self, depth: int, is_maximizer: bool, alpha: float, beta: float, state: BoardState, move_position: int) -> float:
        board_state = copy.deepcopy(state)
        board_state.board = copy.deepcopy(board_state.board)
        board_state.make_move(move_position)

        if time.time() > self.end_time or depth < 1 or board_state.game_over:
            return heuristic(board_state, self.player, self.opponent, self.heuristic_strength)

        if is_maximizer:
            for move in board_state.available_moves:
                #hash_value = (board_state.black_discs | board_state.white_discs).__hash__()
                # hash_value = str(move.__hash__()) + str(board_state)
                # if self.state_hash.__contains__(hash_value):
                #     val = self.state_hash.get(hash_value)
                # else:
                #     val = self.minimax(depth - 1, False, alpha, beta, board_state, move)
                #     self.state_hash.update({hash_value: val})
                val = self.minimax(depth - 1, False, alpha, beta, board_state, move)

                alpha = max(alpha, val)
                if alpha >= beta:
                    return beta
            return alpha
        else:
            for move in board_state.available_moves:
                # hash_value = str(move.__hash__()) + str(board_state)
                # if self.state_hash.__contains__(hash_value):
                #     val = self.state_hash.get(hash_value)
                # else:
                #     val = self.minimax(depth - 1, True, alpha, beta, board_state, move)
                #     self.state_hash.update({hash_value: val})
                val = self.minimax(depth - 1, True, alpha, beta, board_state, move)

                beta = min(beta, val)
                if alpha >= beta:
                    return alpha
            return beta