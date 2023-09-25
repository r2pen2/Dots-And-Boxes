import os
import time

from Constants import *
from Edge import Edge


def awaitTurn():
    """
    Loops until one of the three action files are written by the referee (end_game, SmartTeam.go, SmartTeam.pass) and
    determines the move type upon receiving one of them.

    Returns
    -------
        TurnType: Type of turn to do when exiting.
    """

    # Loop until action is requested by the referee
    while True:

        # Try not to blow up some poor TA's laptop :(
        time.sleep(SLEEP_TIME)

        # Has the game ended?
        if os.path.exists(f'./end_game'):
            return TurnType.END

        # Is it our turn?
        elif os.path.exists(f'./{TEAM_NAME}.go'):
            return TurnType.GO

        # Are we passing?
        elif os.path.exists(f'./{TEAM_NAME}.pass'):
            return TurnType.PASS


def addNewEdgeFromMove(board, player, vertex1, vertex2):
    """
    Examine the current board state and return a value proportional to its favor towards P1.
    Current implementation takes into account the [potential] score of both players AND an avoidance of
    completing the third side of a box (using 'uscore').

    Parameters
    ----------
        board: arr arr Box
            Board to add move to.

        player: Player
            Player making move to add.

        vertex1: Vertex
            Vertex 1 of move edge.

        vertex2: Vertex
            Vertex 2 of move edge.

    Returns
    -------
        bool, EdgeError: True on success, Error type
    """

    # Is the move a pass from the opponent?
    if vertex1.x == 0 and vertex1.y == 0 and vertex2.x == 0 and vertex2.y == 0:
        # Return as if successful, but don't add to board
        return True, EdgeError.EDGE_PASS

    # Is the move out of bounds?
    if (vertex1.x < 0 or vertex1.x > 9 or
            vertex1.y < 0 or vertex1.y > 9 or
            vertex2.x < 0 or vertex2.x > 9 or
            vertex2.y < 0 or vertex2.y > 9):
        # Return Out of Bounds Error
        return False, EdgeError.EDGE_OOB

    # Make new edge
    edge = Edge.getEdgeFromBoard(board, vertex1, vertex2)

    # If edge is null, it doesn't exist
    if edge is None:
        return False, EdgeError.EDGE_INVALID

    # Check if edge is claimed

    # Set owner and add to board
    edge.setOwner(player)
    edge.addToBoard()

    # Return true to indicate success
    return True, EdgeError.EDGE_VALID


def oopsie(error):
    """
    Called when the opponent has made an error and we need to end the program signifying what error was made.

    Parameters
    ----------
        error: bool, EdgeError
            Returned from addNewEdgeFromMove, containing an error.
    """

    # If the edge was invalid
    if error[1] is EdgeError.EDGE_INVALID:
        print("Opponent made an error: Edge is invalid!")

    # If the edge was out of bounds
    elif error[1] is EdgeError.EDGE_OOB:
        print("Opponent made an error: Edge is out of bounds!")

    # If the edge was already claimed
    elif error[1] is EdgeError.EDGE_CLAIMED:
        print("Opponent made an error: Edge is claimed!")

    # Be smug and exit
    print("I win!  :)")
    exit(0)
