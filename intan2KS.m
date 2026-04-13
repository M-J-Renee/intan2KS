%% kilosort pipeline

clear;
close all;
clc;

%% load data

Epth = '/Volumes/homes/Caras Lab/RIG3_Backup_2025/intan_files/Data/SUBJ-ID-1154/SUBJ-ID-1154_shaping_260408_100339';

%% load data

[Y, events, info] = intan2matlab(Epth, ...
    "dataTypeOut", "BROADBAND");

%% preprocessing

data_int16 = int16(Y.BROADBAND); %convert to int16 binary

ephys_size = size(data_int16, 2); % how many channels 

    if ephys_size == 64
    chan_order = [8 58 16 50 7 57 15 50 13 51 11 53 9 55 5 59 3 61 1 63 14 52 12 54 10 56 6 60 4 62 2 64];    
    elseif ephys_size == 32 
    chan_order = [13 20 9 24 4 29 8 25 7 26 6 27 5 28 3 30 2 31 1 32 10 23 11 22 12 21 14 19 15 18 16 17];
    elseif ephys_size == 16 
    chan_order = [9 8 11 6 12 5 16 1 13 4 14 3 15 2 10 7];
    end

    data_int16 = data_int16(:, chan_order); 

%% write file


%parse subj-id and session

fid = fopen('combined.dat','w');
fwrite(fid, data_int16', 'int16');  
fclose(fid);

%% run kilosort 