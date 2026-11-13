PY ?= python3

all:
	$(PY) -m py_compile elevator.py

run:
	$(PY) elevator.py

test: all
	./run_tests.sh