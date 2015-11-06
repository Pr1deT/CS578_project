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
            fr_mat[ind2][ind1] = None
            ind2 = ind2 + 1
        ind1 = ind1 + 1

    return fr_mat

# compute the four performance measurement
def get_perfor(predict, ground_truth):
    performance = {'true_positive':0, 'false_positive':0, 'false_negative':0, 'true_negative':0}

    true_label = get_label_set(ground_truth,1)
    predict_true_label = get_label_set(predict,1)
    false_label = get_label_set(ground_truth,0)
    predict_false_label = get_label_set(predict,0)

    p = predict_true_label.intersection(true_label)
    #print (9,78) in predict_true_label
    #print (9,78) in true_label
    #print (9,78) in p

    performance['true_positive'] = len(true_label&predict_true_label)
    performance['false_positive'] = len(false_label&predict_true_label)
    performance['false_negative'] = len(true_label&predict_false_label)
    performance['true_negative'] = len(false_label&predict_false_label)

    return performance

# get set for labels
def get_label_set(label_set, input_label):
    label_m = np.where(label_set == input_label)
    i = 0
    label = set()
    while i < len(label_m[0]):
        label.add((label_m[0][i],label_m[1][i])) #= predict_true_label + ()
        i = i + 1

    return label

# get groud truth of friendship
def get_fr_gt_mat(gt):
    #gt[np.isnan(gt)] = 0
    fr_mat = gt
    i = 0
    while i < len(gt):
        j = i
        while j < len(gt):
            if i == j:
                fr_mat[i][j] = 1
            elif gt[i][j] == 1:
                fr_mat[j][i] = 0
            elif gt[j][i] == 1:
                fr_mat[i][j] = 1
                fr_mat[j][i] = 0
            else:
                fr_mat[i][j] = 0
            j = j + 1
        i = i + 1

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
    fr_gt_mat = get_fr_gt_mat(ground_truth)
    # get accuracy
    performance = get_perfor(fr_mat, fr_gt_mat)
    print performance

    precision = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_positive'])
    recall = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_negative'])

    print 'precision: ', precision, ' recall: ', recall



if __name__ == '__main__':
    main()
