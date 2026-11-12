#!/usr/bin/env bash
# Adjust the expected-file naming below to match the provided zip.
status=0
for in in tests/*.in; do
  expected="${in%.in}.out"
  python3 elevator.py < "$in" > actual.out
  if diff actual.out "$expected" > /dev/null; then
    echo "PASS $in"
  else
    echo "FAIL $in"; diff actual.out "$expected" | head -20; status=1
  fi
done
rm -f actual.out
exit $status