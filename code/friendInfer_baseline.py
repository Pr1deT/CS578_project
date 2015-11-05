## friendInfer_baseline.py
# ======================================================
# Function: Infer friendship between pair of individuals
#           using community labels
# Author: Ting Zhang
# Contact: zhan1013@purdue.edu
# ======================================================

import sys
import scipy.io as sio
import numpy as np


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
    return mat_content

## Baseline method to infer friendship, soly dependent on community label

def is_friend(ind1,ind2,community):
    #community = community.tolist()
    if community[ind1]==community[ind2]:
        return 1
    else:
        return 0

def friend_matrix(community):
    fr_mat = np.zeros(shape=(len(community),len(community)))

    ind1 = 0
    while ind1 < len(community):
        ind2 = ind1
        while ind2 < len(community):
            fr_mat[ind1][ind2] = is_friend(ind1, ind2, community)
            ind2 = ind2 + 1
        ind1 = ind1 + 1

    return fr_mat



# main
def main():

    # read ground truth for friendship
    gt_f_name = '../Data/friend_ground_truth.mat'
    gt_mat = get_data(gt_f_name)
    gt_key = 'friend_ground_truth'
    ground_truth = gt_mat[gt_key]

    # read community label
    commu_f_name = '../Data/community.mat'
    commu_mat = get_data(commu_f_name)
    #num_ind = len(dataset)
    commu_key = 'community'
    community = commu_mat[commu_key]

    # get baseline accuracy for friendship inference
    fr_mat = friend_matrix(community)

    print fr_mat




if __name__ == '__main__':
    main()
