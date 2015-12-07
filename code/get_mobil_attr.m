% get attributes from phone logs
% # of voice calls
% night-call ratio
% call duration: total duration

load('../Data/dataset_93.mat','dataset');

attr = [];

% iterate through every subject data
for i = 1:numel(dataset)
    subject = dataset(i);
    logs = subject.comm;
    numOfCalls = containers.Map;
    % iterate through every phone log
    for j = 1:numel(logs)
        contact = logs(j).contact;
        if contact ~= -1
            if isKey(numOfCalls,num2str(contact))
                numOfCalls(num2str(contact)) = numOfCalls(num2str(contact))+1;
            else
                numOfCalls(num2str(contact)) = 1;
            end
        end
    end
    
    % store as one attribute
    allKeys = keys(numOfCalls);
    for j = 1:numel(allKeys)
        oneKey = allKeys(j);
        oneEntry = [i,str2double(oneKey),numOfCalls(char(oneKey))];
        attr = [attr;oneEntry];
    end
end

