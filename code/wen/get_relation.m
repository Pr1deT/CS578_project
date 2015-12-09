
load('../../Data/dataset_93.mat');

offset = 1;
errIdx = [52,89,91,92,93];
relation = zeros(88,88);
community = [];
member = zeros(88,1);

for i = 1:93  %%for each user
    if(~ismember(i,errIdx))
        member(offset,1) = dataset(i).mac;
        community = [community; dataset(i).my_affil];
        offset = offset + 1;
    end
end

offset = 1;

for i = 1:93  %%for each user
    if(~ismember(i,errIdx))
        datasize = size(dataset(i).device_macs);
        for j = 1:datasize(1,2) %%for each scan
            mac = dataset(i).device_macs(j);
            if(isempty(mac))
                continue
            end
            val = mac{:};
            scansize = size(val);
            for k = 1:scansize(1,2) %%for each mac
                row = find(member == val(k));
                if(~isempty(row))
                    relation(offset,row) = relation(offset,row)+1;
                end
            end
        end
        offset = offset + 1;
    end
    %disp(relation)
end
%disp(relation)
disp(community)
%csvwrite('relation.csv',relation);


                
        