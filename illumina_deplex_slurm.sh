#!/bin/bash

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=illumina_deplex        ### Job Name
#SBATCH --output=illumina_deplex.out      ### File in which to store job output
#SBATCH --error=illumina_deplex.err       ### File in which to store job error messages
#SBATCH --time=0-10:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=1     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp          ### Account used for job submission

path=/projects/bgmp/shared/2017_sequencing
in_path=/projects/bgmp/jonasg/bioinfo/622/projects/demultiplex
out_path=/projects/bgmp/jonasg/bioinfo/622/projects/demultiplex

python demultiplex_v1.py -r1 $in_path/r1_unit_test.fastq.gz -r2 $in_path/r2_unit_test.fastq.gz -r3 $in_path/r3_unit_test.fastq.gz -r4 $in_path/r4_unit_test.fastq.gz -i $path/indexes.txt -p $out_path -q 20
