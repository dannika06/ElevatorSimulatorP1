# Elevator Controller Simulator

A three-floor elevator controller implemented in Python as a finite state machine. It reads events (button presses and sensor signals) from standard input and writes door and motion commands to standard output.

## Requirements

- Python 3, available as `python3` (tested with 3.12)
- make
- bash (used by the test script)

The test script must be executable. If you get a "Permission denied" error, run `chmod +x run_tests.sh`. These instructions assume a Linux or macOS shell. On Windows, use WSL.

## Build

```
make
```

Python has no compile step, so this checks `elevator.py` for syntax errors.

## Run

```
make run
```

The program waits for events on standard input, one per line. Press Ctrl+D to finish.

## Test

```
make test
```

This builds the project, then runs `./run_tests.sh`, which feeds every `tests/inputN.txt` to the program and compares the output with `tests/outputN.txt` using `diff`. Any mismatch prints the differences, and the command exits with an error.

The script can also be run on its own:

```
./run_tests.sh
```

To add a test, create `tests/inputN.txt` and `tests/outputN.txt` with the next number. The script picks it up automatically.

## Input and output

**Inputs (one per line):**

| Type | Events |
|---|---|
| Hallway buttons | `FLOOR1_UP`, `FLOOR2_UP`, `FLOOR2_DOWN`, `FLOOR3_DOWN` |
| Car buttons | `CAR_FLOOR1`, `CAR_FLOOR2`, `CAR_FLOOR3` |
| Floor sensors | `AT_FLOOR1`, `AT_FLOOR2`, `AT_FLOOR3` |
| Midpoint sensors | `BETWEEN_1_2`, `BETWEEN_2_3` |

**Outputs:** `OPEN_DOOR`, `CLOSE_DOOR`, `MOVE_UP_FAST`, `MOVE_UP_SLOW`, `MOVE_DOWN_FAST`, `MOVE_DOWN_SLOW`, `STOP`

## Design

The controller has 7 states:

- `IDLE_FLOOR1`, `IDLE_FLOOR2`, `IDLE_FLOOR3`: stopped at a floor with the door open
- `MOVING_UP_FAST`, `MOVING_UP_SLOW`, `MOVING_DOWN_FAST`, `MOVING_DOWN_SLOW`: door closed and moving

The elevator starts in `IDLE_FLOOR1`. The current floor is not stored in a variable. It is encoded by which idle state is active.

When a request arrives in an idle state, the controller emits `CLOSE_DOOR` and the matching `MOVE_*_FAST` output, saves the destination floor in a `dest` variable, and enters a fast moving state. It switches to the slow state when the midpoint sensor next to the destination fires, and stops (`STOP`, `OPEN_DOOR`) when the destination's floor sensor fires in a slow state. While moving, all button presses and sensor events that do not apply are ignored. A request for the current floor while idle does nothing.

## Repository layout

- `elevator.py`: the controller
- `Makefile`: build, run, and test targets
- `run_tests.sh`: executable script that runs all tests and compares actual output with expected output
- `tests/`: input and expected output files
- `.github/workflows/ci.yml`: GitHub Actions workflow

## Continuous integration

GitHub Actions runs `make test` on every push and pull request. The workflow fails if any output does not match the expected output exactly.