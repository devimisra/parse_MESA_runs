#!/usr/bin/env python3
import os
import glob


runs_dir =  # top folder with your run directories
log_name = "log.txt"      # change if needed
keywords = ["termination code"]  # search terms
expected_end = "termination code"  # string that indicates a clean finish

# SCAN RUNS
unique_msgs = set()
timeout_runs = []

for run_path in glob.glob(os.path.join(runs_dir, "*")):
    if not os.path.isdir(run_path):
        continue

    log_file = os.path.join(run_path, log_name)
    if not os.path.exists(log_file):
        continue

    with open(log_file, "r", errors="ignore") as f:
        lines = f.readlines()

    # check for failure/termination messages
    found_msg = False
    for line in lines:
        if any(key in line.lower() for key in keywords):
            unique_msgs.add(line.strip())
            found_msg = True

    # if no keyword found at all → probably incomplete
    if not found_msg:
        timeout_runs.append(run_path)

# OUTPUT
print(f"Found {len(unique_msgs)} unique termination/failure messages:\n")
for msg in sorted(unique_msgs):
    print(" -", msg)

print("\nRuns that may have timed out / incomplete (no termination code found):")
for run in timeout_runs:
    print(" -", run)
