#!/usr/bin/env bash
status=0
for in in testsP2/input*.txt; do
  n="${in##*/input}"          # "1.txt" from "testsP2/input1.txt"
  n="${n%.txt}"               # "1"
  expected="testsP2/output${n}.txt"
  python3 elevator.py < "$in" > actual.out
  if diff actual.out "$expected" > /dev/null; then
    echo "PASS $in"
  else
    echo "FAIL $in"
    diff actual.out "$expected" | head -20
    status=1
  fi
done
rm -f actual.out
exit $status