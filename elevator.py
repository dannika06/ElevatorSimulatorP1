import sys
from enum import Enum, auto

class State(Enum):
    # use auto() to automatically assign values to the states
    IDLE_FLOOR1 = auto()
    IDLE_FLOOR2 = auto()
    IDLE_FLOOR3 = auto()
    MOVING_UP_FAST = auto()
    MOVING_UP_SLOW = auto()
    MOVING_DOWN_FAST = auto()
    MOVING_DOWN_SLOW = auto()

# Map every button token to the floor it requests
REQUESTS = {
    "FLOOR1_UP": 1,
    "FLOOR2_UP": 2,
    "FLOOR2_DOWN": 2,
    "FLOOR3_DOWN": 3,
    "CAR_FLOOR1": 1,
    "CAR_FLOOR2": 2,
    "CAR_FLOOR3": 3,
}

def emit(*outputs):
    for o in outputs:
        print(o)

def handle_idle(state, event, dest):
    # TODO: decide direction from the idle state and requested floor,
    # emit CLOSE_DOOR then the MOVE output, return (new_state, dest)
    if event in REQUESTS:
        requested_floor = REQUESTS[event]
        if state == State.IDLE_FLOOR1:
            if requested_floor == 2:
                emit("CLOSE_DOOR", "MOVE_UP_FAST")
                return State.MOVING_UP_FAST, 2
            elif requested_floor == 3:
                emit("CLOSE_DOOR", "MOVE_UP_FAST")
                return State.MOVING_UP_FAST, 3
        elif state == State.IDLE_FLOOR2:
            if requested_floor == 1:
                emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
                return State.MOVING_DOWN_FAST, 1
            elif requested_floor == 3:
                emit("CLOSE_DOOR", "MOVE_UP_FAST")
                return State.MOVING_UP_FAST, 3
        elif state == State.IDLE_FLOOR3:
            if requested_floor == 1:
                emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
                return State.MOVING_DOWN_FAST, 1
            elif requested_floor == 2:
                emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
                return State.MOVING_DOWN_FAST, 2
    return state, dest

def handle_moving(state, event, dest):
    # TODO: FAST -> SLOW on the right midpoint sensor
    # TODO: SLOW -> idle on the right floor sensor (STOP, OPEN_DOOR)
    # everything else is ignored
    return state, dest

def main():
    # TODO: read the input file, parse the events, and call the appropriate handler
    state, dest = State.IDLE_FLOOR1, None
    for line in sys.stdin:
        event = line.strip()
        if not event:
            continue
        if state in (State.IDLE_FLOOR1, State.IDLE_FLOOR2, State.IDLE_FLOOR3):
            state, dest = handle_idle(state, event, dest)
        else:
            state, dest = handle_moving(state, event, dest)

if __name__ == "__main__":
    main()