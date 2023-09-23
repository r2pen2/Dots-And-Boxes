import math
from copy import deepcopy

from Gameplay import *


def evaluateBoard(board):

    boxesP1 = 0
    boxesP2 = 0
    uscore = 0

    # Iterate over each box
    for row in range(0, 9):
        for col in range(0, 9):

            boxEdges = 0

            # Isolate box
            box = board[row][col]

            # Increment box count if claimed
            if box.owner is Player.P1:
                boxesP1 += 1
            elif box.owner is Player.P2:
                boxesP2 += 1

            boxEdges += box.northEdge.owner is not Player.NONE
            boxEdges += box.eastEdge.owner is not Player.NONE
            boxEdges += box.southEdge.owner is not Player.NONE
            boxEdges += box.westEdge.owner is not Player.NONE

            if boxEdges == 3:
                uscore += 1

    # Calculate score
    score = (boxesP1 * 1000) - (boxesP2 * 1000) - uscore

    # Return score for board state
    return score


def minimax(boardState, nextMoves, depth, player, alpha, beta):

    # Check if we're at the depth limit
    if depth == 0:
        return evaluateBoard(boardState.board), None

    # Check player
    if player is Player.P1:

        # Set default best move
        bestMove = -math.inf, None

        # Iterate through possible moves
        for move in nextMoves:

            # Debug
            # print(f'Check {move.vertex1.x},{move.vertex1.y} {move.vertex2.x},{move.vertex2.y} @ {depth} for {player} -> {evaluateBoard(boardState.board)}')

            # Copy the board
            boardCopy = deepcopy(boardState)

            # Simulate next move
            addNewEdgeFromMove(boardCopy.board, player, move.vertex1, move.vertex2)

            # Evaluate new board
            evaluation = evaluateBoard(boardCopy.board)

            # Alpha-Beta pruning
            if evaluation >= beta:
                return evaluation, move
            else:
                alpha = max(alpha, evaluation)

            # Recurse!
            childMove = minimax(boardCopy, nextMoves, depth-1, Player.P2, alpha, beta)

            # Is child move better than others?
            if childMove[0] > bestMove[0]:
                bestMove = childMove[0], move

            # Double-check alpha
            alpha = max(alpha, childMove[0])

        # Return best move
        return bestMove

    else:  # Player.P2

        # Set default best move
        bestMove = math.inf, None

        # Iterate through possible moves
        for move in nextMoves:

            # Debug
            # print(f'Check {move.vertex1.x},{move.vertex1.y} {move.vertex2.x},{move.vertex2.y} @ {depth} for {player} -> {evaluateBoard(boardState.board)}')

            # Copy the board
            boardCopy = deepcopy(boardState)

            # Simulate next move
            addNewEdgeFromMove(boardCopy.board, player, move.vertex1, move.vertex2)

            # Evaluate new board
            evaluation = evaluateBoard(boardCopy.board)

            # Alpha-Beta pruning
            if evaluation <= alpha:
                return evaluation, move
            else:
                beta = min(beta, evaluation)

            # Recurse!
            childMove = minimax(boardCopy, nextMoves, depth - 1, Player.P1, alpha, beta)

            # Is child move worse than others?
            if childMove[0] < bestMove[0]:
                bestMove = childMove[0], move

            # Double-check beta
            beta = min(beta, childMove[0])

        # Return best move
        return bestMove