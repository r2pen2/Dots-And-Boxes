import os
import time

from Constants import *
from Edge import Edge


def awaitTurn():
    # Is our .go file there?
    while True:
        time.sleep(SLEEP_TIME)  # Try not to blow up some poor TA's laptop :(
        if os.path.exists(f'./end_game'):
            return TurnType.END
        if os.path.exists(f'./{TEAM_NAME}.go'):
            return TurnType.GO
        if os.path.exists(f'./{TEAM_NAME}.pass'):
            return TurnType.PASS


def gameHasEnded():
    # Is the end_game file there?
    return os.path.exists(f'game_end')


def addNewEdgeFromMove(board, player, vertex1, vertex2):

    if vertex1.x == 0 and vertex1.y == 0 and vertex2.x == 0 and vertex2.y == 0:
        return True, EdgeError.EDGE_PASS

    if (vertex1.x < 0 or vertex1.x > 9 or
            vertex1.y < 0 or vertex1.y > 9 or
            vertex2.x < 0 or vertex2.x > 9 or
            vertex2.y < 0 or vertex2.y > 9):
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
        # return False, EdgeError.EDGE_CLAIMED

    # Return true to indicate success
    return True, EdgeError.EDGE_VALID


def oopsie(error):

    if error[1] is EdgeError.EDGE_INVALID:
        print("Opponent made an error: Edge is invalid!")

    elif error[1] is EdgeError.EDGE_OOB:
        print("Opponent made an error: Edge is out of bounds!")

    elif error[1] is EdgeError.EDGE_CLAIMED:
        print("Opponent made an error: Edge is claimed!")

    print("I win!  :)")
    exit(0)
