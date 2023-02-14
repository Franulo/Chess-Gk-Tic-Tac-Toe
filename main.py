# Import libraries
import pygame
import sys
import time
import random

pygame.init()  # Initialize all imported pygame modules

WIDTH = 900  # Width of the screen
BACK_COLOR = (100, 100, 100)  # Background Color

BOARD = pygame.image.load("assets/Board.png")  # Load the grafic of the game board
X_IMG = pygame.image.load("assets/X.png")  # Load the grafic of the X
O_IMG = pygame.image.load("assets/O.png")  # Load the grafic of the O

SCREEN = pygame.display.set_mode((WIDTH, WIDTH))  # Initialize a window or screen for display

pygame.display.set_caption("Tic Tac Toe")  # Set the current window caption


# A function that takes in a text and renders it to the game window if called
def generate_massage(massage):
    main_font = pygame.font.SysFont("Roboto", 90)  # Create a Font object from the system fonts
    _massage = main_font.render(massage, True, "white", "Red")
    _massage_rect = _massage.get_rect(center=(WIDTH / 2, WIDTH / 2))  # Get the rectangular area of the Surface
    SCREEN.blit(_massage, _massage_rect)  # Blit the surface, "draw on the surface"


# A function that adds an X or O to where the player clicked and renders it in to the game by calling the renderer function if called
def add_OX(player_turn, board,  x_img, o_img):
    current_pos = pygame.mouse.get_pos()  # Get the position of the mouse
    converted_x = (current_pos[0] - 65) / 835 * 2  # Convert it in to for the programm useful values
    converted_y = current_pos[1] / 835 * 2
    if board[round(converted_y)][round(converted_x)] != 'O' and board[round(converted_y)][round(converted_x)] != 'X':  # If the field in the board is free
        board[round(converted_y)][round(converted_x)] = player_turn  # Set the current players icon (X or O) into this field
        player_turn = change_Turn(player_turn)  # Change the players turn
        renderer(board,x_img, o_img)  # Render the changes
    return board, player_turn


# A function that changes the player Turn when called
def change_Turn(player_turn):
    if player_turn == 'O':
        player_turn = 'X'
    else:
        player_turn = 'O'
    return player_turn


# A function that renders values of the array 'board' on to the game board if called
def renderer(board, x_img, o_img):
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == 'X':
                SCREEN.blit(x_img, (x_img.get_rect(center=(j * 300 + 150, i * 300 + 150))))  # Render the X or O
                pygame.display.update()  # Update the screen of the game
            if board[i][j] == 'O':
                SCREEN.blit(o_img, (o_img.get_rect(center=(j * 300 + 150, i * 300 + 150))))
                pygame.display.update()


# A function that checks if someone won the game if called
def check_win(board):
    winner = None
    for row in range(0, 3):  # For the rows
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None): # If one row is full with the same icons
            winner = board[row][0]  # The winner is the one that set the icons
            return winner

    for col in range(0, 3):  # For the colums
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            return winner

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):  # For one diagonal
        winner = board[0][0]
        return winner

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):  # For the other diagonal
        winner = board[0][2]
        return winner

    if winner is None:  # If board is full and no one won return DRAW
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        return "DRAW"


# A function that gives the texts for the end of the game to the function generate_massage and restarts the game if called
def end_of_game(output):
    if output is not None:
        if output == 'X':
            generate_massage("X wins")
        if output == 'O':
            generate_massage("O wins")
        if output == "DRAW":
            generate_massage("DRAW")
        pygame.display.update()  #Updates the display
        time.sleep(2)  # Makes the programm sleep for 2sek
        main()  #Calls the main function (restarts the game)


# A function that sets a X or O to a random spot on the board if called
def random_bot(board, player_turn, x_img, o_img):
    random_number1 = random.randrange(0, len(board))  # Generates a random number form 0 to 3
    random_number2 = random.randrange(0, len(board))

    while board[random_number1][random_number2] is not None:  # Sets an icon on a random not filled field in the board
        random_number1 = random.randrange(0, len(board))
        random_number2 = random.randrange(0, len(board))
    board[random_number1][random_number2] = player_turn
    renderer(board, x_img, o_img)


# A assisting function that gives the find_a_move function the needed requirement in called
def give_correct_if(board, coord_x, coord_y, player_turn, call_nr, check_nr):
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


# A function that looks for 2 O or X in one row, colum or diagonal and places the a O or X to allow the bot to eather win (priority) or stop the player form winning if called
def find_a_move(board, player_turn, x_img, o_img, call_nr):  # The first call_nr looks for wins and the second for loses
    information = [[0, 0, 0], [0, 0, 0], [0, 0]]
    for row in range(0, 3):
        for col in range(0, 3):
            if give_correct_if(board, row, col, player_turn, call_nr, 0):
                information[0][row] += 1
            if information[0][row] == 2:
                for i in range(0, 3):
                    if board[row][i] is None:
                        board[row][i] = player_turn
                        renderer(board, x_img, o_img)
                        return False

    for col in range(0, 3):
        for row in range(0, 3):
            if give_correct_if(board, row, col, player_turn, call_nr, 0):
                information[1][col] += 1
            if information[1][col] == 2:
                for i in range(0, 3):
                    if board[i][col] is None:
                        board[i][col] = player_turn
                        renderer(board, x_img, o_img)
                        return False

    for diagonal in range(0, 3):
        if give_correct_if(board, diagonal, diagonal, player_turn, call_nr, 1):
            information[2][0] += 1
        if information[2][0] == 2:
            for i in range(0, 3):
                if board[i][i] is None:
                    board[i][i] = player_turn
                    renderer(board, x_img, o_img)
                    return False
        if give_correct_if(board, diagonal, diagonal, player_turn, call_nr, 2):
            information[2][1] += 1
        if information[2][1] == 2:
            for i in range(0, 3):
                if board[i][len(board[0])-1 - i] is None:
                    board[i][len(board[0])-1 - i] = player_turn
                    renderer(board, x_img, o_img)
                    return False
    return True


# A function that uses the function find_a_move and if that function doesn't find anything calls the random_bot function if called
def intelli_bot(board, player_turn, x_img, o_img):
    if find_a_move(board, player_turn, x_img, o_img, 0):
        if find_a_move(board, player_turn, x_img, o_img, 1):
            random_bot(board, player_turn, x_img, o_img)


# The main function is the function that gets called at the start of the programm
# It sets up what wasn't already set up and has a while True loop(infinite loop)
# Calls all the other functions and reacts to all things the player does
# It allows to close the game and stop the programm by hitting esc or the red x
# It reacts if the player clicks a mousebutton
def main():
    SCREEN.fill(BACK_COLOR)
    SCREEN.blit(BOARD, (64, 64))

    player_turn = "X"
    board = [[None, None, None], [None, None, None], [None, None, None]]
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()  # Uninitialize all pygame modules
                sys.exit()
            if player_turn == "X":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board, player_turn = add_OX(player_turn, board, X_IMG, O_IMG)
                    win = check_win(board)
                    end_of_game(win)
            else:
                intelli_bot(board, player_turn, X_IMG, O_IMG)
                player_turn = change_Turn(player_turn)
                win = check_win(board)
                end_of_game(win)


# calls the function main at the beginning
if __name__ == "__main__":
    main()
