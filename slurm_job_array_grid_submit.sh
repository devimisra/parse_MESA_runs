#!/bin/bash
#SBATCH --account=share-nv-fys
#SBATCH --partition=norma2
#SBATCH -N 1
#SBATCH --cpus-per-task=4
#SBATCH --ntasks-per-node=1
#SBATCH --time=2-00:00:00
#SBATCH --job-name="mesa_grid"
#SBATCH --output=slurm-%A_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=devina.misra@ntnu.no
#SBATCH --mem-per-cpu=4G
#SBATCH --array=1-128

source $MESASDK_ROOT/../init-mesa
echo "MESA+POSYDON Initialized"

# get the run directory for this job index
RUN_DIR=$(awk -v id=$SLURM_ARRAY_TASK_ID '$1==id {print $2}' joblist.txt)
cd RUNS3/$RUN_DIR || exit 1

./clean
./mk
./rn |tee log.txt