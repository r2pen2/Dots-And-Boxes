from enum import Enum

TEAM_NAME = "SmartTeam"
SLEEP_TIME = 0.300
TREE_DEPTH = 5


class Player(Enum):
    NONE = 0
    P1 = 1
    P2 = 2


class TurnType(Enum):
    GO = 0
    PASS = 1
    END = 2


class EdgeError(Enum):
    EDGE_VALID = 0
    EDGE_INVALID = 1
    EDGE_OOB = 2
    EDGE_CLAIMED = 3
    EDGE_PASS = 4
