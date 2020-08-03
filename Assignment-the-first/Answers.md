
## Part 1
1. Be sure to upload your Python script.


File Name   |   Label 
|---|---|
| r1_unit_test.fastq.gz | read 1 sequence |
| r2_unit_test.fastq.gz | index 1 (i5) |
| r3_unit_test.fastq.gz | index 2 (i7) |
| r4_unit_test.fastq.gz | read 2 sequence |
| illumina_qual_dist.py | processes 4 files at once |
| illumina_qual_dist_v2.py | processes 1 file at once |
| 1294_S1_L008_R1_001.fastq.gz | read 1 sequence | 
| 1294_S1_L008_R2_001.fastq.gz | index 1 (i5) |
| 1294_S1_L008_R3_001.fastq.gz | index 2 (i7) |
| 1294_S1_L008_R4_001.fastq.gz | read 2 sequence |

2. Per-base NT distribution
    1. ```![alt text](R1_quality_dist.png "Title")``
    2. ```![alt text](R2_quality_dist.png "Title")``
    3. ```![alt text](R3_quality_dist.png "Title")``
    4. ```![alt text](R4_quality_dist.png "Title")``

```i. Above```

```ii. R1: I think about 30, because this is what Illumina statess will contain ~95% of your reads, and based on the graphs the lowest average is about 30. This should allow for 95% retention of reads and alow for successful assembly ```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```R2: 20 or lower. The way the demultiplexing program works, if bases are not correct, they will be put into the error file because the indexes won't match, so a lower cutoff is fine```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```R3: 20 or lower for the same reason explained for R2```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```R4: I think about 30, because this is what Illumina statess will contain ~95% of your reads, and based on the graphs the lowest average is about 30. This should allow for 95% retention of reads and alow for successful assembly```

```iii. command : zcat r2_unit_test.fastq.gz | sed -n '2~4p' | grep 'N' | wc -l```\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```line count: 3976613 + 3328051 = 7,304,664 ```\=

## Part 2
1. Define the problem\
    ```//headed all 4 files and investigated format ```\
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```gzcat 1294_S1_L008_R[1-4]_001.fastq.gz | head```\
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```file 1 contains the read 1 biological sequence (R1)```\
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```file 2 contains the index 1 barcodes (R2)```\
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```file 3 contains the index 2 barcodes (R3) (reverse complement of index 1)```\
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ```file 4 contains the read 2 barcodes (R4)```
            
    ```//each record corresponds to the same read in each file so they must ```\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```be iterated through simutaneously for max efficiency```\
    ```//must organize reads from R1 and R4 files based on their barcode after verifying that the barcodes match between the R1 and R4 records.```

2. Describe output

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```//output will include;```\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```24 files for the R1 organized by index```\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```24 files for the R4 organized by index```\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```2 files for R1 and R4 non-matching indexes``` \
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```2 files for poor read quality data (averag phred to determine cutoff)```\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```1 file including: ```\
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;```index hop counts (all permutations of index) number of errors```\
``` ```
                        

3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [4 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
