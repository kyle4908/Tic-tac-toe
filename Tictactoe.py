import pygame

pygame.init()

screen_width = 300
screen_length = 500

# creates screen for game
screen = pygame.display.set_mode((screen_width, screen_length))
pygame.display.set_caption("Tic-tac-toe")

White = (255, 255, 255)
Black = (0, 0, 0)

FPS = 60

# size of the cells of the grid
c_size = int(screen_width / 3)

grid = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]

turn = 0
gameWon = False
draw = False


def reset():  # resets the grid to all blanks
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = ' '


def update_grid():  # updates grid on display to the current state of the grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'O':
                draw_o(i, j)
            elif grid[i][j] == 'X':
                draw_x(i, j)
            else:
                continue
    pygame.display.update()


def space_free(row, col):  # checks if a space is blank/free
    if grid[row][col] == ' ':
        return True
    else:
        return False


def insert_letter(letter, row, col):  # inserts a letter to a free space
    if space_free(row, col):
        grid[row][col] = letter


def is_draw():  # checks if the game has concluded in a draw
    for row in grid:
        for element in row:
            if element == ' ':
                return False

    return True


def is_win():  # checks if the game has concluded in a win
    for row in grid:
        if row[0] == row[1] and row[1] == row[2] and row[0] != ' ':
            return True

    for i in range(len(grid[0])):
        if grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i] and grid[0][i] != ' ':
            return True

    if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] and grid[0][0] != ' ':
        return True

    if grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] and grid[0][2] != ' ':
        return True

    return False


def check_who_won(letter):  # checks if a specific letter has won
    for row in grid:
        if row[0] == row[1] and row[1] == row[2] and row[0] == letter:
            return True

    for i in range(len(grid[0])):
        if grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i] and grid[0][i] == letter:
            return True

    if grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] and grid[0][0] == letter:
        return True

    if grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] and grid[0][2] == letter:
        return True

    return False


def comp_move():  # uses minimax algorithm to find the best move for the computer to make
    best_score = -1000  # stores best score that can be obtained from a move
    best_row = -1  # stores row of best move
    best_col = -1  # stores column of best move

    for i in range(len(grid)):
        for j in range(len(grid[0])):  # iterates through all row and column numbers
            if grid[i][j] == ' ':
                grid[i][j] = 'X'  # makes move
                score = minimax(0, False)  # uses minimax to calculate score of that move
                grid[i][j] = ' '  # undoes move
                if score > best_score:  # changes best move and score if current move is the better than previous best
                    best_score = score
                    best_row = i
                    best_col = j

    insert_letter('X', best_row, best_col)  # does the best move found


def minimax(depth, isMaximizing):  # minimax algorithm for calculating score of a move
    if check_who_won('X'):  # gives positive score if move results in a win
        return 100
    elif check_who_won('O'):  # gives negative score if move results in a loss
        return -100
    elif is_draw():  # gives neutral score if move results in a draw
        return 0

    if isMaximizing:
        best_score = -1000  # this segment runs when maximizing and attempts to maximize score from a computer move

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == ' ':
                    grid[i][j] = 'X'
                    score = minimax(0, False)
                    grid[i][j] = ' '
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = 1000  # this segment runs when minimizing and attempts to minimize score from a player move

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == ' ':
                    grid[i][j] = 'O'
                    score = minimax(depth + 1, True)
                    grid[i][j] = ' '
                    if score < best_score:
                        best_score = score
        return best_score


def draw_x(row, col):  # draws an x at the specified row and column
    o1 = int(c_size / 4)
    o2 = o1 * 3
    pygame.draw.line(screen, Black, ((c_size * col) + o1, (c_size * row) + o1),
                     ((c_size * col) + o2, (c_size * row) + o2))
    pygame.draw.line(screen, Black, ((c_size * col) + o1, (c_size * row) + o2),
                     ((c_size * col) + o2, (c_size * row) + o1))


def draw_o(row, col):  # draws an o at the specified row and column
    pygame.draw.circle(screen, Black, ((c_size * col) + int(c_size / 2), (c_size * row) + int(c_size / 2)),
                       int(c_size / 4), 1)


def draw_screen():  # draws white background and the unfilled board
    screen.fill(White)
    pygame.draw.line(screen, Black, (0, c_size), (3 * c_size, c_size))
    pygame.draw.line(screen, Black, (0, 2 * c_size), (3 * c_size, 2 * c_size))
    pygame.draw.line(screen, Black, (c_size, 0), (c_size, 3 * c_size))
    pygame.draw.line(screen, Black, (2 * c_size, 0), (2 * c_size, 3 * c_size))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    running = True
    draw_screen()  # draws white background and the unfilled board
    global turn
    global gameWon
    global draw
    font = pygame.font.Font('freesansbold.ttf', 12)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows quit when exiting out of window
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameWon or draw:  # resets graphics and game when the mouse is pressed after a game is complete
                    reset()
                    turn = 0
                    gameWon = False
                    draw = False
                    draw_screen()
                else:
                    col = int(event.pos[0] / c_size)  # finds row and column of button press
                    row = int(event.pos[1] / c_size)
                    if row > 2 or col > 2 or (not space_free(row, col)):  # ensures pressed space is free and on grid
                        break
                    grid[row][col] = 'O'  # places piece
                    gameWon = is_win()  # checks for game win or draw
                    draw = is_draw()
                    update_grid()
                    if not (gameWon or draw):  # goes to computer turn if player turn completed without game completion
                        turn = turn + 1
                        comp_move()  # performs computer move
                        update_grid()
                        gameWon = is_win()  # checks for game win or draw
                        draw = is_draw()
                        if not (gameWon or draw):  # increments turn count if game isn't complete after computer move
                            turn = turn + 1
                    if gameWon or draw:  # if the game was won or drawn an appropriate message is displayed
                        if gameWon:
                            if turn % 2 == 0:
                                text = font.render('Player won the game, press anywhere to restart', True, Black)
                            else:
                                text = font.render('Computer won the game, press anywhere to restart', True, Black)
                            text_rect = text.get_rect()
                            text_rect.center = (int(screen_width / 2), int((screen_width + screen_length) / 2))
                        else:
                            text = font.render('Game ended in a draw', True, Black)
                            text_rect = text.get_rect()
                            text_rect.center = (int(screen_width / 2), int((screen_width + screen_length) / 2))
                        screen.blit(text, text_rect)
                        pygame.display.update()

    pygame.quit()


main()
