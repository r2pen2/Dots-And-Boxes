from collections import deque

from Box import Box
from Constants import *


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
