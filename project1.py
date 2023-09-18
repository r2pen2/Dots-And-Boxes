import math
import os
import time
from enum import Enum
import sys
from collections import deque
from copy import deepcopy

TEAM_NAME = "smartteam"
SLEEP_TIME = 50
TREE_DEPTH = 1


class Player(Enum):
    NONE = 0
    P1 = 1
    P2 = 2


def awaitTurn():
    # Is our .go file there?
    while True:
        time.sleep(SLEEP_TIME)  # Try not to blow up some poor TA's laptop :(
        if os.path.exists(f'./{TEAM_NAME}.go'):
            return True


def gameHasEnded():
    # Is the end_game file there?
    return os.path.exists(f'game_end')


# Run tests
# Tester.runTests()

class Vertex:
    """
    An object representing the endpoint of an Edge or corner of a Box

    Parameters
    ------------
        x: int
            The x coordinate of this Vertex (from 0 to 9)
        y: int
            The y coordinate of this Vertex (from 0 to 9)
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, other):
        """
        Two Vertices are equal if their x and y coordinates are the same

        Parameters
        ------------
            other: Vertex
                Vertex with which we will compare coordinates

        Return
        ------------
            boolean: Whether these Vertices are equal
        """
        xEq = self.x == other.x
        yEq = self.y == other.y
        return xEq and yEq


class Edge:
    """
    An object representing the line between two vertices. Edges keep track of their owners,
    their two Vertices, and the two (or one if on the outside of the board) Boxes that they touch.

    Parameters
    ------------
        box1: Box
            The first adjacent box
        box2: Box
            The second adjacent box
        vertex1: Vertex
            The first vertex making up this Edge
        vertex2: Vertex
            The second vertex making up this Edge
    """
    owner = Player.NONE
    vertex1 = None
    vertex2 = None

    def __init__(self, box1, box2, vertex1, vertex2):
        self.box1 = box1
        self.box2 = box2
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def setOwner(self, newOwner):
        """
        Set the owner of this Edge

        Parameters
        ------------
            newOwner: Player
                New Player to act as owner for this Edge
        """
        self.owner = newOwner

    def equals(self, other):
        """
        Two Edges are equal if their vertices are the same

        Parameters
        ------------
            other: Edge
                Edge with which we will compare Vertices

        Return
        ------------
            boolean: Whether these Edges are equal
        """
        v1 = self.vertex1.equals(other.vertex1)
        v2 = self.vertex2.equals(other.vertex2)
        return v1 and v2

    def isInList(self, list):
        """
        Determine if an identical edge is in a given list

        Parameters
        ------------
            list: Edge[]
                list of Edges to search for a match

        Return
        ------------
            boolean: Whether this Edge is already in the list
        """
        for edge in list:
            if edge.equals(self):
                return True
        return False

    @staticmethod
    def getEdgeFromBoard(board, vertex1, vertex2):
        """
        Find the Edge on the current game board with the given vertices

        Parameters
        ------------
            board: Board
                The current game board
            vertex1: Vertex
                The first Vertex of the Edge we're locating
            vertex2: Vertex
                The second Vertex of the Edge we're locating

        Return
        ------------
            Edge: The Board's Edge at requested position
        """
        # Find the two boxes that this Edge touches
        for row in board:
            for box in row:
                if box.hasVertices(vertex1, vertex2):
                    # We only need the edge from box1 becuase box2 may not exist but they should be the same Edge either way
                    return box.getEdgeWithVertices(vertex1, vertex2)

        # If edge does not exist
        return None

    def addToBoard(self):
        """
        Place this edge on the board by updating box owners
        """
        # Since boxes share an edge, we need to call claim on both children in order to accurately update counts
        self.box1.claimEdge(self)
        if self.box2 != None:
            self.box2.claimEdge(self)


class Box:
    """
    An object representing a Box on the game board. Boxes keep track of their four Vertices, their four Edges, their Player (owner),
    and how many of their edges have been claimed.

    Parameters
    ------------
        x: int
            This Box's x position on the game board
        y: int
            This Box's y position on the game board
    """

    topLeft = None
    bottomLeft = None
    topRight = None
    bottomRight = None

    owner = Player.NONE
    northEdge = None
    eastEdge = None
    southEdge = None
    westEdge = None
    __x = -1
    __y = -1

    __claimedEdges = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        # Add vertices
        self.topLeft = Vertex(x, y)
        self.bottomLeft = Vertex(x, y + 1)
        self.topRight = Vertex(x + 1, y)
        self.bottomRight = Vertex(x + 1, y + 1)

    def printEdges(self):
        goNorth = self.northEdge == None
        goEast = self.eastEdge == None
        goSouth = self.southEdge == None
        goWest = self.westEdge == None
        if not goNorth and not goEast and not goSouth and not goWest:
            sys.stdout.write("X")
            return
        sys.stdout.write(" ")

    def findNeighbors(self, board):
        """
        Once the board has been initialized, locate all neighbors of this box.

        Parameters
        ------------
            board: Board
                The current game board
        """
        # Check which edges of are unclaimed
        goNorth = self.northEdge is None
        goEast = self.eastEdge is None
        goSouth = self.southEdge is None
        goWest = self.westEdge is None

        # Go in these directions and add an edge w/ neighboring Box
        if goNorth:
            if self.__y == 0:
                # Out of bounds
                self.northEdge = Edge(self, None, self.topLeft, self.topRight)
            else:
                # Find box to north
                northBox = board[self.__y - 1][self.__x]
                # Find edge between
                edgeBetween = Edge(self, northBox, self.topLeft, self.topRight)
                self.northEdge = edgeBetween
                northBox.southEdge = edgeBetween
                # Search north box for adjacencies
                northBox.findNeighbors(board)

        if goEast:
            if self.__x == 8:
                # Out of bounds
                self.eastEdge = Edge(self, None, self.topRight, self.bottomRight)
            else:
                # Find box to the east
                eastBox = board[self.__y][self.__x + 1]
                # Find edge between
                edgeBetween = Edge(self, eastBox, self.topRight, self.bottomRight)
                self.eastEdge = edgeBetween
                eastBox.westEdge = edgeBetween
                # Search east box for adjacencies
                eastBox.findNeighbors(board)

        if goSouth:
            if self.__y == 8:
                # Out of bounds
                self.southEdge = Edge(self, None, self.bottomLeft, self.bottomRight)
            else:
                # Find box to south
                southBox = board[self.__y + 1][self.__x]
                # Find edge between
                edgeBetween = Edge(self, southBox, self.bottomLeft, self.bottomRight)
                self.southEdge = edgeBetween
                southBox.northEdge = edgeBetween
                # Search south box for adjacencies
                southBox.findNeighbors(board)

        if goWest:
            if self.__x == 0:
                # Out of bounds
                self.westEdge = Edge(self, None, self.topLeft, self.bottomLeft)
            else:
                # Find box to west
                westBox = board[self.__y][self.__x - 1]
                # Find edge between
                edgeBetween = Edge(self, westBox, self.topLeft, self.bottomLeft)
                self.westEdge = edgeBetween
                westBox.eastEdge = edgeBetween
                # Search west box for adjacencies
                westBox.findNeighbors(board)

    def setOwner(self, newOwner):
        """
        Set the owner of this Box

        Parameters
        ------------
            newOwner: Player
                New Player to act as owner for this Box
        """
        self.owner = newOwner

    def toString(self):
        """
        Get this Box as a string
        """
        sys.stdout.write('{: <7}'.format(f'[{self.owner}] '.replace("Player.", "")))

    def hasVertices(self, vertex1, vertex2):
        """
        Determine whether this specified Box, defined by its four vertices, encompasses or includes any two given vertices.

        Parameters
        ------------
            vertex1: Vertex
                First vertex to check
            vertex2: Vertex
                Second vertex to check

        Return
        ------------
            boolean: Whether this Box encompasses these two Vertices
        """
        hasVertex1 = vertex1.equals(self.topLeft) or vertex1.equals(self.topRight) or vertex1.equals(
            self.bottomLeft) or vertex1.equals(self.bottomRight)
        hasVertex2 = vertex2.equals(self.topLeft) or vertex2.equals(self.topRight) or vertex2.equals(
            self.bottomLeft) or vertex2.equals(self.bottomRight)
        return hasVertex1 and hasVertex2

    def getEdgeWithVertices(self, vertex1, vertex2):
        """
        Get the edge on this box with given vertices.

        Parameters
        ------------
            vertex1: Vertex
                First vertex to check
            vertex2: Vertex
                Second vertex to check

        Return
        ------------
            Edge: Edge with these two vertices
        """
        if vertex1.equals(self.topLeft) and vertex2.equals(self.topRight):
            return self.northEdge
        if vertex1.equals(self.bottomLeft) and vertex2.equals(self.bottomRight):
            return self.southEdge
        if vertex1.equals(self.topRight) and vertex2.equals(self.bottomRight):
            return self.eastEdge
        if vertex1.equals(self.topLeft) and vertex2.equals(self.bottomLeft):
            return self.westEdge

    def claimEdge(self, edge):
        """
        Claim an Edge on this Box for the Edge's owner. Update the Box's owner if we've now claimed 4 Edges.

        Parameters
        ------------
            edge: Edge
                Edge to claim on this box
        """
        # If we've already claimed 4 Edges, return
        if self.__claimedEdges >= 4:
            return

        # Find the edge that matches and set owner accordingly
        isNorth = edge.equals(self.northEdge)
        isEast = edge.equals(self.eastEdge)
        isSouth = edge.equals(self.southEdge)
        isWest = edge.equals(self.westEdge)
        if isNorth:
            self.northEdge.owner = edge.owner
            self.__claimedEdges += 1
        elif isEast:
            self.eastEdge.owner = edge.owner
            self.__claimedEdges += 1
        elif isSouth:
            self.southEdge.owner = edge.owner
            self.__claimedEdges += 1
        elif isWest:
            self.westEdge.owner = edge.owner
            self.__claimedEdges += 1
        # Update box's owner if that was the last edge
        if self.__claimedEdges == 4:
            self.owner = edge.owner

        # Update the board accordingly


class Board:

    def __init__(self):

        self.board = [
            [Box(0, 0), Box(1, 0), Box(2, 0), Box(3, 0), Box(4, 0), Box(5, 0), Box(6, 0), Box(7, 0), Box(8, 0)],
            [Box(0, 1), Box(1, 1), Box(2, 1), Box(3, 1), Box(4, 1), Box(5, 1), Box(6, 1), Box(7, 1), Box(8, 1)],
            [Box(0, 2), Box(1, 2), Box(2, 2), Box(3, 2), Box(4, 2), Box(5, 2), Box(6, 2), Box(7, 2), Box(8, 2)],
            [Box(0, 3), Box(1, 3), Box(2, 3), Box(3, 3), Box(4, 3), Box(5, 3), Box(6, 3), Box(7, 3), Box(8, 3)],
            [Box(0, 4), Box(1, 4), Box(2, 4), Box(3, 4), Box(4, 4), Box(5, 4), Box(6, 4), Box(7, 4), Box(8, 4)],
            [Box(0, 5), Box(1, 5), Box(2, 5), Box(3, 5), Box(4, 5), Box(5, 5), Box(6, 5), Box(7, 5), Box(8, 5)],
            [Box(0, 6), Box(1, 6), Box(2, 6), Box(3, 6), Box(4, 6), Box(5, 6), Box(6, 6), Box(7, 6), Box(8, 6)],
            [Box(0, 7), Box(1, 7), Box(2, 7), Box(3, 7), Box(4, 7), Box(5, 7), Box(6, 7), Box(7, 7), Box(8, 7)],
            [Box(0, 8), Box(1, 8), Box(2, 8), Box(3, 8), Box(4, 8), Box(5, 8), Box(6, 8), Box(7, 8), Box(8, 8)]
        ]
        # Recursively add edges from the center box
        self.board[4][4].findNeighbors(self.board)

    def printBoard(self):
        for row in range(0, 9):
            print()
            for col in range(0, 9):
                self.board[row][col].toString()
        print()

    def getOpenEdges(self):

        edges = deque()

        # Iterate over every box
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[row][col].northEdge.owner is Player.NONE and self.board[row][col].northEdge not in edges:
                    edges.append(self.board[row][col].northEdge)
                if self.board[row][col].eastEdge.owner is Player.NONE and self.board[row][col].eastEdge not in edges:
                    edges.append(self.board[row][col].eastEdge)
                if self.board[row][col].southEdge.owner is Player.NONE and self.board[row][col].southEdge not in edges:
                    edges.append(self.board[row][col].southEdge)
                if self.board[row][col].westEdge.owner is Player.NONE and self.board[row][col].westEdge not in edges:
                    edges.append(self.board[row][col].westEdge)

        # Return list of open edges
        return edges


class TreeNode:
    """
    A TreeNode representing a game state with a list of list of children nodes

    Parameters
    ------------
      board: box[][]
        Board data to place in this TreeNode
    """

    children = []
    """ Children of this TreeNode (Boards) """

    def __init__(self, board):
        self.board = board

    def populateChildren(self, depth, player):
        """
        Populate the children of this TreeNode up to a specified depth

        Parameters
      ------------
        depth: int
          Depth from root node to populate children
        player: Player
          Player who's turn is it at this board statea
        """


def addNewEdgeFromMove(board, player, vertex1, vertex2):
    # Make new edge
    edge = Edge.getEdgeFromBoard(board, vertex1, vertex2)

    # If edge is null, it doesn't exist
    if edge is None:
        return False

    # Set owner and add to board
    edge.setOwner(player)
    edge.addToBoard()

    # Return true to indicate success
    return True


def evaluateBoard(board):

    boxesP1 = 0
    boxesP2 = 0

    edgesP1 = 0
    edgesP2 = 0

    # Iterate over each box
    for row in range(0, 9):
        for col in range(0, 9):

            # Isolate box
            box = board[row][col]

            # Increment box count if claimed
            if box.owner is Player.P1:
                boxesP1 += 1
            elif box.owner is Player.P2:
                boxesP2 += 1

            # Increment edge count if claimed
            edgesP1 += box.northEdge.owner is Player.P1
            edgesP1 += box.eastEdge.owner is Player.P1
            edgesP1 += box.southEdge.owner is Player.P1
            edgesP1 += box.westEdge.owner is Player.P1

            edgesP2 += box.northEdge.owner is Player.P2
            edgesP2 += box.eastEdge.owner is Player.P2
            edgesP2 += box.southEdge.owner is Player.P2
            edgesP2 += box.westEdge.owner is Player.P2

    # Claim score
    claimP1 = boxesP1 * 1000
    claimP2 = boxesP2 * 1000

    # Calculate score
    score = (boxesP1 - boxesP2) + (edgesP1 - edgesP2) + (claimP1 - claimP2)

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

            if evaluation >= beta:
                return evaluation, move
            else:
                alpha = max(alpha, evaluation)

            # Recurse!
            childMove = minimax(boardCopy, nextMoves, depth-1, Player.P2, alpha, beta)

            # Is child move better than others?
            if childMove[0] > bestMove[0]:
                bestMove = childMove[0], move

            # Set alpha
            alpha = max(alpha, childMove[0])

            # Problematic if true
            if beta <= alpha:
                break

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

            if evaluation <= alpha:
                return evaluation, move
            else:
                beta = min(beta, evaluation)

            # Recurse!
            childMove = minimax(boardCopy, nextMoves, depth - 1, Player.P1, alpha, beta)

            # Is child move worse than others?
            if childMove[0] < bestMove[0]:
                bestMove = childMove[0], move

            # Set beta
            beta = min(beta, childMove[0])

            # Problematic if true
            if beta <= alpha:
                break

        # Return best move
        return bestMove


# Create a board
boardState = Board()

addNewEdgeFromMove(boardState.board, Player.P2, Vertex(0, 0), Vertex(0, 1))
addNewEdgeFromMove(boardState.board, Player.P1, Vertex(0, 0), Vertex(1, 0))
addNewEdgeFromMove(boardState.board, Player.P2, Vertex(1, 1), Vertex(1, 2))
addNewEdgeFromMove(boardState.board, Player.P1, Vertex(1, 1), Vertex(2, 1))
addNewEdgeFromMove(boardState.board, Player.P2, Vertex(2, 1), Vertex(2, 2))

player = Player.P1

while True:

    boardState.printBoard()
    newmove = minimax(boardState, boardState.getOpenEdges(), 3, player, -math.inf, math.inf)
    print(f'{player} move {newmove[1].vertex1.x},{newmove[1].vertex1.y} {newmove[1].vertex2.x},{newmove[1].vertex2.y}')
    addNewEdgeFromMove(boardState.board, Player.P1, newmove[1].vertex1, newmove[1].vertex2)
    # exit()

    if player is Player.P1:
        player = Player.P2
    elif player is Player.P2:
        player = Player.P1

# print(evaluateBoard(boardState.board))
# for edge in boardState.getOpenEdges():
#     print(f'{edge.vertex1.x},{edge.vertex1.y} {edge.vertex2.x},{edge.vertex2.y}')

# This is "main"
while True:
    break
    # Determine if it's our turn
    awaitTurn()

    # Examine board

    # Make move

    # Pass off

    if gameHasEnded():
        break
