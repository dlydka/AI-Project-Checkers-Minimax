import pygame

from math import sqrt
from pathlib import Path
from constants import *


class BoardGraphics:
    def __init__(self, board, size):
        self.__board = board
        self.__size = size
        # WIDTH and HEIGHT are the dimensions of game window
        self.__WIDTH = self.__size * SQUARE_SIZE
        self.__HEIGHT = self.__size * SQUARE_SIZE
        self.window = pygame.display.set_mode((self.__WIDTH, self.__HEIGHT))
        pygame.init()

    def startWindow(self):
        # initialize game window
        pygame.display.set_caption("Checkers")
        pygame.display.set_icon(pygame.image.load(Path(__file__).parent / "utils/icon.png"))
        self.drawBackground()
        self.drawPieces()
        pygame.display.update()

    def drawBackground(self):
        # draws the black-and-white checkerboard pattern in the background of the window
        self.window.fill(whiteBackground)
        for row in range(self.__size):
            for col in range(not row % 2, self.__size, 2):
                pygame.draw.rect(self.window, blackBackground,
                                 (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawPieces(self):
        # both radiuses are used to create a piece. You overlap the smaller circle on top of the bigger one
        radius_out = SQUARE_SIZE / 2 - PIECE_PADDING
        radius_in = SQUARE_SIZE / 2 - 2 * PIECE_PADDING
        # loading the crown image and scaling it to fit into the smaller circle
        crown = pygame.transform.scale(pygame.image.load(Path(__file__).parent / "utils/crown.png"),
                                       (radius_in * sqrt(2), radius_in * sqrt(2)))
        # loops through each element of game board to find each piece
        # collects both upper-left corner and center coordinates of each field
        for row in range(self.__size):
            _y = row * SQUARE_SIZE
            _yCenter = (row + 1 / 2) * SQUARE_SIZE
            for col in range(self.__size):
                _x = col * SQUARE_SIZE
                _xCenter = (col + 1 / 2) * SQUARE_SIZE
                if self.__board.getPiece(col, row) > 0:
                    # if a piece is found, draws bigger and smaller circles in corresponding color
                    colour_out = darkTeal if self.__board.getPiece(col, row) % 2 else darkRed
                    colour_in = teal if self.__board.getPiece(col, row) % 2 else red
                    pygame.draw.circle(self.window, colour_out, (_xCenter, _yCenter), radius_out)
                    pygame.draw.circle(self.window, colour_in, (_xCenter, _yCenter), radius_in)
                    if self.__board.getPiece(col, row) > 2:
                        self.window.blit(crown, (_xCenter - crown.get_width()/2, _yCenter - crown.get_height()/2))

    def drawWindow(self, board):
        # redraws the window to update any changes
        self.__board = board
        self.drawBackground()
        self.drawPieces()

    def drawValidMoves(self, validMoves):
        # highlights places where it is possible to move
        if validMoves is not None:
            for move in validMoves:
                x, y = move
                pygame.draw.circle(self.window, emerald, ((x + 1 / 2) * SQUARE_SIZE, (y + 1 / 2) * SQUARE_SIZE),
                                   MOVE_SIGNIFIER)

    def update(self):
        pygame.display.update()
