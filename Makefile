Py ?= python3

all:
	$(PY) -m py_compile elevator.py

run:
	$(PY) elevator.py

test: all
	bash run_tests.sh