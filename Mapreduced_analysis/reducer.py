#!/usr/bin/env python
import sys

current_key = None
current_sum = 0

for line in sys.stdin:
    line = line.strip()
    key, value = line.split("\t", 1)
    value = int(value)

    if current_key == key:
        current_sum += value
    else:
        if current_key is not None:
            print(f"{current_key}\t{current_sum}")
        current_key = key
        current_sum = value

# Ne pas oublier la dernière clé
if current_key is not None:
    print(f"{current_key}\t{current_sum}")
