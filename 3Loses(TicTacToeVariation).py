# Import libraries
import pygame
import sys
import time
import math
import numpy as np
import copy

pygame.init()  # Initialize all imported pygame modules

SIZE = 900  # Size of the screen
BACK_COLOR = (100, 100, 100)  # Background Color

BOARD = pygame.image.load("assets/Board.png")  # Load the graphic of the game board
X_IMG = pygame.image.load("assets/X.png")  # Load the graphic of the X
O_IMG = pygame.image.load("assets/O.png")  # Load the graphic of the O

SCREEN = pygame.display.set_mode((SIZE, SIZE))  # Initialize a window or screen for display

pygame.display.set_caption("Drei Verliert")  # Set the current window caption


# A function that takes in a text and renders it to the game window if called
def generate_massage(massage):
    main_font = pygame.font.SysFont("Roboto", 90)  # Create a Font object from the system fonts, type and size of text
    _massage = main_font.render(massage, True, "white", "Red")
    _massage_rect = _massage.get_rect(center=(SIZE / 2, SIZE / 2))  # Get the rectangular area of the Surface
    SCREEN.blit(_massage, _massage_rect)  # Blit the surface, "draw on the surface"


# A function that changes the player Turn when called
def other_player_turn(player_turn):
    if player_turn == '1':
        player_turn = '2'
    else:
        player_turn = '1'
    return player_turn


# A function that renders values of the array 'board' on to the game board if called
def renderer(board, x_img):
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == 'X':
                SCREEN.blit(x_img, (x_img.get_rect(center=(j * 300 + 150, i * 300 + 150))))
                pygame.display.update()


# A function that checks if someone won the game if called
def check_lose(board):
    for row in range(0, 3):  # For the rows
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            return True

    for col in range(0, 3):  # For the columns
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            return True

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):  # For one diagonal
        return True

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):  # For the other diagonal
        return True
    return False


# A function that gives the texts for the end of the game to the
# function generate_massage and restarts the game if called
def end_of_game(output):
    if output is not None:
        if output == '1':
            generate_massage("Player 1 wins")
        if output == '2':
            generate_massage("Player 2 wins")
        pygame.display.update()  # Updates the display
        time.sleep(2)  # Makes the program sleep for 2sek
        main()  # Calls the main function (restarts the game)


# A function that adds an X or O to where the player clicked and renders it in to the game
# by calling the renderer function if called
def add_OX(board, x_img, player_turn):

    current_pos = pygame.mouse.get_pos()  # Get the position of the mouse
    converted_x = math.floor(current_pos[0] / 900 * 3)  # Convert it in to for the program useful values -65 / 835 *2
    converted_y = math.floor(current_pos[1] / 900 * 3)
    if converted_x == 3:  # 'edge case'
        converted_x = 2
    if converted_y == 3:  # 'edge case'
        converted_y = 2
    if board[converted_y][converted_x] is None:  # If the field in the board is free
        board[converted_y][converted_x] = 'X'  # Set the current players icon (X or O) into this field
        renderer(board, x_img)  # Render the changes
        player_turn = other_player_turn(player_turn)

    return board, player_turn


# A function that sets an X or O to a random spot on the board if called

# An assisting function that gives the find_a_move function the needed requirement in called

# Bot we had last lesson
def compMove(board, player_turn):
    possibleMoves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                possibleMoves.append(i*3+j)
    bestScore = -1000
    bestMove = 0

    boardCopy = copy.deepcopy(board)

    for move in possibleMoves:
        j = move % 3
        i = (move - j)//3
        boardCopy[i][j] = 'X'
        # Bewertung durch MiniMax-Algorithmus
        score = minimax(boardCopy, 0, False, player_turn)
        if score > bestScore:
            bestScore = score
            bestMove = move
        boardCopy[i][j] = None

    j = bestMove % 3
    i = (bestMove - j) // 3
    board[i][j] = 'X'


def minimax(currBoard, depth, isMaximizing, player_turn):
    # terminal states
    if check_lose(currBoard) and isMaximizing:
        return 10-depth
    elif check_lose(currBoard) and not isMaximizing:
        return -10+depth

    # recursive minimax
    possibleMoves = []
    for i in range(len(currBoard)):
        for j in range(len(currBoard[i])):
            if currBoard[i][j] is None:
                possibleMoves.append(i * 3 + j)

    # boardCopy = currBoard.copy() ?Ds

    if isMaximizing:

        # -1000 is like -infinity in this case
        bestScore = -1000
        for move in possibleMoves:
            j = move % 3
            i = (move - j)//3
            currBoard[i][j] = 'X'
            score = minimax(currBoard, depth + 1, False, player_turn)
            currBoard[i][j] = None
            bestScore = np.maximum(score, bestScore)
        return bestScore

    else:
        bestScore = 1000
        for move in possibleMoves:
            j = move % 3
            i = (move - j)//3
            currBoard[i][j] = 'X'
            score = minimax(currBoard, depth + 1, True, player_turn)
            currBoard[i][j] = None
            bestScore = np.minimum(score, bestScore)
        return bestScore


# The main function is the function that gets called at the start of the program
# It sets up what wasn't already set up and has a while True loop(infinite loop)
# Calls all the other functions and reacts to all things the player does.
# It allows to close the game and stop the program by hitting esc or the red x
# It reacts if the player clicks a mouse button
def main():
    SCREEN.fill(BACK_COLOR)  # Fill screen with the background color
    SCREEN.blit(BOARD, (64, 64))  # "draws" the board

    player_turn = "1"  # The player turn at the beginning of the game
    board = [[None, None, None], [None, None, None], [None, None, None]]  # Initialise the board
    pygame.display.update()  # Update the screen

    while True:  # infinite loop
        for event in pygame.event.get():  # Get events from the queue https://www.pygame.org/docs/ref/event.html
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()  # Uninitialize all pygame modules
                sys.exit()  # Exit the program
            if player_turn == "1":  # Player gets to play
                if event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is clicked
                    board, player_turn = add_OX(board, X_IMG, player_turn)
                    if check_lose(board):  # Find a win and save it in 'win'
                        end_of_game("2")  # Put out the win massage and restart the game after delay
            else:  # Bot gets to play
                compMove(board, player_turn)
                renderer(board, X_IMG)
                player_turn = other_player_turn(player_turn)
                if check_lose(board):  # Find a win and save it in 'win'
                    end_of_game("1")


# calls the function main at the beginning
if __name__ == "__main__":
    main()
