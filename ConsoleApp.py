from BoardState import BoardState
from Position import Position

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

def play():
    board_state = BoardState()

    while board_state.winner is None:
        print_board(board_state.board)

        print(f"{board_state.current_player}'s turn")
        print_available_moves(board_state.available_moves)

        move = input('Input your move e. g. [1 A]\n>')
        pos = move.split(' ')
        position = Position(int(pos[0]) - 1, ord(pos[1]) - ord('A'))
        board_state.make_move(position)

        if len(board_state.available_moves) < 1:
            if board_state.game_over:
                print('Game over!')
                print(f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
                break

    print('Thank you for playing!')