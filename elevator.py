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

IDLE_FOR_FLOOR = {
    1: State.IDLE_FLOOR1,
    2: State.IDLE_FLOOR2,
    3: State.IDLE_FLOOR3,
}

def emit(*outputs):
    for o in outputs:
        print(o)

def handle_idle(state, event, dest, pending):
    if event in REQUESTS:
        requested_floor = REQUESTS[event]
        if state == State.IDLE_FLOOR1:
            if requested_floor == 2:
                emit("CLOSE_DOOR", "MOVE_UP_FAST")
                return State.MOVING_UP_FAST, 2, pending
            elif requested_floor == 3:
                emit("CLOSE_DOOR", "MOVE_UP_FAST")
                return State.MOVING_UP_FAST, 3, pending
        elif state == State.IDLE_FLOOR2:
            if requested_floor == 1:
                emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
                return State.MOVING_DOWN_FAST, 1, pending
            elif requested_floor == 3:
                emit("CLOSE_DOOR", "MOVE_UP_FAST")
                return State.MOVING_UP_FAST, 3, pending
        elif state == State.IDLE_FLOOR3:
            if requested_floor == 1:
                emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
                return State.MOVING_DOWN_FAST, 1, pending
            elif requested_floor == 2:
                emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
                return State.MOVING_DOWN_FAST, 2, pending
    return state, dest, pending

def handle_moving(state, event, dest, pending):
    # NEW: buttons are no longer ignored while moving
    if event in REQUESTS:
        pending.add(REQUESTS[event])      # a set also handles duplicates
        return state, dest, pending
    
    if state == State.MOVING_UP_FAST:
        if (event == "BETWEEN_1_2" and dest == 2) or (event == "BETWEEN_2_3" and dest == 3):
            emit("MOVE_UP_SLOW")
            return State.MOVING_UP_SLOW, dest, pending
    elif state == State.MOVING_UP_SLOW:
        if (event == "AT_FLOOR2" and dest == 2) or (event == "AT_FLOOR3" and dest == 3):
            emit("STOP", "OPEN_DOOR")
            pending.discard(dest)         # this floor is now serviced
            return arrive(dest, pending, "UP") 
    elif state == State.MOVING_DOWN_FAST:
        if (event == "BETWEEN_1_2" and dest == 1) or (event == "BETWEEN_2_3" and dest == 2):
            emit("MOVE_DOWN_SLOW")
            return State.MOVING_DOWN_SLOW, dest, pending
    elif state == State.MOVING_DOWN_SLOW:
        if (event == "AT_FLOOR1" and dest == 1) or (event == "AT_FLOOR2" and dest == 2):
            emit("STOP", "OPEN_DOOR")
            pending.discard(dest)         # this floor is now serviced
            return arrive(dest, pending, "DOWN")  
    return state, dest, pending

def arrive(floor, pending, direction):
    if not pending:
        return IDLE_FOR_FLOOR[floor], None, pending

    next_dest = choose_next(floor, pending, direction)
    if next_dest > floor:
        emit("CLOSE_DOOR", "MOVE_UP_FAST")
        return State.MOVING_UP_FAST, next_dest, pending
    else:
        emit("CLOSE_DOOR", "MOVE_DOWN_FAST")
        return State.MOVING_DOWN_FAST, next_dest, pending


def choose_next(floor, pending, direction):
    # floor     = where the car just stopped (already removed from pending)
    # pending   = floors still waiting; guaranteed non-empty here
    # direction = "UP" or "DOWN", the way the car was just travelling

    ahead = [f for f in pending if (direction == "UP" and f > floor) or (direction == "DOWN" and f < floor)]
    behind = [f for f in pending if (direction == "UP" and f < floor) or (direction == "DOWN" and f > floor)]

    if direction == "UP":
        if ahead:
            return min(ahead)
        else:
            return max(behind)
    else:
        if ahead:
            return max(ahead)
        else:
            return min(behind)

def main():
    state, dest, pending = State.IDLE_FLOOR1, None, set()
    for line in sys.stdin:
        event = line.strip()
        if not event:
            continue
        if state in (State.IDLE_FLOOR1, State.IDLE_FLOOR2, State.IDLE_FLOOR3):
            state, dest, pending = handle_idle(state, event, dest, pending)
        else:
            state, dest, pending = handle_moving(state, event, dest, pending)
            
if __name__ == "__main__":
    main()
