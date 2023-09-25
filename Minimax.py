import math
import threading
import time
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

    # Define weights for different components of the evaluation
    boxesP1_weight = 1000
    boxesP2_weight = -1000
    uscore_weight = -1

    # Initialize scores
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
            boxEdges += int(box.northEdge.owner is not Player.NONE)
            boxEdges += int(box.eastEdge.owner is not Player.NONE)
            boxEdges += int(box.southEdge.owner is not Player.NONE)
            boxEdges += int(box.westEdge.owner is not Player.NONE)

            # If there are 3 sides owned, increment uscore
            if boxEdges == 3:
                uscore += 1

    # Calculate score using weighted components
    score = (boxesP1 * boxesP1_weight) + (boxesP2 * boxesP2_weight) + (uscore * uscore_weight)

    # Return score for board state
    return score

# A Hash table to store the previous evaluated Evaluation Scores of previously visited edges
transposition_table = {}

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

    # Generate a unique hash key for the current board position
    board_hash = hash(tuple(tuple(box.owner for box in row) for row in boardState.board))

    # Check if this position is already in the transposition table
    if board_hash in transposition_table:
        entry = transposition_table[board_hash]

        # Check if we can use the cached result
        if entry['depth'] >= depth:
            if entry['flag'] == 'exact':
                return entry['score'], entry['best_move']
            elif entry['flag'] == 'lowerbound':
                alpha = max(alpha, entry['score'])
            elif entry['flag'] == 'upperbound':
                beta = min(beta, entry['score'])

            if alpha >= beta:
                return entry['score'], entry['best_move']

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

    # If we reach here, we didn't find a cached result, so compute the result
    best_score, best_move = None, None  # Initialize with no result

    # Cache the result in the transposition table
    if best_score is not None:
        if best_score <= alpha:
            flag = 'upperbound'
        elif best_score >= beta:
            flag = 'lowerbound'
        else:
            flag = 'exact'

        transposition_table[board_hash] = {
            'depth': depth,
            'score': best_score,
            'flag': flag,
            'best_move': best_move,
        }

    return best_score, best_move


def iterative_deepening(boardState, nextMoves, max_depth, player, time_limit):
    best_move = None
    start_time = time.time()
    
    for depth in range(1, max_depth + 1):
        # Call minimax with alpha-beta pruning and transposition tables
        score, move = minimax(boardState, nextMoves, depth, player, -math.inf, math.inf)

        # Update the best move if a better one is found
        if move is not None:
            best_move = move

        # Check if time limit is exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            break

    return best_move






