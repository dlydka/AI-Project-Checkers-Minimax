import sys
import pygame

from Checkers import Checkers
from constants import SQUARE_SIZE, FPS, DEPTH
from minimax import minimax


def gameLoop_pvp(checkers):
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        if checkers.winner() is not None:
            if checkers.winner() == 1:
                print("You lost!")
            if checkers.winner() == 2:
                print("You won!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board = checkers.get_board()
                print()
                board.printBoardToConsole()
                print()
                pos = pygame.mouse.get_pos()
                x, y = pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                checkers.select(col, row)
        checkers.updateWindow()
    pygame.quit()


def gameLoop_pvc(checkers):
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        if checkers.get_turn() == 1:
            value, new_board = minimax(checkers.get_board(), 4, True, checkers)
            checkers.ai_move(new_board)
            checkers.board.printBoardToConsole()

        if checkers.winner() is not None:
            if checkers.winner() == 1:
                print("You lost!")
            if checkers.winner() == 2:
                print("You won!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board = checkers.get_board()
                print()
                board.printBoardToConsole()
                print()
                pos = pygame.mouse.get_pos()
                x, y = pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                checkers.select(col, row)
        checkers.updateWindow()
    pygame.quit()


def gameLoop_cvc(checkers):
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        value, new_board = minimax(checkers.get_board(), DEPTH, True, checkers)
        if new_board is None:
            if checkers.get_turn() == 2:
                ends.append(1)
                print("You lost!")
            elif checkers.get_turn() == 1:
                ends.append(2)
                print("You won!")
            running = False
            continue
        checkers.ai_move(new_board)
        if checkers.winner() is not None:
            if checkers.winner() == 1:
                ends.append(1)
                print("You lost!")
            elif checkers.winner() == 2:
                ends.append(2)
                print("You won!")
            running = False
        checkers.updateWindow()
    pygame.quit()


def main():
    checkers = Checkers(8)
    checkers.board_graphics.startWindow()
    if int(sys.argv[1]) == 1:
        gameLoop_pvp(checkers)
    elif int(sys.argv[1]) == 2:
        gameLoop_pvc(checkers)
    else:
        gameLoop_cvc(checkers)


ends = []
main()
won = lose = 0
for i in range(len(ends)):
    if ends[i] == 2:
        won += 1
    elif ends[i] == 1:
        lose += 1
print("Won: " + str(won))
print("Lost: " + str(lose))