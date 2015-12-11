## friendInfer.py
# ======================================================
# Function: Infer friendship between pair of individuals
# Author: Ting Zhang
# Contact: zhan1013@purdue.edu
# ======================================================

import sys
import scipy.io as sio
#from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt


## Feature Extraction

# 1. Bluetooth
# --------------------------------------------------
#      |            id 1                | id 2 | ...
# --------------------------------------------------
# id 1 | begin_time, end_time, duration |
# --------------------------------------------------
# id 2 |                                |
# --------------------------------------------------


def feature_bluetooth(dataset):
	pass

# Read data from realitymining.mat
def get_data(f_name):
    mat_content = sio.loadmat(f_name)
    return mat_content

# get_neighbor
def get_neighbor(net,vi):
    neighbor = np.nonzero(net[vi,:])[0]
    return neighbor

# Count shared neighbors of two nodes.
def count_shared_neighbor(net,vi,vj):
    neighbor_vi = get_neighbor(net,vi)
    neighbor_vj = get_neighbor(net,vj)
    num = len(set(neighbor_vi) & set(neighbor_vj))
    return num

# determine if two person are friends
def is_friend(net,vi,vj,thresh):
    num_shared = count_shared_neighbor(net,vi,vj)
    if num_shared > thresh:
        return 1
    else :
        return 0

# build friend network from bluetooth network
def get_friend_net(blue_net,thresh):
    num = blue_net.shape[0]
    friend_net = [[0 for x in range(num)] for x in range(num)]
    i=0
    while i < num-1:
        j=i
        while j < num:
            friend_net[i][j] = is_friend(blue_net,i,j,thresh)
            j = j + 1
        i = i + 1

    return friend_net

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

# read bluetooth network file
def get_blue_net(file_name):
    blue_net = genfromtxt(file_name, delimiter=',')
    return blue_net

# use svm
def get_friend_net_svm(data_85):
    # build training data
    train = data_85[1:len(data_85)/3,:]
    pass

# main
def main():
    # read bluetooth network
    file_name = '../Data/bluetooth_net.csv'
    blue_net = get_blue_net(file_name)

    # read ground truth for friendship
    gt_f_name = '../Data/friend_ground_truth_85.mat'
    gt_mat = get_data(gt_f_name)
    gt_key = 'friend_ground_truth'
    ground_truth = gt_mat[gt_key]

    # build friendship network
    thresh = 39
    friend_net = get_friend_net(blue_net,thresh)
    fr_net_mat = np.asarray(friend_net)
    fr_gt_mat = get_fr_gt_mat(ground_truth)

    # get performance
    performance = get_perfor(fr_net_mat, fr_gt_mat)
    print performance

    precision = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_positive'])
    recall = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_negative'])

    print 'stucture--precision: ', precision, ' recall: ', recall

    

if __name__ == '__main__':
    main()
