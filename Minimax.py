import math
from copy import deepcopy

from Gameplay import *


def evaluateBoard(board):
    """
    Examine the current board state and return a value proportional to its favor towards P1.
    Current implementation takes into account the [potential] score of both players AND an avoidance of
    completing the third side of a box (using 'uscore').

    Parameters
    ----------
        board: arr arr Box
            Board to evaluate.

    Returns
    -------
        int: Score of the given board.
    """

    # Set up scores
    boxesP1 = 0
    boxesP2 = 0
    uscore = 0

    # Iterate over each box
    for row in range(0, 9):
        for col in range(0, 9):

            # Used to count a single box's edges
            boxEdges = 0

            # Isolate box
            box = board[row][col]

            # Increment box count if claimed
            if box.owner is Player.P1:
                boxesP1 += 1
            elif box.owner is Player.P2:
                boxesP2 += 1

            # For each owned side, increment boxEdges
            boxEdges += box.northEdge.owner is not Player.NONE
            boxEdges += box.eastEdge.owner is not Player.NONE
            boxEdges += box.southEdge.owner is not Player.NONE
            boxEdges += box.westEdge.owner is not Player.NONE

            # If there are 3 sides owned, increment uscore
            if boxEdges == 3:
                uscore += 1

    # Calculate score
    score = (boxesP1 * 1000) - (boxesP2 * 1000) - uscore

    # Return score for board state
    return score


def minimax(boardState, nextMoves, depth, player, alpha, beta):
    """
    Use the minimax algorithm with a defined depth limit to determine the bext move to make.

    Parameters
    ----------
        boardState: Board
            Game board at the top of the tree.

        nextMoves: list Edge
            List of open edges / available moves.

        depth: int
            Distance from maximum depth of tree.

        player: Player
            Player whose turn it is on the current level of the tree.

        alpha: int
            Lowest board / move score so far.

        beta: int
            Highest board / move score so far.

    Returns
    -------
        int: Score of the given board
    """

    # Check if we're at the depth limit
    if depth == 0:
        return evaluateBoard(boardState.board), None

    # Check player
    if player is Player.P1:

        # Set default best move
        bestMove = -math.inf, None

        # Iterate through possible moves
        for move in nextMoves:

            # DEBUG
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

        # Return best move
        return bestMove

    else:  # Player.P2

        # Set default best move
        bestMove = math.inf, None

        # Iterate through possible moves
        for move in nextMoves:

            # DEBUG
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

        # Return best move
        return bestMove