import copy

from BoardState import BoardState
from Position import Position
from OpponentAI import OpponentAI

def print_board(board):
    print('Current board state:')
    row_text = '  A B C D E F G H'
    print(row_text)

    for i in range(8):
        row = str(i + 1) + ' '
        for j in range(8):
            if board[i][j] is None:
                row += '. '
            else:
                row += board[i][j] + ' '
        print(row)
    print()

def print_available_moves(moves):
    print("Available moves:")
    for move in moves:
        print(move)

def play_pvp():
    board_state = BoardState()

    while not board_state.game_over:
        print_board(board_state.board)

        print(f"{board_state.current_player}'s turn")
        print_available_moves(board_state.available_moves)

        move = input('Input your move e. g. [A 1]\n>')
        pos = move.split(' ')
        position = Position(int(pos[1]) - 1, ord(pos[0]) - ord('A'))
        board_state.make_move(position)

    print('Game over!')
    print_board(board_state.board)
    print(f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')


def play_pve():
    board_state = BoardState()
    opponent = OpponentAI()
    players_turn = True

    while not board_state.game_over:
        print_board(board_state.board)

        print(f"{board_state.current_player}'s turn")
        print_available_moves(board_state.available_moves)

        if players_turn:
            move = input('Input your move e. g. [A 1]\n>')
            pos = move.split(' ')
            position = Position(int(pos[1]) - 1, ord(pos[0]) - ord('A'))
            board_state.make_move(position)
        else:
            board_state.make_move(opponent.get_next_move(copy.deepcopy(board_state)))
        players_turn = not players_turn

    print('Game over!')
    print_board(board_state.board)
    print(
        f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')