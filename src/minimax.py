import random

from copy import deepcopy


def minimax(board, depth, max_player, checkers):
    if depth == 0 or board.winCondition() is not None:
        if checkers.get_turn() == 2:
            return board.evaluate_2(False), board
        elif checkers.get_turn() == 1:
            return board.evaluate(True), board

    if max_player:
        maxEval = [float('-inf')]
        best_move = None
        for move in get_all_moves(board, checkers.get_turn(), checkers):
            evaluation = minimax(move, depth-1, False, checkers)[0]
            if evaluation > maxEval[0]:
                maxEval = [evaluation]
                best_move = [move]
            elif evaluation == maxEval[0]:
                maxEval.append(evaluation)
                best_move.append(move)
        if best_move:
            r = random.randint(0, len(maxEval) - 1)
            maxEval = maxEval[r]
            best_move = best_move[r]
        else:
            maxEval = 0
            best_move = None
        return maxEval, best_move
    else:
        minEval = [float('inf')]
        best_move = None
        for move in get_all_moves(board, checkers.get_turn() % 2 + 1, checkers):
            evaluation = minimax(move, depth-1, True, checkers)[0]
            if evaluation < minEval[0]:
                minEval = [evaluation]
                best_move = [move]
            elif evaluation == minEval[0]:
                minEval.append(evaluation)
                best_move.append(move)
        if best_move:
            r = random.randint(0, len(minEval) - 1)
            minEval = minEval[r]
            best_move = best_move[r]
        else:
            minEval = 0
            best_move = None
        return minEval, best_move


def simulate_move(x, y, move, board, skip):
    board.move(x, y, move[0], move[1])
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, player, checkers):
    moves = []
    x, y = board.getAllPieces(player)
    for i in range(len(x)):
        valid_moves = checkers.findPossibleMovesByPiece(x[i], y[i], board, player)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            new_board = simulate_move(x[i], y[i], move, temp_board, skip)
            moves.append(new_board)
    return moves