# author: Dafydd-Rhys Maund

import pygame
import sys
from operator import add, sub

# board is 8x8
board = [['  ' for i in range(8)] for j in range(8)]


# holds data for each piece
class Piece:
    def __init__(self, team, t, image, killable=False):
        self.team = team
        self.type = t
        self.killable = killable
        self.image = image


# creates instances of each piece (colour, type, image)
bp = Piece('b', 'p', 'images\\b_pawn.png')
wp = Piece('w', 'p', 'images\\w_pawn.png')
bk = Piece('b', 'k', 'images\\b_king.png')
wk = Piece('w', 'k', 'images\\w_king.png')
br = Piece('b', 'r', 'images\\b_rook.png')
wr = Piece('w', 'r', 'images\\w_rook.png')
bb = Piece('b', 'b', 'images\\b_bishop.png')
wb = Piece('w', 'b', 'images\\w_bishop.png')
bq = Piece('b', 'q', 'images\\b_queen.png')
wq = Piece('w', 'q', 'images\\w_queen.png')
bkn = Piece('b', 'kn', 'images\\b_knight.png')
wkn = Piece('w', 'kn', 'images\\w_knight.png')

# starting order of chessboard
starting_order = {(0, 0): pygame.image.load(br.image), (1, 0): pygame.image.load(bkn.image),
                  (2, 0): pygame.image.load(bb.image), (3, 0): pygame.image.load(bk.image),
                  (4, 0): pygame.image.load(bq.image), (5, 0): pygame.image.load(bb.image),
                  (6, 0): pygame.image.load(bkn.image), (7, 0): pygame.image.load(br.image),
                  (0, 1): pygame.image.load(bp.image), (1, 1): pygame.image.load(bp.image),
                  (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),
                  (4, 1): pygame.image.load(bp.image), (5, 1): pygame.image.load(bp.image),
                  (6, 1): pygame.image.load(bp.image), (7, 1): pygame.image.load(bp.image),

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                  (0, 6): pygame.image.load(wp.image), (1, 6): pygame.image.load(wp.image),
                  (2, 6): pygame.image.load(wp.image), (3, 6): pygame.image.load(wp.image),
                  (4, 6): pygame.image.load(wp.image), (5, 6): pygame.image.load(wp.image),
                  (6, 6): pygame.image.load(wp.image), (7, 6): pygame.image.load(wp.image),
                  (0, 7): pygame.image.load(wr.image), (1, 7): pygame.image.load(wkn.image),
                  (2, 7): pygame.image.load(wb.image), (3, 7): pygame.image.load(wk.image),
                  (4, 7): pygame.image.load(wq.image), (5, 7): pygame.image.load(wb.image),
                  (6, 7): pygame.image.load(wkn.image), (7, 7): pygame.image.load(wr.image), }


# creates the chess board with white at bottom
def create(chessboard):
    chessboard[0] = [Piece('b', 'r', 'b_rook.png'), Piece('b', 'kn', 'b_knight.png'), Piece('b', 'b', 'b_bishop.png'),
                     Piece('b', 'q', 'b_queen.png'), Piece('b', 'k', 'b_king.png'), Piece('b', 'b', 'b_bishop.png'),
                     Piece('b', 'kn', 'b_knight.png'), Piece('b', 'r', 'b_rook.png')]

    chessboard[7] = [Piece('w', 'r', 'w_rook.png'), Piece('w', 'kn', 'w_knight.png'), Piece('w', 'b', 'w_bishop.png'),
                     Piece('w', 'q', 'w_queen.png'), Piece('w', 'k', 'w_king.png'), Piece('w', 'b', 'w_bishop.png'),
                     Piece('w', 'kn', 'w_knight.png'), Piece('w', 'r', 'w_rook.png')]

    for i in range(8):
        chessboard[1][i] = Piece('b', 'p', 'b_pawn.png')
        chessboard[6][i] = Piece('w', 'p', 'w_pawn.png')

    return chessboard


# returns whether input withing boundaries
def on(position):
    if -1 < position[0] < 8 and -1 < position[1] < 8:
        return True


# resets killable pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass


# Takes in board as argument then returns 2d array containing positions of valid moves
def highlight(chessboard):
    highlighted = []

    for i in range(len(chessboard)):
        for j in range(len(chessboard[0])):
            if chessboard[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                try:
                    if chessboard[i][j].killable:
                        highlighted.append((i, j))
                except:
                    pass

    return highlighted


# checks whether piece is black or white
def check(moves, index):
    row, col = index

    if moves % 2 == 0:
        if board[row][col].team == 'w':
            return True
    else:
        if board[row][col].team == 'b':
            return True


# checks where a piece can move
def select_moves(piece, index, moves):
    if check(moves, index):
        if piece.type == 'p':
            if piece.team == 'b':
                return highlight(pawn(index, 1, add, 'b'))
            else:
                return highlight(pawn(index, 6, sub, 'w'))

        if piece.type == 'b':
            return highlight(bishop(index))

        if piece.type == 'kn':
            return highlight(knight(index))

        if piece.type == 'r':
            return highlight(rook(index))

        if piece.type == 'q':
            return highlight(queen(index))

        if piece.type == 'k':
            return highlight(king(index))


# return possible pawn moves adhering to rules
def pawn(index, initial, op, col):
    if index[0] == initial:
        if board[op(index[0], 2)][index[1]] == '  ' and board[op(index[0], 1)][index[1]] == '  ':
            board[op(index[0], 2)][index[1]] = 'x '

    top3 = [[op(index[0], 1), index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != col:
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '

    return board


# return possible bishop moves adhering to rules
def bishop(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break

    return board


# return possible knight moves adhering to rules
def knight(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True

    return board


# return possible rook moves adhering to rules
def rook(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break

    return board


# return possible queen moves adhering to rules
def queen(index):
    rook(index)
    chessboard = bishop(index)

    return chessboard


# return possible king moves adhering to rules
def king(index):
    for y in range(3):
        for x in range(3):
            if on((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True

    return board


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)


class Board:

    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, win):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] is None:
                pass
            else:
                win.blit(starting_order[(self.row, self.col)], (self.x, self.y))


# make UI
def make(rows, width):
    grid = []
    gap = width // rows
    print(gap)

    for i in range(rows):
        grid.append([])

        for j in range(rows):
            node = Board(j, i, gap)
            grid[i].append(node)

            if (i + j) % 2 == 1:
                grid[i][j].colour = GREY
    return grid


# draw UI
def draw(win, rows, width):
    gap = width // 8

    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))


# update UI
def update(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)

    draw(win, rows, width)
    pygame.display.update()


# find potential moves
def find(pos, width):
    interval = width / 8
    y, x = pos
    rows = y // interval
    columns = x // interval

    return int(rows), int(columns)


# completes move
def move(original, final):
    starting_order[final] = starting_order[original]
    starting_order[original] = None


# removes blue highlighting
def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i + j) % 2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY

    return grid


create(board)


# initializes UI and chess game
def main(window, win_width):
    moves = 0
    selected = False
    piece_to_move = []
    grid = make(8, WIDTH)

    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # close program if user exits window

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = find(pos, win_width)

                if not selected:
                    try:
                        possible = select_moves((board[x][y]), (x, y), moves)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                            # highlight possible move locations

                        piece_to_move = x, y
                        selected = True
                    except:
                        piece_to_move = []

                else:
                    try:
                        if board[x][y].killable:
                            row, col = piece_to_move  # x,y of og piece
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            move((col, row), (y, x))
                            moves += 1
                        else:
                            deselect()
                            remove_highlight(grid)
                    except:
                        if board[x][y] == 'x ':
                            row, col = piece_to_move
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)
                            move((col, row), (y, x))
                            moves += 1
                        else:
                            deselect()
                            remove_highlight(grid)
                    selected = False

            update(window, grid, 8, win_width)


main(WIN, WIDTH)
