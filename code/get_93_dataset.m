% get database of 93 subjects

load('../Data/realitymining.mat');

%network.sub_sort
%dataset_93 = {}
num_ind = 93;
dataset = s(1);
for i = 1:num_ind
    index = network.sub_sort(i);
    index
    dataset(i) = s(index);
end

%save('../Data/dataset_93.mat', 'dataset', '-v7.3');