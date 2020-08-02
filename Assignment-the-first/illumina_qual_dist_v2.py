#!/usr/bin/env python

import itertools
import gzip
import numpy as np
import argparse

def makeGraphs(x,y,title,ylabel,outFile):
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = (15,9)

    plt.bar(x, y,width=0.5, align='center', alpha=1)

    plt.ylabel(ylabel)
    plt.xlabel("Base pair position")
    plt.title(title)
    
    plt.savefig(outFile)

def illumina_qual_dist(file_in, file_out, seq_length, title):
    qual_line = 3
    line_num = 0
 
    mean = np.zeros(seq_length)
  

    with gzip.open(file_in,'r') as file_in:
            for line in file_in:

                if qual_line == line_num:
                    line = line.decode("utf-8").strip('\n')
                    
                    for index, phred in enumerate(line):
                        mean[index] += (ord(phred) - 33)
                
                    qual_line += 4

                line_num +=1

    mean = mean/(line_num/4)
    makeGraphs(np.array(range(seq_length)), mean, title, 'Mean Quality Score', file_out)


def get_args():
    parser = argparse.ArgumentParser(description='Make kmer spectrum graph')
    parser.add_argument("-f", "--file_in", type=str, help='file in')
    parser.add_argument("-o", "--file_out", type=str, help='file out')
    parser.add_argument("-l", "--seq_length", type=int, help='length of sequence')
    parser.add_argument("-t", "--title", type=str, help='title for graphs')

    return parser.parse_args()

parse_args = get_args()
title      = parse_args.title
file_in    = parse_args.file_in
file_out   = parse_args.file_out
seq_length = parse_args.seq_length

illumina_qual_dist(file_in, file_out, seq_length, title)

