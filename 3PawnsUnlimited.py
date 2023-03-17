import pygame
import sys
import time

pygame.init()

SIZE = 800

BOARD = pygame.image.load("assets/img.png")
B_PAWN = pygame.image.load("assets/B_Pawn.png")
W_PAWN = pygame.image.load("assets/W_Pawn.png")

SIZED_BOARD = pygame.transform.scale(BOARD, (1.28*(SIZE+100), 1.28*SIZE))
SCREEN = pygame.display.set_mode((SIZE, SIZE))

pygame.display.set_caption("3 Pawns")

graphical_board = [[W_PAWN, W_PAWN, W_PAWN],
                   [None, None, None],
                   [B_PAWN, B_PAWN, B_PAWN]]

player_turn = "White"


def synchronizeDigital(abstract_board):
    for i in range(0, 3):
        for j in range(0, 3):
            if graphical_board[i][j] == W_PAWN:
                abstract_board[i][j] = 'W'
            if graphical_board[i][j] == B_PAWN:
                abstract_board[i][j] = 'B'
            if graphical_board[i][j] is None:
                abstract_board[i][j] = None
    return abstract_board


def check_win():
    w_count = 0
    b_count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if graphical_board[i][j] == B_PAWN:
                b_count += 1
            if graphical_board[i][j] == W_PAWN:
                w_count += 1
    if w_count != 0 and b_count == 0:
        return 'White'
    if b_count != 0 and w_count == 0:
        return 'Black'


def end_of_game(output):
    if output is not None:
        if output == 'White':
            generate_massage("White wins")
        if output == 'Black':
            generate_massage("Black wins")
        if output == 'Draw':
            generate_massage("Draw")
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()


def generate_massage(massage):
    main_font = pygame.font.SysFont("Roboto", 90)  # Create a Font object from the system fonts, type and size of text
    _massage = main_font.render(massage, True, "white", "Red")
    _massage_rect = _massage.get_rect(center=(SIZE / 2, SIZE / 2))  # Get the rectangular area of the Surface
    SCREEN.blit(_massage, _massage_rect)


def check_movement_rules(selected_row, selected_colum, figure, row, colum, the_board):
    if figure == W_PAWN:
        if row == selected_row+1 and colum == selected_colum and the_board[row][colum] is None:
            return True
        if row == selected_row+1 and (colum == selected_colum-1 or colum == selected_colum+1 or (selected_colum == 0 and colum == 2) or (selected_colum == 2 and colum == 0)) and (the_board[row][colum] == B_PAWN or the_board[row][colum] == 'B'):
            return True
        if row == 0 and selected_row == 2 and colum == selected_colum and the_board[row][colum] is None:
            return True
        if row == 0 and selected_row == 2 and (colum == selected_colum-1 or colum == selected_colum+1 or (selected_colum == 0 and colum == 2) or (selected_colum == 2 and colum == 0)) and (the_board[row][colum] == B_PAWN or the_board[row][colum] == 'B'):
            return True

        # if selected_row == 0 and row == 2 and colum == selected_colum and the_board[row][colum] is None and the_board[1][colum] is None:
            # return True
    if figure == B_PAWN:
        if row == selected_row-1 and colum == selected_colum and the_board[row][colum] is None:
            return True
        if row == selected_row-1 and (colum == selected_colum-1 or colum == selected_colum+1 or (selected_colum == 0 and colum == 2) or (selected_colum == 2 and colum == 0)) and (the_board[row][colum] == W_PAWN or the_board[row][colum] == 'W'):
            return True
        if row == 2 and selected_row == 0 and colum == selected_colum and the_board[row][colum] is None:
            return True
        if row == 2 and selected_row == 0 and (colum == selected_colum-1 or colum == selected_colum+1 or (selected_colum == 0 and colum == 2) or (selected_colum == 2 and colum == 0)) and (the_board[row][colum] == W_PAWN or the_board[row][colum] == 'W'):
            return True
        # if selected_row == 2 and row == 0 and colum == selected_colum and the_board[row][colum] is None and the_board[1][colum] is None:
            # return True
    return False


def change_player_turn():
    if player_turn == "White":
        return "Black"
    else:
        return "White"


def which_color(selected_row, selected_colum):
    if graphical_board[selected_row][selected_colum] == W_PAWN:
        return "White"
    else:
        return "Black"


def select_clicked_figure():
    mouse_posX, mouse_posY = pygame.mouse.get_pos()
    colum = round(((mouse_posX - 150) / 0.83) / 300)
    row = round(((mouse_posY - 650) / -0.83) / 300)
    if row == 3:
        row = 2
    if colum == 3:
        colum = 2
    if row == -1:
        row = 0
    if colum == -1:
        colum = 0
    return row, colum


def move_to_clicked(selected_row, selected_colum):
    global player_turn
    mouse_posX, mouse_posY = pygame.mouse.get_pos()
    colum = round(((mouse_posX - 150) / 0.83) / 300)
    row = round(((mouse_posY - 650) / -0.83) / 300)
    if check_movement_rules(selected_row, selected_colum, graphical_board[selected_row][selected_colum], row, colum, graphical_board):
        player_turn = change_player_turn()
        move_figure(selected_row, selected_colum, row, colum)


def move_figure(figure_row, figure_colum, new_row, new_colum):
    figure = graphical_board[figure_row][figure_colum]
    graphical_board[figure_row][figure_colum] = None
    graphical_board[new_row][new_colum] = figure


def second_click(selected_row, selected_colum):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                move_to_clicked(selected_row, selected_colum)
                if check_win() == 'Black':
                    end_of_game('Black')
                if check_win() == 'White':
                    end_of_game('White')
                main()


def sized_Figure(image):
    return pygame.transform.scale(image, (165, 360))


def renderer():
    SCREEN.blit(SIZED_BOARD, (-200, -70))
    for row, val1 in enumerate(graphical_board):
        for colum, val2 in enumerate(val1):
            if graphical_board[row][colum] is not None:
                x_coords = (300 * colum) * 0.83 + 70
                y_coords = 400 - (300 * row) * 0.83
                SCREEN.blit(sized_Figure(val2), (x_coords, y_coords))


def compMove():
    boardCopy = [[None, None, None], [None, None, None], [None, None, None]]
    boardCopy = synchronizeDigital(boardCopy)
    possibleFigures = []
    for i in range(len(boardCopy)):
        for j in range(len(boardCopy[i])):
            if boardCopy[i][j] == 'B':
                possibleFigures.append(i*3+j)

    bestScore = -1000
    bestMove = 0
    bestFigure = 0
    counter = 0
    for figure in possibleFigures:
        possibleMoves = []
        j = figure % 3
        i = (figure - j)//3
        for a in range(len(boardCopy)):
            for b in range(len(boardCopy[a])):
                if check_movement_rules(i, j, B_PAWN, a, b, boardCopy):
                    possibleMoves.append(a*3 + b)
        if possibleMoves:
            counter += 1
            for move in possibleMoves:
                b = move % 3
                a = (move - b) // 3
                boardCopy[i][j] = None
                boardCopy[a][b] = 'B'
        # Bewertung durch MiniMax-Algorithmus
                score = minimax(boardCopy, 0, False)
                if score > bestScore:
                    bestScore = score
                    bestFigure = figure
                    bestMove = move
                boardCopy[i][j] = 'B'
                boardCopy[a][b] = None

    if counter == 0:
        end_of_game('Draw')
    j = bestFigure % 3
    i = (bestFigure - j) // 3
    b = bestMove % 3
    a = (bestMove - b) // 3
    graphical_board[i][j] = None
    graphical_board[a][b] = B_PAWN


def minimax(currBoard, depth, isMaximizing):
    # terminal states
    if check_win() == 'White':
        return -100+depth
    elif check_win() == 'Black':
        return 100-depth
    # recursive minimax
    possibleFigures = []
    for i in range(len(currBoard)):
        for j in range(len(currBoard[i])):
            if currBoard[i][j] == 'B':
                possibleFigures.append(i * 3 + j)

    if isMaximizing:

        # -1000 is like -infinity in this case
        bestScore = -1000
        for figure in possibleFigures:
            possibleMoves = []
            j = figure % 3
            i = (figure - j) // 3
            for a in range(len(currBoard)):
                for b in range(len(currBoard[a])):
                    if check_movement_rules(i, j, B_PAWN, a, b, currBoard):
                        possibleMoves.append(a * 3 + b)
            for move in possibleMoves:
                b = move % 3
                a = (move - b) // 3
                currBoard[i][j] = None
                currBoard[a][b] = B_PAWN
                # Bewertung durch MiniMax-Algorithmus
                score = minimax(currBoard, depth + 1, False)
                if score > bestScore:
                    bestScore = score
                currBoard[i][j] = B_PAWN
                currBoard[a][b] = None
        return bestScore

    else:
        bestScore = 1000
        for figure in possibleFigures:
            possibleMoves = []
            j = figure % 3
            i = (figure - j) // 3
            for a in range(len(currBoard)):
                for b in range(len(currBoard[a])):
                    if check_movement_rules(i, j, W_PAWN, a, b, currBoard):
                        possibleMoves.append(a * 3 + b)
            for move in possibleMoves:
                b = move % 3
                a = (move - b) // 3
                currBoard[i][j] = None
                currBoard[a][b] = W_PAWN
                # Bewertung durch MiniMax-Algorithmus
                score = minimax(currBoard, depth + 1, True)
                if score > bestScore:
                    bestScore = score
                currBoard[i][j] = W_PAWN
                currBoard[a][b] = None
        return bestScore


def main():
    global player_turn
    renderer()
    pygame.display.update()

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if player_turn == "Black":
                compMove()
                player_turn = change_player_turn()
                renderer()
                if check_win() == 'Black':
                    end_of_game('Black')
                pygame.display.update()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_row, selected_colum = select_clicked_figure()
                    if player_turn == which_color(selected_row, selected_colum):
                        if graphical_board[selected_row][selected_colum] is not None:
                            second_click(selected_row, selected_colum)


if __name__ == "__main__":
    main()
