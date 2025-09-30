import os, shutil, itertools, numpy as np

# Parameter grid
m1_vals = # Initial Donor masses
m2_vals = # Initial Point masses
porb_vals = # Inintial Periods
beta_ctrl = # 1 - Accretion efficiencies

# Base directory
template_dir =  # your clean template folder
runs_dir = # where you want to run the grids
os.makedirs(runs_dir, exist_ok=True)

with open('joblist.txt', 'w', encoding='ascii') as f:
    job_id = 0
    for m1, m2, Porb, beta in itertools.product(m1_vals, m2_vals, porb_vals, beta_ctrl):
        job_id += 1
        run_name = f'm1-{m1:.1f}_m2-{m2:.1f}_Porb-{Porb:.3f}_x-{xctrl:.1f}'
        run_dir = os.path.join(runs_dir, run_name)
        if os.path.exists(run_dir):
            shutil.rmtree(run_dir)
        shutil.copytree(template_dir, run_dir)

        # edit inlist_project
        proj_file = os.path.join(run_dir, 'inlist_project')
        with open(proj_file) as pf:
            lines = pf.readlines()
        with open(proj_file, 'w') as pf:
            for line in lines:
                if 'm1 =' in line:
                    pf.write(f'm1 = {m1}d0\n')
                elif 'm2 =' in line:
                    pf.write(f'm2 = {m2}d0\n')
                elif 'initial_period_in_days' in line:
                    pf.write(f'initial_period_in_days = {Porb}d0\n')
                elif 'mass_transfer_beta =' in line:
                    pf.write(f'mass_transfer_beta = {beta}d0\n')
                else:
                    pf.write(line)

                    
        f.write(f'{job_id} {run_name}\n')

print(f'Prepared {job_id} runs. Mapping written to joblist.txt')
