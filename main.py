import pygame
import sys
import time
import random

pygame.init()

WIDTH = 900
BACK_COLOR = (100, 100, 100)

BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")

SCREEN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Tic Tac Toe")


def generate_massage(massage):
    main_font = pygame.font.SysFont("Roboto", 90)
    _massage = main_font.render(massage, True, "white", "Red")
    _massage_rect = _massage.get_rect(center=(WIDTH / 2, WIDTH / 2))
    SCREEN.blit(_massage, _massage_rect)


def add_OX(player_turn, board,  x_img, o_img):
    current_pos = pygame.mouse.get_pos()
    converted_x = (current_pos[0] - 65) / 835 * 2
    converted_y = current_pos[1] / 835 * 2
    if board[round(converted_y)][round(converted_x)] != 'O' and board[round(converted_y)][round(converted_x)] != 'X':
        board[round(converted_y)][round(converted_x)] = player_turn
        player_turn = change_Turn(player_turn)
        renderer(board,x_img, o_img)
    return board, player_turn


def change_Turn(player_turn):
    if player_turn == 'O':
        player_turn = 'X'
    else:
        player_turn = 'O'
    return player_turn


def renderer(board, x_img, o_img):
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == 'X':
                SCREEN.blit(x_img, (x_img.get_rect(center=(j * 300 + 150, i * 300 + 150))))
                pygame.display.update()
            if board[i][j] == 'O':
                SCREEN.blit(o_img, (o_img.get_rect(center=(j * 300 + 150, i * 300 + 150))))
                pygame.display.update()


def check_win(board):
    winner = None
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            return winner

    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            return winner

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        return winner

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        return winner

    if winner is None:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        return "DRAW"


def win_output(output):
    if output is not None:
        if output == 'X':
            generate_massage("X wins")
        if output == 'O':
            generate_massage("O wins")
        if output == "DRAW":
            generate_massage("DRAW")
        pygame.display.update()
        time.sleep(2)
        main()


def random_bot(board, player_turn, x_img, o_img):
    random_number1 = random.randrange(0, len(board))
    random_number2 = random.randrange(0, len(board))

    while board[random_number1][random_number2] is not None:
        random_number1 = random.randrange(0, len(board))
        random_number2 = random.randrange(0, len(board))
    board[random_number1][random_number2] = player_turn
    renderer(board, x_img, o_img)


def c(board, coord_x, coord_y, player_turn, call_nr, check_nr):
    if call_nr == 0:
        if check_nr == 0:
            if board[coord_x][coord_y] == player_turn:
                return True
        if check_nr == 1:
            if board[coord_x][coord_y] == player_turn:
                return True
        if check_nr == 2:
            if board[coord_x][len(board[0])-1 - coord_y] == player_turn:
                return True
    if call_nr == 1:
        if check_nr == 0:
            if board[coord_x][coord_y] != player_turn and board[coord_x][coord_y] is not None:
                return True
        if check_nr == 1:
            if board[coord_x][coord_y] != player_turn and board[coord_x][coord_y] is not None:
                return  True
        if check_nr == 2:
            if board[coord_x][len(board[0]) - 1 - coord_y] != player_turn and board[coord_x][len(board[0]) - 1 - coord_y] is not None:
                return True
    return False

def find_a_move(board, player_turn, x_img, o_img, call_nr):
    information = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for row in range(0, 3):
        for col in range(0, 3):
            if c(board, row, col, player_turn, call_nr, 0):
                information[0][row] += 1
            if information[0][row] == 2:
                for i in range(0, 3):
                    if board[row][i] is None:
                        board[row][i] = player_turn
                        renderer(board, x_img, o_img)
                        return False

    for col in range(0, 3):
        for row in range(0, 3):
            if c(board, row, col, player_turn, call_nr, 0):
                information[1][col] += 1
            if information[1][col] == 2:
                for i in range(0, 3):
                    if board[i][col] is None:
                        board[i][col] = player_turn
                        renderer(board, x_img, o_img)
                        return False

    for diagonal in range(0, 3):
        if c(board, diagonal, diagonal, player_turn, call_nr, 1):
            information[2][0] += 1
        if information[2][0] == 2:
            for i in range(0, 3):
                if board[i][i] is None:
                    board[i][i] = player_turn
                    renderer(board, x_img, o_img)
                    return False
        if c(board, diagonal, diagonal, player_turn, call_nr, 2):
            information[2][1] += 1
        if information[2][1] == 2:
            for i in range(0, 3):
                if board[i][len(board[0])-1 - i] is None:
                    board[i][len(board[0])-1 - i] = player_turn
                    renderer(board, x_img, o_img)
                    return False
    return True


def intelli_bot(board, player_turn, x_img, o_img):
    if find_a_move(board, player_turn, x_img, o_img, 0):
        if find_a_move(board, player_turn, x_img, o_img, 1):
            random_bot(board, player_turn, x_img, o_img)


def main():
    SCREEN.fill(BACK_COLOR)
    SCREEN.blit(BOARD, (64, 64))

    player_turn = "X"
    board = [[None, None, None], [None, None, None], [None, None, None]]
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if player_turn == "X":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board, player_turn = add_OX(player_turn, board, X_IMG, O_IMG)
                    win = check_win(board)
                    win_output(win)
            else:
                intelli_bot(board, player_turn, X_IMG, O_IMG)
                player_turn = change_Turn(player_turn)
                win = check_win(board)
                win_output(win)


if __name__ == "__main__":
    main()
