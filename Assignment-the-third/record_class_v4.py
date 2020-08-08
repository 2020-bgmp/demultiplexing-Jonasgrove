#!/usr/bin/env python

class Record:

    def __init__(self, r1, r2, r3, r4, limit):
        self.limit      = limit
        self.index_1    = r2.split('\n')[1].strip('\n')
        self.index_2    = self.rev_comp(r3.split('\n')[1].strip('\n'))
        self.index_pair = self.index_1 + '-' + self.index_2
        
        self.r1_score = self.avgQscore(r1)
        self.r2_score = self.avgQscore(r2)
        self.r3_score = self.avgQscore(r3)
        self.r4_score = self.avgQscore(r4)
        
        self.r1_record = self.add_index_head(r1)
        self.r2_record = self.add_index_head(r2)
        self.r3_record = self.add_index_head(r3)
        self.r4_record = self.add_index_head(r4)

        self.error      = self.check_error()

    def avgQscore(self, record):
        seq        = record.split('\n')[3].strip('\n')
        total_seq  = 0
        seq_length = 0
        for char in seq:
            value = ord(char) - 33
            total_seq += (value)
            seq_length += 1
        
        return total_seq/seq_length

    def rev_comp(self, seq):
        rc_seq   = ''
        seq_dict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
        for char in seq:
            rc_seq = seq_dict[char] + rc_seq
        
        return rc_seq
    
    def add_index_head(self, record):
        record_list           = record.split('\n')
        head_line             = record_list[0].strip('\n') + ' ' + self.index_pair
        record_list[0]        = head_line
        record_w_index_header = '\n'.join(record_list)

        return record_w_index_header

    def check_error(self):

        if self.index_1 != self.index_2:
            error = True
        elif 'N' in self.index_1 or 'N' in self.index_2:
            error = True
        elif self.r2_score < self.limit or self.r2_score < self.limit:
            error = True
        else:
            error = False
        
        return error

















'''
record = Record('headr1\nAAAAAAAAAAAAAAAAAAAAAA\n+\n#AA<FJJJ', 'headr1\nGGGG\n+\n####', 'headr1\nCCCC\n+\n####', 'headr1\nCCCCCCCCCCCCCCCCCCCCC\n+\n####')

print("r1", record.r1_record)
print("r2", record.r2_record)
print("r3", record.r3_record)
print("r4", record.r4_record)

print("r1 score", record.r1_score) 
print("r2 score", record.r2_score) 
print("r3 score", record.r3_score) 
print("r4 score", record.r4_score) 

print('index1', record.index_1)
print('index2', record.index_2)

print(record.error)

newheader = record.add_index_head(record.r1_record)
print('')
print(newheader)
'''