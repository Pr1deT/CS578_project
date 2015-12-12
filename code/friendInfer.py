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
from sklearn import svm


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
    feature = [[0 for x in range(num)] for x in range(num)]
    i=0
    while i < num-1:
        j=i
        while j < num:
            friend_net[i][j] = is_friend(blue_net,i,j,thresh)
            feature[i][j] = count_shared_neighbor(blue_net,i,j)
            j = j + 1
        i = i + 1
    np.savetxt("../Data/feature_share.csv", feature, delimiter=",")
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
    flag = 0;
    #build training data
    if flag==1:
        col = data_85.shape[1]
        index_false = []
        index_true = []
        i = 0
        while i < data_85.shape[0]:
            if data_85[i][col-1] == 1:
                index_true = index_true + [i]
            else:
                index_false = index_false + [i]
            i = i + 1
        num_of_train = 15
        train_index = index_true[0:14]+index_false[0:140]
        train = data_85[train_index,:]
    else:
        train = data_85[1:data_85.shape[0]/3,:]
    trainX = train[:,2:train.shape[1]-1]
    trainY = train[:,train.shape[1]-1]

    testX = data_85[:,2:data_85.shape[1]-1]
    testY = data_85[:,data_85.shape[1]-1]

    # test feature
    trainX = train[:,3:train.shape[1]-1]
    testX = data_85[:,3:train.shape[1]-1]

    # fit the model
    clf = svm.SVC(kernel='rbf',class_weight={1: 10})
    clf.fit(trainX, trainY)
    # test
    y_pred_train = clf.predict(trainX)
    y_pred_test = clf.predict(testX)

    # compute performance
    performance = {'true_positive':0, 'false_positive':0, 'false_negative':0, 'true_negative':0}

    true_label = np.nonzero(testY)[0]
    predict_true_label = np.nonzero(y_pred_test)[0]
    bindices_zero = (testY == 0)
    false_label = np.arange(len(testY))[bindices_zero]
    bindices_zero = (y_pred_test == 0)
    predict_false_label = np.arange(len(y_pred_test))[bindices_zero]

    performance['true_positive'] = len(set(true_label)&set(predict_true_label))
    performance['false_positive'] = len(set(false_label)&set(predict_true_label))
    performance['false_negative'] = len(set(true_label)&set(predict_false_label))
    performance['true_negative'] = len(set(false_label)&set(predict_false_label))

    #build network
    #num = data_85.shape[0]
    #friend_net = [[0 for x in range(num)] for x in range(num)]
    #k=0
    #while k < len(y_pred_test):
    #    i=data_85[k,0]
    #    j=data_85[k,1]
    #    friend_net[int(i-1)][int(j-1)] = y_pred_test[k]
    #    k = k + 1

    return performance

# use hybrid
def get_friend_net_hybrid(data_85,feature_share):
    # build feature tuple
    feature_new = [[0 for x in range(data_85.shape[1]+1)] for x in range(data_85.shape[0])]
    i = 0
    while i < len(feature_new):
        p = int(data_85[i][0] - 1)
        q = int(data_85[i][1] - 1)
        feature_new[i][1:data_85.shape[1]-1] = data_85[i,1:data_85.shape[1]-1]
        feature_new[i][len(feature_new[0])-2] = feature_share[p][q]
        feature_new[i][len(feature_new[0])-1] = data_85[i][data_85.shape[1]-1]
        i = i + 1

    # svm
    friend_net = get_friend_net_svm(np.asarray(feature_new))

    return friend_net


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

    # use svm
    # build friendship network
    data_85 = get_blue_net('../Data/feature_85.csv')
    performance = get_friend_net_svm(data_85)

    precision = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_positive'])
    recall = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_negative'])
    print performance
    print 'svm--precision: ', precision, ' recall: ', recall

    # hybrid
    # use number of same neighbor as a feature in svm
    file_name = '../Data/feature_share.csv'
    feature_share = get_blue_net(file_name)

    performance = get_friend_net_hybrid(data_85,feature_share)

    precision = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_positive'])
    recall = 1.0 * (performance['true_positive'])/(performance['true_positive']+performance['false_negative'])
    print performance
    print 'hybrid--precision: ', precision, ' recall: ', recall

if __name__ == '__main__':
    main()
