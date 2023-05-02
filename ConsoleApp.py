from BoardState import BoardState
from OpponentAI import OpponentAI
import time

def print_board(board: list[str | None], moves: dict):
    print('W - white, B - black, X - available move position')
    print('Current board state:')
    row_text = '  A B C D E F G H'
    print(row_text)

    for i in range(8):
        row = str(i + 1) + ' '
        for j in range(8):
            if moves.__contains__(i * 8 + j):
                row += 'X '
            elif board[i * 8 + j] is None:
                row += '. '
            else:
                row += board[i * 8 + j] + ' '
        print(row)
    print()

def print_available_moves(moves):
    print('Available moves:')
    for move in moves:
        print(chr(move % 8 + ord('A')) + ' ' + str(move // 8 + 1))

def play_pvp():
    board_state = BoardState()

    while not board_state.game_over:
        print_board(board_state.board, board_state.available_moves)

        print(f"{board_state.current_player}'s turn")
        print_available_moves(board_state.available_moves)

        move = input('Input your move e. g. [A 1]\n>')
        pos = move.split(' ')
        position = (int(pos[1]) - 1) * 8 + (ord(pos[0]) - ord('A'))
        board_state.make_move(position)

    print('Game over!')
    print_board(board_state.board, {})
    print(f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')


def play_ai_vs_ai():
    board_state = BoardState()
    blackAI = OpponentAI(4, 'B')
    whiteAI = OpponentAI(4, 'W')
    black_turn = True

    print('Playing...')
    while not board_state.game_over:
        print(f"{board_state.current_player}'s turn")
        print_available_moves(board_state.available_moves)

        start = time.time()
        if black_turn:
            position = blackAI.get_next_move(board_state)
        else:
            position = whiteAI.get_next_move(board_state)
        end = time.time()

        print(f'{board_state.current_player} AI played {position}')
        print(f'Elapsed time: {end - start}\n')
        board_state.make_move(position)
        black_turn = not black_turn

    print('Game over!')
    print_board(board_state.board, {})
    print(
        f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')

def play_pve():
    board_state = BoardState()
    opponent = OpponentAI(4, 'W')
    players_turn = True

    while not board_state.game_over:
        print_board(board_state.board, board_state.available_moves)

        print(f"{board_state.current_player}'s turn")
        print_available_moves(board_state.available_moves)

        if players_turn:
            move = input('Input your move e. g. [A 1]\n>>')
            pos = move.split(' ')
            position = (int(pos[1]) - 1) * 8 + (ord(pos[0]) - ord('A'))
            board_state.make_move(position)
        else:
            start = time.time()
            position = opponent.get_next_move(board_state)
            end = time.time()

            print(f'AI played {chr(position % 8 + ord("A"))} {str(position // 8 + 1)}')
            print(f'Elapsed time (pruning): {end - start}')

            board_state.make_move(position)
        players_turn = not players_turn

    print('Game over!')
    print_board(board_state.board, {})
    print(
        f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')