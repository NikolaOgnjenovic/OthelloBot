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


# Piece difference, frontier disks and disk squares
def piece_difference(board: list[list], player_color: str, opponent_color: str) -> (float, float):
    weights = [[20, -3, 11, 8, 8, 11, -3, 20],
               [-3, -7, -4, 1, 1, -4, -7, -3],
               [11, -4, 2, 2, 2, 2, -4, 11],
               [8, 1, 2, -3, -3, 2, 1, 8],
               [8, 1, 2, -3, -3, 2, 1, 8],
               [11, -4, 2, 2, 2, 2, -4, 11],
               [-3, -7, -4, 1, 1, -4, -7, -3],
               [20, -3, 11, 8, 8, 11, -3, 20]
               ]
    x_weights = [-1, -1, 0, 1, 1, 1, 0, -1]
    y_weights = [0, 1, 1, 1, 0, -1, -1, -1]
    player_tiles = 0
    opponent_tiles = 0
    player_front_tiles = 0
    opponent_front_tiles = 0
    result = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player_color:
                result += weights[i][j]
                player_tiles += 1
            elif board[i][j] == opponent_color:
                result -= weights[i][j]
                opponent_tiles += 1

            if board[i][j] is not None:
                for k in range(8):
                    x = i + x_weights[k]
                    y = j + y_weights[k]
                    if 0 <= x < 8 and 0 <= y < 8 and board[i][j] is None:
                        if board[i][j] == player_color:
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


def corner_occupancy(board: list[list], player_color: str, opponent_color: str) -> float:
    player_tiles = opponent_tiles = 0
    if board[0][0] == player_color:
        player_tiles += 1
    elif board[0][0] == opponent_color:
        opponent_tiles += 1

    if board[0][7] == player_color:
        player_tiles += 1
    elif board[0][7] == opponent_color:
        opponent_tiles += 1

    if board[7][0] == player_color:
        player_tiles += 1
    elif board[7][0] == opponent_color:
        opponent_tiles += 1

    if board[7][7] == player_color:
        player_tiles += 1
    elif board[7][7] == opponent_color:
        opponent_tiles += 1

    return 25 * (player_tiles - opponent_tiles)


def corner_closeness(board: list[list], player_color: str, opponent_color: str) -> float:
    player_tiles = opponent_tiles = 0
    if board[0][0] is None:
        if board[0][1] == player_color:
            player_tiles += 1
        elif board[0][1] == opponent_color:
            opponent_tiles += 1

        if board[1][1] == player_color:
            player_tiles += 1
        elif board[1][1] == opponent_color:
            opponent_tiles += 1

        if board[1][0] == player_color:
            player_tiles += 1
        elif board[1][0] == opponent_color:
            opponent_tiles += 1

    if board[0][7] == '-':
        if board[0][6] == player_color:
            player_tiles += 1
        elif board[0][6] == opponent_color:
            opponent_tiles += 1

        if board[1][6] == player_color:
            player_tiles += 1
        elif board[1][6] == opponent_color:
            opponent_tiles += 1

        if board[1][7] == player_color:
            player_tiles += 1
        elif board[1][7] == opponent_color:
            opponent_tiles += 1

    if board[7][0] == '-':
        if board[7][1] == player_color:
            player_tiles += 1
        elif board[7][1] == opponent_color:
            opponent_tiles += 1

        if board[6][1] == player_color:
            player_tiles += 1
        elif board[6][1] == opponent_color:
            opponent_tiles += 1

        if board[6][0] == player_color:
            player_tiles += 1
        elif board[6][0] == opponent_color:
            opponent_tiles += 1

    if board[7][7] == '-':
        if board[6][7] == player_color:
            player_tiles += 1
        elif board[6][7] == opponent_color:
            opponent_tiles += 1

        if board[6][6] == player_color:
            player_tiles += 1
        elif board[6][6] == opponent_color:
            opponent_tiles += 1

        if board[7][6] == player_color:
            player_tiles += 1
        elif board[7][6] == opponent_color:
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


class OpponentAI:
    board_state: BoardState

    def get_next_move(self, board_state: BoardState) -> Position:
        root = Node(None)

        for move in board_state.available_moves:
            root.add_child(Node(move))

        # Minimax each child
        for child in root.children:
            child.value = self.minimax(3, True, board_state)

        # Get the best option
        best_option = root.children[0]
        for child in root.children:
            if child.value > best_option.value:
                best_option = child

        return best_option.position

    def minimax(self, depth: int, is_maximizer: bool, board_state: BoardState):
        if depth == 0 or board_state.game_over:
            if is_maximizer:
                return heuristic(board_state, 'W', 'B')
            else:
                return heuristic(board_state, 'B', 'W')

        if is_maximizer:
            max_val = -inf
            for move in board_state.available_moves:
                val = self.minimax(depth - 1, False, board_state)
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = inf
            for move in board_state.available_moves:
                val = self.minimax(depth - 1, True, board_state)
                min_val = min(min_val, val)
            return min_val