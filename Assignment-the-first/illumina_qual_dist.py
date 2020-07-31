#!/usr/bin/env python

import itertools
import gzip
import numpy as np
import argparse

def makeGraphs(x,y,title,ylabel,outFile):
    import matplotlib.pyplot as plt
    variable = plt.figure()
    plt.rcParams['figure.figsize'] = (15,9)

    plt.bar(x, y,width=0.5, align='center', alpha=1)

    plt.ylabel(ylabel)
    plt.xlabel("Base pair position")
    plt.title(title)
    
    plt.savefig(outFile)

def illumina_qual_dist(r1, r2, r3, r4):
    qual_line = 3
    line_num = 0
    r1_mean = np.zeros(101)
    r2_mean = np.zeros(8)
    r3_mean = np.zeros(8)
    r4_mean = np.zeros(101)

    with gzip.open(r1,'r') as r1, gzip.open(r2,'r') as r2, gzip.open(r3,'r') as r3, gzip.open(r4,'r') as r4:
            for (r1_line, r2_line, r3_line, r4_line) in zip(r1, r2, r3, r4):

                if qual_line == line_num:
                    print(r1_line)
                    r1_line = r1_line.decode("utf-8").strip('\n')
                    print(r1_line)
                    r2_line = r2_line.decode("utf-8").strip('\n')
                    r3_line = r3_line.decode("utf-8").strip('\n')
                    r4_line = r4_line.decode("utf-8").strip('\n')
                    
                    index = 0
                    for (r1_base, r4_base) in zip(r1_line, r4_line):
                        r1_mean[index] += (ord(r1_base) - 33)
                        r4_mean[index] += (ord(r4_base) - 33)
                        index += 1

                    index = 0
                    for (r2_base, r3_base) in zip(r2_line, r3_line):
                        r2_mean[index] += (ord(r2_base) - 33)
                        r3_mean[index] += (ord(r3_base) - 33)
                        index += 1
                
                    qual_line += 4

                line_num +=1

    r1_mean = r1_mean/line_num
    r2_mean = r2_mean/line_num
    r3_mean = r3_mean/line_num
    r4_mean = r4_mean/line_num

    makeGraphs(np.array(range(101)), r1_mean, 'R1 Quality Distribution', 'Mean Quality Score','/Users/jonasgrove/bioinformatics/Bi622/demultiplexing-Jonasgrove/Assignment-the-first/r1_qc_graph')
    makeGraphs(np.array(range(8)), r2_mean, 'R2 Quality Distribution', 'Mean Quality Score','/Users/jonasgrove/bioinformatics/Bi622/demultiplexing-Jonasgrove/Assignment-the-first/r2_qc_graph')
    makeGraphs(np.array(range(8)), r3_mean, 'R3 Quality Distribution', 'Mean Quality Score','/Users/jonasgrove/bioinformatics/Bi622/demultiplexing-Jonasgrove/Assignment-the-first/r3_qc_graph')
    makeGraphs(np.array(range(101)), r4_mean, 'R4 Quality Distribution', 'Mean Quality Score','/Users/jonasgrove/bioinformatics/Bi622/demultiplexing-Jonasgrove/Assignment-the-first/r4_qc_graph')


def get_args():
    parser = argparse.ArgumentParser(description='Make kmer spectrum graph')
    parser.add_argument("-r1", "--read1", type=str, help='r1 read 1 file')
    parser.add_argument("-r2", "--index1", type=str, help='r2 index 1 file')
    parser.add_argument("-r3", "--index2", type=str, help='r3 index 2 file')
    parser.add_argument("-r4", "--read2", type=str, help='r4 read 2 file')

    return parser.parse_args()

parse_args = get_args()
r1_file    = parse_args.read1
r2_file    = parse_args.index1
r3_file    = parse_args.index2
r4_file    = parse_args.read2

illumina_qual_dist(r1_file, r2_file, r3_file, r4_file)

