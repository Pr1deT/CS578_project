## friendInfer_baseline.py
# ======================================================
# Function: Infer friendship between pair of individuals
#           using community labels
# Author: Ting Zhang
# Contact: zhan1013@purdue.edu
# ======================================================

import sys
import scipy.io as sio


## Feature Extraction

# Community label
# id 1 | commu_label

def feature_commu(num_ind, dataset):
    commu_label = [None] * num_ind
    i = 0
    while i < num_ind:
        commu_label[i] = dataset[i].my_affil
        i = i + 1

    return commu_label

# Read data from dataset_93.mat
def get_data(f_name):
    mat_content = sio.loadmat(f_name)





# main
def main():
    f_name = '../Data/dataset_93.mat'
    dataset = get_data(f_name)


if __name__ == '__main__':
    main()
