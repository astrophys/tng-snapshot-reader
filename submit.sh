#!/bin/bash
#$ -M asnedden@nd.edu
#$ -m abe
#$ -pe smp 4
#$ -q debug

set -e
module use /afs/crc.nd.edu/group/phillips/software/modules/
ml purge
ml load python/illustris

#Rscript src/astro_tda.R /afs/crc.nd.edu/user/a/asnedden/Analysis/TDA/TNG-50/Illustris-3/snapshot_135/gas_snap_135_nvox_100.pkl Dionysus none kde none none 0.20

python src/snapshot_reader.py ~/Lab/phillips/data/TNG-50/Illustris-3/output/ 135 100 75000
echo "done"
