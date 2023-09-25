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