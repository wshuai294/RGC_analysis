#!/usr/bin/env python3

# require wgsim

import os
import numpy as np
import random


def get_abundance(num):
    # Set the parameters of the log-normal distribution
    mu = 0.0  # Mean of the logarithm of the distribution
    sigma = 1.0  # Standard deviation of the logarithm of the distribution

    # Generate random numbers from the log-normal distribution
    abundance = np.random.lognormal(mean=mu, sigma=sigma, size=1000)
    new_abun = abundance[:num]
    abundance = np.array(new_abun)/sum(new_abun)
    # print (abundance)
    return abundance

def get_sample(ID, bin_num):
    abundance = get_abundance(bin_num)
    random.shuffle(bins_list)
    select_bins = bins_list[:bin_num]
    sample_dir = outdir + "/" + ID
    os.system("mkdir %s"%(sample_dir))
    truth_file = sample_dir + "/" + ID + ".truth.csv"
    f = open(truth_file, 'w')
    

    for i in range(bin_num):
        the_bin = select_bins[i]
        bin_name = the_bin.split("/")[-1] 
        abun = abundance[i]
        read_pair_num = round(read_num * abun)

        print (bin_name, read_pair_num, abun, file = f)

        os.system(f"wgsim -S 6 -e 0 -1 150 -2 150 -r 0 -N {read_pair_num} {the_bin} {sample_dir}/{ID}_tem{i}.read1.fq {sample_dir}/{ID}_tem{i}.read2.fq")
    
    os.system(f"cat {sample_dir}/{ID}_tem*.read1.fq > {sample_dir}/{ID}.read1.fq")
    os.system(f"cat {sample_dir}/{ID}_tem*.read2.fq > {sample_dir}/{ID}.read2.fq")
    # os.system(f"rm {sample_dir}/{ID}_tem*.read*.fq")
    os.system(f"gzip -f {sample_dir}/{ID}.read*.fq")



if __name__ == "__main__":
    ## hyper parameters
    base_num = 10000000000 ## 10G base
    # base_num = 100000 ## 10G base
    bin_num = 10
    sample_num = 50
    outdir = "data/"  
    bin_file_list = "bins.list"  # each line is a path of a bin's fasta file


    read_num = round(base_num/(150*2)) ###150bp pair
    bins_list = []
    for line in open(bin_file_list):
        bins_list.append(line.strip())

    for i in range(sample_num):
        ID = f"rgc_meta_{i}"
        get_sample(ID, bin_num)

    
