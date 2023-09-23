from Constants import *


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
        if self.box2 is not None:
            self.box2.claimEdge(self)
