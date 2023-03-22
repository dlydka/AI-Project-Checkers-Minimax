from copy import deepcopy
from constants import PLAYER1_PIECE,PLAYER2_PIECE, PLAYER1_QUEEN, PLAYER2_QUEEN

class Board:
    # Field types:
    #  - 0 represents a filed that isn't taken by any piece
    #  - 1 represents a filed taken by Player 1's piece
    #  - 2 represents a filed taken by Player 2's piece
    #  - 3 represents a filed taken by Player 1's queen
    #  - 4 represents a filed taken by Player 2's queen

    def __init__(self, argument):
        # passed argument is an int describing the size of the board
        # given size it's assumed we want to start a new game on a square board
        self.__size = argument
        self.__board = []
        self.setBoard()
        self.onesLeft = self.twosLeft = (self.__size // 2 - 1) * (self.__size // 2)  # how many pieces is there
        self.onesQueens = self.twosQueens = 0
        self.countPieces()

    def countPieces(self):
        # count pieces and queens for each side of the board
        self.onesLeft = self.onesQueens = self.twosLeft = self.twosQueens = 0
        for y in range(self.__size):
            for x in range(self.__size):
                if self.__board[y][x] % 2 == 1:
                    if self.__board[y][x] == 3:
                        self.onesQueens += 1
                    self.onesLeft += 1
                elif self.__board[y][x] != 0 and self.__board[y][x] % 2 == 0:
                    if self.__board[y][x] == 4:
                        self.twosQueens += 1
                    self.twosLeft += 1

    def startNewBoard(self):
        # place the pieces in their starting positions
        for row in range(self.__size // 2 - 1):
            new_row_up = []
            new_row_down = []
            for col in range(self.__size):
                if col % 2 == ((row + 1) % 2):
                    new_row_up.append(PLAYER1_PIECE)
                    new_row_down.append(PLAYER2_PIECE * (self.__size % 2))
                else:
                    new_row_up.append(0)
                    new_row_down.append(PLAYER2_PIECE * (not self.__size % 2))
            self.__board[row] = new_row_up
            self.__board[self.__size - row - 1] = new_row_down

    def setBoard(self):
        # build the board into it's starting state
        for _ in range(self.__size):
            row = []
            for _ in range(self.__size):
                row.append(0)
            self.__board.append(row)
        self.startNewBoard()

    def printBoardToConsole(self):
        for i in range(self.__size):
            print(self.__board[i])

    def move(self, x, y, new_x, new_y):
        # move the piece from (x, y) to (new_x, new_y) and make a queen if the end of the board is reached
        self.__board[y][x], self.__board[new_y][new_x] = self.__board[new_y][new_x], self.__board[y][x]
        if self.__board[new_y][new_x] < min(PLAYER1_QUEEN, PLAYER2_QUEEN) and (new_y == self.__size - 1 or new_y == 0):
            self.__board[new_y][new_x] += 2
        self.countPieces()

    def remove(self, pieces):
        # remove pieces from the list from the board
        for piece in pieces:
            x, y = piece
            self.__board[y][x] = 0
        self.countPieces()

    def winCondition(self):
        self.countPieces()
        if self.onesLeft <= 0:
            return 2
        elif self.twosLeft <= 0:
            return 1
        return None

    def getPiece(self, x, y):
        return self.__board[y][x]

    def getBoard(self):
        return deepcopy(self.__board)

    def count_pieces(self, mode):
        blue = red = 0
        for y in range(self.__size):
            for x in range(self.__size):
                if self.__board[y][x] == 1:
                    blue += 10
                elif self.__board[y][x] == 3:
                    blue += 30
                elif self.__board[y][x] == 2:
                    red += 10
                elif self.__board[y][x] == 4:
                    red += 30
        if mode:
            return blue - red
        else:
            return red - blue

    def evaluate_move_forward(self, mode):
        # premiowanie posuwania sie do przodu, tylko dla zwyklych pionkow
        blue = red = 0
        for y in range(self.__size):
            for x in range(self.__size):
                if self.__board[y][x] == 1:
                    blue = blue + (y * y) + 1
                elif self.__board[y][x] == 2:
                    red = red + ((self.__size - 1 - y) * (self.__size - 1 - y)) + 1 # dla 8x8 to bedzie (7 - y) * (7 - y)
        if mode:
            return blue - red
        else:
            return red - blue

    # mode == True -> dla czerwonego
    # mode == False -> dla niebieskiego
    def count_save_checkers(self, mode):
        if not mode:
            myPiece = 2
            myKing = 4
            enemyPiece = 1
            enemyKing = 3
        else:
            myPiece = 1
            myKing = 3
            enemyPiece = 2
            enemyKing = 4

        count = 0
        for y in range(self.__size):
            for x in range(self.__size):
                if y != 0 and y != self.__size - 1 and x != 0 and x != self.__size - 1:
                    # player blue
                    if mode:
                        if self.__board[y][x] == myPiece and (self.__board[y + 1][x + 1] != enemyPiece
                                                              and self.__board[y + 1][x - 1] != enemyKing):
                            #print("b y = ", y, "x = ", x)
                            count += 1
                    # player red
                    else:
                        if self.__board[y][x] == myPiece and (self.__board[y - 1][x + 1] != enemyPiece
                                                              and self.__board[y - 1][x - 1] != enemyKing):
                            #print("r y = ", y, "x = ", x)
                            count += 1
        return count

    # ciekawa heurystyka https://github.com/dimitrijekaranfilovic/checkers/blob/master/checkers.py
    # do analizy https://github.com/Hsankesara/Draughts-AI/blob/1857c693a8113ed6c515f2023144cf63c0ab25c3/gamebot.py#L193

    def evaluate(self, mode):
        #print(self.count_save_checkers(mode))
        #sleep(5)
        return self.count_pieces(mode)

    def evaluate_2(self, mode):
        # te 3 razem nie graja najlepiej ale count_ppices + save_checkers jset najlepsze jak na razie
        return self.count_pieces(mode) + self.count_save_checkers(mode) + self.evaluate_move_forward(mode)

    def getAllPieces(self, player):
        # return all pieces that are available to the player
        x = []
        y = []

        for i in range(self.__size):
            for j in range(self.__size):
                if self.__board[i][j] != 0 and self.__board[i][j] % 2 == player % 2:
                    x.append(j)
                    y.append(i)

        return x, y
