#!/usr/bin/env python
import record_class
import argparse
Record = record_class.Record

def get_index_perms(index_file):
    from itertools import permutations

    index_file = open(index_file, 'r')
    index_file.readline()
    index_seq_list = []
    index_name_dic = {}         #{AGTC:J9}
    for line in index_file:
        line = line.strip('\n').split()
        seq = line[4]
        name = line[3]
        index_seq_list.append(seq)
        index_name_dic[seq] = name

    index_count_dic = {index:0 for index in index_seq_list}   #{AGTC:count}
    index_error_dic = {perm:0 for perm in list(permutations(index_seq_list, 2))}

    index_file.close()

    for perm in list(permutations(index_seq_list, 2)):
        index_error_dic[perm] = 0
    
    index_file.close()
    return index_error_dic, index_count_dic, index_name_dic

def files_dic(index_file, path, extension):
    index_file = open(index_file, 'r')
    index_file.readline()
    file_dic = {}                           #dictionary {index_string: file_variable}

    for line in index_file:
        line = line.strip('\n').split()
        index_name, index_seq = line[3], line[4]
        file_name = path + '/' + index_name + '_' + index_seq + '_' + extension + '.fastq' #path/C9_AGTC_r1.fastq
        file_dic[index_seq] = open(file_name, 'w')

    index_file.close()
    return file_dic    
    
def get_index_ratios(index_count_dic, num_records_out):
    for index in index_count_dic:
        index_count_dic[index] = (index_count_dic[index]/num_records_out)*100
    return index_count_dic

def make_out_report(total_index_swapping, num_records_out, index_ratios, index_name_dic, total_error, path_out):
    out_report_file = open(path_out + '/dm_report.txt', 'w')
    out_report_file.write('Total Reads Retained: ' + str(num_records_out) + '\n')
    out_report_file.write('Total Index Hopping: ' + str(total_index_swapping) + '\n')
    out_report_file.write('Total Error Records: ' + str(total_error) + '\n')
    out_report_file.write('sample_ID    sequence    sample_percentage\n')
    for index_seq in index_ratios.keys():
        new_line = index_name_dic[index_seq] + '    ' + index_seq + '   ' + str(index_ratios[index_seq]) + '\n'
        out_report_file.write(new_line)
    out_report_file.close()

def get_records(r1_file, r2_file, r3_file, r4_file, index_file, q_cutoff, path_out):
    import gzip
    import itertools

    index_error_dic, index_count_dic, index_name_dic  = get_index_perms(index_file)

    #open 42 files
    r1_file_dic = files_dic(index_file, path_out, 'r1')
    r4_file_dic = files_dic(index_file, path_out, 'r4')
    r1_ihop_file = open(path_out + '/r1_ihop.fastq', 'w')
    r4_ihop_file = open(path_out + '/r4_ihop.fastq', 'w')
    r1_er_file = open(path_out + '/r1_error.fastq', 'w')
    r4_er_file = open(path_out + '/r4_error.fastq', 'w')

    #counts
    total_index_swapping = 0
    num_records_out = 0
    total_error = 0

    with gzip.open(r1_file,'r') as r1, gzip.open(r2_file,'r') as r2, gzip.open(r3_file,'r') as r3, gzip.open(r4_file,'r') as r4:
        for (r1_line, r2_line, r3_line, r4_line) in zip(r1, r2, r3, r4):
           
            record_1  = ''.join([r1_line.decode("utf-8")] + [r1.readline().decode("utf-8") for i in range(3)])
            record_2  = ''.join([r2_line.decode("utf-8")] + [r2.readline().decode("utf-8") for i in range(3)])
            record_3  = ''.join([r3_line.decode("utf-8")] + [r3.readline().decode("utf-8") for i in range(3)])
            record_4  = ''.join([r4_line.decode("utf-8")] + [r4.readline().decode("utf-8") for i in range(3)])
            
            cur_record = Record(record_1, record_2, record_3, record_4)
    
            if cur_record.r2_score < q_cutoff or cur_record.r3_score < q_cutoff:
                r1_er_file.write(cur_record.r1_record)
                r4_er_file.write(cur_record.r4_record)
                total_error += 1

            elif cur_record.error == True or cur_record.index_1 not in index_count_dic:
                key = (cur_record.index_1, cur_record.index_2)
                if key in index_error_dic:
                    r1_ihop_file.write(cur_record.r1_record)
                    r4_ihop_file.write(cur_record.r4_record)
                    index_error_dic[key] += 1
                    total_index_swapping += 1
                else:
                    r1_er_file.write(cur_record.r1_record)
                    r4_er_file.write(cur_record.r4_record)
                    total_error += 1

            else: 
                r1_file_dic[cur_record.index_1].write(cur_record.r1_record)
                r4_file_dic[cur_record.index_1].write(cur_record.r4_record)
                index_count_dic[cur_record.index_1] += 1
                num_records_out += 1
        

    if num_records_out != 0:
        index_count_dic = get_index_ratios(index_count_dic, num_records_out)  
     

    ###close all 48 files in for loop
    for r1_key, r4_key in zip(r1_file_dic.keys(), r4_file_dic.keys()):
        r1_file_dic[r1_key].close()
        r4_file_dic[r4_key].close()

    hop_count_file = open(path_out+'/hop_count.txt','w')
    for key in index_error_dic.keys():
        new_line = str(key) + '\t' + str(index_error_dic[key]) + '\n'
        hop_count_file.write(new_line)
    hop_count_file.close()

    r1_ihop_file.close()
    r4_ihop_file.close()
    r1_er_file.close()
    r4_er_file.close()

    make_out_report(total_index_swapping, num_records_out, index_count_dic, index_name_dic, total_error, path_out)

    return None




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

