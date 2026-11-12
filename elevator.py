import sys
from enum import Enum, auto

class State(Enum):
    # TODO: add the states for the elevator
    pass

# Map every button token to the floor it requests
REQUESTS = {
    # TODO: "FLOOR1_UP": 1, ...
}

def emit(*outputs):
    for o in outputs:
        print(o)

def handle_idle(state, event, dest):
    # TODO: decide direction from the idle state and requested floor,
    # emit CLOSE_DOOR then the MOVE output, return (new_state, dest)
    return state, dest

def handle_moving(state, event, dest):
    # TODO: FAST -> SLOW on the right midpoint sensor
    # TODO: SLOW -> idle on the right floor sensor (STOP, OPEN_DOOR)
    # everything else is ignored
    return state, dest

def main():
    # TODO: read the input file, parse the events, and call the appropriate handler
    pass

if __name__ == "__main__":
    main()