from Board import Board
from BoardGraphics import BoardGraphics


class Checkers:
    def __init__(self, argument):
        self.__size = argument
        self.board = Board(self.__size)
        self.board_graphics = BoardGraphics(self.board, self.__size)
        self.__game_over = False
        self.__selectedPiece = None
        self.__validMoves = None
        self.__turn = 2

    def get_turn(self):
        return self.__turn

    def updateWindow(self):
        # redraw the window after an update on the board
        self.board_graphics.drawWindow(self.board)
        self.board_graphics.drawValidMoves(self.__validMoves)
        self.board_graphics.update()

    def winner(self):
        return self.board.winCondition()

    def getPlayer(self, x, y):
        # return a player that the piece belongs to
        if self.board.getPiece(x, y) != 0:
            return 1 if self.board.getPiece(x, y) % 2 else 2
        else:
            return 0

    def move(self, x, y):
        # the process of moving a selected piece to the position (x, y)
        if self.__selectedPiece and self.board.getPiece(x, y) == 0 and (x, y) in self.__validMoves:
            a, b = self.__selectedPiece
            self.board.move(a, b, x, y)
            skipped = self.__validMoves[(x, y)]
            if skipped:
                self.board.remove(skipped)
            self.switchTurn()
            return True
        return False

    def select(self, x, y):
        # reaction to selecting a field by pressing a mouse button
        if self.__selectedPiece:
            if not self.move(x, y):
                self.__selectedPiece = None
                self.select(x, y)
        piece = self.board.getPiece(x, y)
        if piece != 0 and self.getPlayer(x, y) == self.__turn:
            self.__selectedPiece = (x, y)
            self.__validMoves = self.findPossibleMovesByPiece(x, y, self.board, self.__turn)
            print(self.__validMoves)
            return True
        self.__selectedPiece = None
        self.__validMoves = None
        return False

    def switchTurn(self):
        # after the player moves, switch the turn to the opponent
        self.__validMoves = {}
        if self.__turn == 1:
            self.__turn = 2
        else:
            self.__turn = 1

    def findPossibleMovesByPiece(self, x, y, board, player):
        # collect moves that a given piece can make
        possibleMoves = {}
        d_y = pow(-1, player)  # defines the vertical direction (up or down) in which the piece can be moved
        #                              with value -1 for Player 1 and 1 for Player 2
        possibleMoves.update(self._traverse_left(y - d_y, max(y - 3, -1) if d_y == 1 else min(y + 3, self.__size), -d_y, x - 1, player))
        possibleMoves.update(self._traverse_right(y - d_y, max(y - 3, -1) if d_y == 1 else min(y + 3, self.__size), -d_y, x + 1, player))
        if board.getPiece(x, y) > 2:  # additional check for the queens
            d_y = -d_y
            possibleMoves.update(self._traverse_left(y - d_y, max(y - 3, -1) if d_y == 1 else min(y + 3, self.__size), -d_y, x - 1, player))
            possibleMoves.update(self._traverse_right(y - d_y, max(y - 3, -1) if d_y == 1 else min(y + 3, self.__size), -d_y, x + 1, player))
        return possibleMoves

    def _traverse_left(self, start, stop, step, x, player, skipped=[]):
        # start traversing at the field above or below current field
        # stop traversing on two fields above or below or when reached 0
        # step determines the direction in which we're moving (up or down)
        possibleMoves = {}
        last = []

        # loop checking position below current piece and one below that
        for r in range(start, stop, step):
            if x < 0 or x >= self.__size: break  # make sure the x index is still in bounds of the board
            current = self.board.getPiece(x, r)
            if current == 0:  # found a field that's empty
                if skipped and not last:
                    break  # after jumping over, next move must also be a jump over
                elif skipped:  # after jumping over save this move as final
                    skipped.append(last)
                    possibleMoves[(x, r)] = skipped
                else:
                    possibleMoves[(x, r)] = list(filter(None, [last]))  # normal diagonal move without jumping over
                if last:
                    row = max(r - 3, -1) if step == -1 else min(r + 3, self.__size)
                    if skipped:
                        skipped.append(last)
                        possibleMoves.update(self._traverse_left(r + step, row, step, x - 1, player, skipped=list(filter(None, skipped))))
                        possibleMoves.update(self._traverse_right(r + step, row, step, x + 1, player, skipped=list(filter(None, skipped))))
                    else:
                        possibleMoves.update(self._traverse_left(r + step, row, step, x - 1, player, skipped=list(filter(None, [last]))))
                        possibleMoves.update(self._traverse_right(r + step, row, step, x + 1, player, skipped=list(filter(None, [last]))))
                break
            elif player == self.getPlayer(x, r):
                break  # found a piece of the same colour
            else:  # found a piece of a different colour. Attempt jumping over
                last = (x, r)
            x -= 1
        return possibleMoves

    def _traverse_right(self, start, stop, step, x, player, skipped=[]):
        possibleMoves = {}
        last = []
        for r in range(start, stop, step):
            if x < 0 or x >= self.__size: break  # make sure the x index is still in bounds of the board
            current = self.board.getPiece(x, r)
            if current == 0:  # found a field that's empty
                if skipped and not last:
                    break  # after jumping over, next move must also be a jump over
                elif skipped:  # after jumping over save this move as final
                    skipped.append(last)
                    possibleMoves[(x, r)] = skipped
                else:
                    possibleMoves[(x, r)] = list(filter(None, [last]))  # normal diagonal move without jumping over
                if last:
                    row = max(r - 3, -1) if step == -1 else min(r + 3, self.__size)
                    if skipped:
                        skipped.append(last)
                        possibleMoves.update(self._traverse_left(r + step, row, step, x - 1, player, skipped=list(filter(None, skipped))))
                        possibleMoves.update(self._traverse_right(r + step, row, step, x + 1, player, skipped=list(filter(None, skipped))))
                    else:
                        possibleMoves.update(self._traverse_left(r + step, row, step, x - 1, player, skipped=list(filter(None, [last]))))
                        possibleMoves.update(self._traverse_right(r + step, row, step, x + 1, player, skipped=list(filter(None, [last]))))
                break
            elif player == self.getPlayer(x, r):
                break  # found a piece of the same colour
            else:  # found a piece of a different colour. Attempt jumping over
                last = (x, r)
            x += 1
        return possibleMoves

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.switchTurn()
