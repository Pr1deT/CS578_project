## friendInfer.py
# ======================================================
# Function: Infer friendship between pair of individuals
# Author: Ting Zhang
# Contact: zhan1013@purdue.edu
# ======================================================

import sys
import scipy.io as sio


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





# main
def main():
    dataset = get_data()


if __name__ == '__main__':
    main()
