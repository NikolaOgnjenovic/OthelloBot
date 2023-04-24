import copy

from Position import Position
from BoardState import BoardState
from math import inf

class Node:
    def __init__(self, position: Position | None):
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
    result = 0
    for i in range(8):
        for j in range(8):
            if board[i * 8 + j] == player_color:
                result += weights[i * 8 + j]
                player_tiles += 1
            elif board[i * 8 + j] == opponent_color:
                result -= weights[i * 8 + j]
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

    return p, f


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


def heuristic(board_state: BoardState, player_color: str, opponent_color: str):
    p, f = piece_difference(board_state.board, player_color, opponent_color)
    c = corner_occupancy(board_state.board, player_color, opponent_color)
    l = corner_closeness(board_state.board, player_color, opponent_color)
    m = mobility(board_state, player_color, opponent_color)

    score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f)
    return score


# TODO: think of a better hashing algorithm
def hash_board(board: list[str | None]):
    return str(board)

class OpponentAI:
    board_state: BoardState

    state_hash: dict = {} # Hash map of already calculated state branch values (transposition table)

    def get_next_move(self, board_state: BoardState) -> Position:
        root = Node(None)

        for move in board_state.available_moves:
            root.add_child(Node(move))

        # Minimax each child
        for child in root.children:
            child.value = self.minimax(10, True, -inf, inf, board_state, child.position)

        # Get the best option
        best_option = root.children[0]
        for child in root.children:
            if child.value > best_option.value:
                best_option = child

        return best_option.position

    def minimax(self, depth: int, is_maximizer: bool, alpha: float, beta: float, state: BoardState, child_position: Position) -> float:
        board_state = copy.deepcopy(state)
        board_state.board = copy.deepcopy(board_state.board)
        board_state.make_move(child_position)

        if depth < 1 or board_state.game_over:
            if is_maximizer:
                return heuristic(board_state, 'W', 'B')
            else:
                return heuristic(board_state, 'B', 'W')

        if is_maximizer:
            max_val = -inf
            for move in board_state.available_moves:
                if self.state_hash.__contains__(board_state.board.__hash__):
                    val = self.state_hash.get(board_state.board.__hash__)
                    print('ALREADY CALCULATED')
                else:
                    val = self.minimax(depth - 1, False, alpha, beta, board_state, move)
                    self.state_hash.update({board_state.board.__hash__: val})
                #val = self.minimax(depth - 1, False, alpha, beta, board_state, move)

                max_val = max(max_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_val
        else:
            min_val = inf
            for move in board_state.available_moves:
                if self.state_hash.__contains__(board_state.board.__hash__):
                    val = self.state_hash.get(board_state.board.__hash__)
                    print('ALREADY CALCULATED')
                else:
                    val = self.minimax(depth - 1, True, alpha, beta, board_state, move)
                    self.state_hash.update({board_state.board.__hash__: val})
                #val = self.minimax(depth - 1, True, alpha, beta, board_state, move)

                min_val = min(min_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_val