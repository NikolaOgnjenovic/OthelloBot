from BoardState import BoardState
from OpponentAI import OpponentAI
import time


def nth_bit_set(number: int, n: int):
    return (number & (1 << n)) == 0


def print_board(white_board: int, black_board: int, moves: dict):
    print('○ - white, ● - black, x - available move position')
    print('Current board state:')
    row_text = '  A B C D E F G H'
    print(row_text)

    for i in range(8):
        row = str(i + 1) + ' '
        for j in range(8):
            position = i * 8 + j
            if moves.__contains__(position):
                row += 'x '
            elif nth_bit_set(white_board, position):
                row += '○ '
            elif nth_bit_set(black_board, position):
                row += '● '
            else:
                row += '  '
        print(row)
    print()

def print_available_moves(moves):
    print('Available moves:')
    for move in moves:
        print(chr(move % 8 + ord('A')) + ' ' + str(move // 8 + 1))

def play_pvp():
    board_state = BoardState()

    while not board_state.game_over:
        print_board(board_state.white_board, board_state.black_board, board_state.available_moves)

        if board_state.black_turn:
            print("Black player's turn")
        else:
            print("White player's turn")
        print_available_moves(board_state.available_moves)

        move = input('Input your move e. g. [A 1]\n>')
        pos = move.split(' ')
        position = (int(pos[1]) - 1) * 8 + (ord(pos[0]) - ord('A'))
        if position not in board_state.available_moves:
            print('Invalid move.\n')
            continue
        board_state.make_move(position)

    print('Game over!')
    print_board(board_state.white_board, board_state.black_board, {})
    print(f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')


def play_ai_vs_ai():
    board_state = BoardState()
    blackAI = OpponentAI(True)
    whiteAI = OpponentAI(False)
    black_turn = True

    print('Playing...')
    while not board_state.game_over:
        if board_state.black_turn:
            print("Black player's turn")
        else:
            print("White player's turn")
        print_available_moves(board_state.available_moves)

        start = time.time()
        if black_turn:
            position = blackAI.get_next_move(board_state)
        else:
            position = whiteAI.get_next_move(board_state)
        end = time.time()

        if position is None:
            print('Turn skipped')
        else:
            print(f'AI played {chr(position % 8 + ord("A"))} {str(position // 8 + 1)}')
        print(f'Elapsed time: {end - start}\n')
        board_state.make_move(position)
        black_turn = not black_turn

    print('Game over!')
    print_board(board_state.white_board, board_state.black_board, {})
    print(
        f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')


def play_pve():
    board_state = BoardState()

    if input('Do you want to play as the black player? (Y/N)\n') == 'Y':
        opponent = OpponentAI(False)
        players_turn = True
    else:
        opponent = OpponentAI(True)
        players_turn = False

    while not board_state.game_over:
        print_board(board_state.white_board, board_state.black_board, board_state.available_moves)

        if board_state.black_turn:
            print("Black player's turn")
        else:
            print("White player's turn")
        print_available_moves(board_state.available_moves)

        if players_turn:
            move = input('Input your move e. g. [A 1]\n>>')
            pos = move.split(' ')
            position = (int(pos[1]) - 1) * 8 + (ord(pos[0]) - ord('A'))
            if position not in board_state.available_moves:
                print('Invalid move.\n')
                continue
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
    print_board(board_state.white_board, board_state.black_board, {})
    print(
        f'Winner: {board_state.winner}\nNumber of discs:\nWhite: {board_state.white_discs}\nBlack: {board_state.black_discs}')
    print('Thank you for playing!')