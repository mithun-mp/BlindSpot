import glob
import os

files = sorted(glob.glob("blindspot/semantic/*.py"))
total = 0
print("--- SEMANTIC SUBSYSTEM BEFORE LOC ---")
for f in files:
    count = len(open(f, "r", encoding="utf-8").readlines())
    total += count
    print(f"{f}: {count}")
print(f"TOTAL BEFORE LOC: {total}")
