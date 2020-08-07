#!/bin/bash

#SBATCH --partition=bgmp        ### Partition (like a queue in PBS)
#SBATCH --job-name=deplex_30        ### Job Name
#SBATCH --output=deplex_30.out      ### File in which to store job output
#SBATCH --error=deplex_30.err       ### File in which to store job error messages
#SBATCH --time=0-10:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=1     ### Number of tasks to be launched per Node
#SBATCH --account=bgmp          ### Account used for job submission

conda activate bgmp_py37

path=/projects/bgmp/shared/2017_sequencing
in_path=/projects/bgmp/shared/2017_sequencing
out_path=/projects/bgmp/jonasg/bioinfo/622/projects/demultiplexing-Jonasgrove/Assignment-the-third/out_files_30
python demultiplex_v3.py -r1 $in_path/1294_S1_L008_R1_001.fastq.gz -r2 $in_path/1294_S1_L008_R2_001.fastq.gz -r3 $in_path/1294_S1_L008_R3_001.fastq.gz -r4 $in_path/1294_S1_L008_R4_001.fastq.gz -i $path/indexes.txt -p $out_path -q 30

