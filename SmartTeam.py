import re

from Board import Board
from Minimax import *
from Vertex import Vertex
from Gameplay import *

# Create a board
boardState = Board()

# This is "main"
while True:

    # Determine if it's our turn
    turnType = awaitTurn()

    if turnType is TurnType.END:
        print("GAME END")
        break

    print("MY TURN")

    # Examine board
    moveFileR = open("move_file", "r")
    line = moveFileR.readline()
    moveFileR.close()

    # Interpret coords
    coords = re.findall("[0-9],[0-9]", line)

    # If opponent has moved
    if len(coords) != 0:
        vertex1 = Vertex(int(coords[0][0]), int(coords[0][2]))
        vertex2 = Vertex(int(coords[1][0]), int(coords[1][2]))

        print(f'Op move {vertex1.x},{vertex1.y} {vertex2.x},{vertex2.y}')

        # Add opponent move
        edgeStatus = addNewEdgeFromMove(boardState.board, Player.P2, vertex1, vertex2)
        if not edgeStatus[0]:
            oopsie(edgeStatus)

    # Do we pass or play?
    if turnType is TurnType.GO:
        # Make our move
        ourMove = minimax(boardState, boardState.getOpenEdges(), TREE_DEPTH, Player.P1, -math.inf, math.inf)

        addNewEdgeFromMove(boardState.board, Player.P1, ourMove[1].vertex1, ourMove[1].vertex2)

        print(f'My move {ourMove[1].vertex1.x},{ourMove[1].vertex1.y} {ourMove[1].vertex2.x},{ourMove[1].vertex2.y}')

        # Pass off
        moveFileW = open("move_file", "w")
        line = f'{TEAM_NAME} {ourMove[1].vertex1.x},{ourMove[1].vertex1.y} {ourMove[1].vertex2.x},{ourMove[1].vertex2.y}'
        moveFileW.write(line)
        moveFileW.close()

    elif turnType is TurnType.PASS:
        print(f'My move PASS')

        # Pass off
        moveFileW = open("move_file", "w")
        line = f'{TEAM_NAME} 0,0 0,0'
        moveFileW.write(line)
        moveFileW.close()
