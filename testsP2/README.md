# Elevator Controller Simulator - Part 3 Sample Tests

## Scheduling Rules

While moving up:
- Service requests for higher floors during the current upward trip.
- Queue requests for lower floors until the elevator begins moving downward.

While moving down:
- Service requests for lower floors during the current downward trip.
- Queue requests for higher floors until the elevator begins moving upward.

Hallway requests include direction.

## Test 1
Queue a FLOOR2_DOWN request while moving to Floor 3. Service it on the way down.

## Test 2
Queue FLOOR2_DOWN and CAR_FLOOR1 while moving to Floor 3. Service both after reversing direction.

## Test 3
Request Floor 2, then request Floor 3. Continue upward and service Floor 3.

## Test 4
Request Floor 3, then request Floor 1 while moving upward. Queue Floor 1 until the elevator reverses direction.
