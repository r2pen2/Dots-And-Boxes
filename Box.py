import sys

from Constants import *
from Edge import Edge
from Vertex import Vertex

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

    def getClaimedEdges(self):
        return self.__claimedEdges

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
