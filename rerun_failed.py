#!/usr/bin/env python3
import os
import glob
import shutil

# -----------------------
# SETTINGS
# -----------------------
runs_dir = "RUNS3"        # top folder with your run directories
log_name = "log.txt"      # log file inside each run dir
expected_end = "termination code"  # marker for a clean run

# -----------------------
# FIX FUNCTIONS
# -----------------------
def apply_fix(inlist_file, fix_type):
    """Edit inlist_project or inlist1 to apply the chosen fix."""
    with open(inlist_file, "r") as f:
        lines = f.readlines()

    with open(inlist_file, "w") as f:
        for line in lines:
            if fix_type == "reduce_opacity_max" and line.strip().startswith("!opacity_max"):
                f.write("opacity_max = 10.0d0\n")  # tighten opacity control
            else:
                f.write(line)

# -----------------------
# MAIN SCAN + FIX
# -----------------------
timeout_runs = []

for run_path in glob.glob(os.path.join(runs_dir, "*")):
    if not os.path.isdir(run_path):
        continue
    run_name = os.path.basename(run_path)
    log_file = os.path.join(run_path, log_name)
    if not os.path.exists(log_file):
        continue

    with open(log_file, "r", errors="ignore") as f:
        contents = f.read()

    # check if run finished properly
    if expected_end not in contents.lower():
        print(f"[TIMEOUT] {run_name} → preparing retry")

        retry_dir = run_path + "_retry"
        if os.path.exists(retry_dir):
            shutil.rmtree(retry_dir)
        shutil.copytree(run_path, retry_dir)

        # here you can apply generic fixes if you want
        inlist_file = os.path.join(retry_dir, "inlist1")
        if os.path.exists(inlist_file):
            apply_fix(inlist_file, "reduce_opacity_max")

        timeout_runs.append(run_name)

# -----------------------
# WRITE SUMMARY
# -----------------------
with open("timeout_runs.txt", "w") as f:
    for run in timeout_runs:
        f.write(f"{run} rerun-prepared\n")

print(f"\nSummary: {len(timeout_runs)} timeout runs prepared for rerun. See timeout_runs.txt")