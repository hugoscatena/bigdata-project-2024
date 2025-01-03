#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    # pseudo parse
    if "INFO" in line:
        print("INFO\t1")
    elif "WARN" in line:
        print("WARN\t1")
    elif "ERROR" in line:
        print("ERROR\t1")
    else:
        print("OTHER\t1")
