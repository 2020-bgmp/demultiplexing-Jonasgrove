#!/usr/bin/env python
import record_class
import argparse
Record = record_class.Record


def get_records(r1_file, r2_file, r3_file, r4_file, index_file, q_cutoff, path_out):
    import gzip
    import itertools

    index_error_dic  = get_index_perms(index_file)

    with gzip.open(r1_file,'r') as r1, gzip.open(r2_file,'r') as r2, gzip.open(r3_file,'r') as r3, gzip.open(r4_file,'r') as r4:
        for (r1_line, r2_line, r3_line, r4_line) in zip(r1, r2, r3, r4):
           
            record_1  = ''.join([r1_line.decode("utf-8")] + [r1.readline().decode("utf-8") for i in range(3)])
            record_2  = ''.join([r2_line.decode("utf-8")] + [r2.readline().decode("utf-8") for i in range(3)])
            record_3  = ''.join([r3_line.decode("utf-8")] + [r3.readline().decode("utf-8") for i in range(3)])
            record_4  = ''.join([r4_line.decode("utf-8")] + [r4.readline().decode("utf-8") for i in range(3)])
            
            cur_record = Record(record_1, record_2, record_3, record_4)

            if cur_record.r2_score < q_cutoff or cur_record.r3_score < q_cutoff:
                print('if statement')
                out_file_r1 = path_out + '/r1_qc_trim.fastq'
                out_file_r4 = path_out + '/r4_qc_trim.fastq'
                with open(out_file_r1, 'w') as r1_out, open(out_file_r4, 'w') as r4_out:
                    r1_out.write(cur_record.r1_record)
                    r4_out.write(cur_record.r4_record)

            elif cur_record.error == True:
                print('elif statement')
                key = (cur_record.index_1, cur_record.index_2)
                if key in index_error_dic:
                    print('in dic')
                    out_file_r1 = path_out + '/r1_qc_hop.fastq'
                    out_file_r4 = path_out + '/r4_qc_hop.fastq'
                    index_error_dic[key] += 1
                else:
                    print('not in  dic')
                    out_file_r1 = path_out + '/r1_qc_trim.fastq'
                    out_file_r4 = path_out + '/r4_qc_trim.fastq'
                with open(out_file_r1, 'a') as r1_out, open(out_file_r4, 'a') as r4_out:
                    r1_out.write(cur_record.r1_record)
                    r4_out.write(cur_record.r4_record)

            else:
                print('else statement')
                out_file_r1 = path_out + '/' + cur_record.index_1 + '_r1.fastq'
                out_file_r4 = path_out + '/' + cur_record.index_2 + '_r4.fastq'
                with open(out_file_r1, 'a') as r1_out, open(out_file_r4, 'a') as r4_out:
                    r1_out.write(cur_record.r1_record)
                    r4_out.write(cur_record.r4_record)

    hop_count_file = open(path_out+'/hop_count.txt','w')
    for key in index_error_dic.keys():
        new_line = str(key) + '\t' + str(index_error_dic[key]) + '\n'
        hop_count_file.write(new_line)
    hop_count_file.close()

            

def get_index_perms(index_file):
    from itertools import permutations

    index_file = open(index_file, 'r')
    index_file.readline()
    index_list      = [line.split()[4] for line in index_file]
    index_error_dic = {}

    index_file.close()

    for perm in list(permutations(index_list, 2)):
        index_error_dic[perm] = 0
    
    index_file.close()
    return index_error_dic


def get_args():
    parser = argparse.ArgumentParser(description='Make kmer spectrum graph')
    parser.add_argument("-r1", "--read1", type=str, help='r1 read 1 file')
    parser.add_argument("-r2", "--index1", type=str, help='r2 index 1 file')
    parser.add_argument("-r3", "--index2", type=str, help='r3 index 2 file')
    parser.add_argument("-r4", "--read2", type=str, help='r4 read 2 file')
    parser.add_argument("-i", "--index_file", type=str, help='index file')
    parser.add_argument("-p", "--path_out", type=str, help='indicate director for output')
    parser.add_argument("-q", "--q_cutoff", type=int, help='index quality ')

    return parser.parse_args()

parse_args = get_args()
r1_file    = parse_args.read1
r2_file    = parse_args.index1
r3_file    = parse_args.index2
r4_file    = parse_args.read2
index_file = parse_args.index_file
path_out   = parse_args.path_out
q_cutoff   = parse_args.q_cutoff


get_records(r1_file, r2_file, r3_file, r4_file, index_file, q_cutoff, path_out)

