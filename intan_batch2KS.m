%% convert a group of recordings to KS binary format
clear;
close all;
clc;

%% path

Edir = '/Volumes/homes/Caras Lab/RIG3_Backup_2025/intan_files/Data/SUBJ-ID-1154';
outputdir = '/Users/marissarenee/Desktop/test';

%% load data

% list all folders
d = dir(Edir);
d = d([d.isdir]);
d = d(~ismember({d.name},{'.','..'}));

for i = 1:length(d)

    sessionName = d(i).name;
    Epth = fullfile(Edir, sessionName);
    outDir = Epth;

    fprintf('Processing: %s\n', sessionName);

    try
        % load data
        [Y, events, info] = intan2matlab(Epth, ...
            "dataTypeOut", "BROADBAND");

        % preprocessing
        data_int16 = int16(Y.BROADBAND);

        ephys_size = size(data_int16, 2);

        if ephys_size == 64
            chan_order = [8 58 16 50 7 57 15 50 13 51 11 53 9 55 5 59 3 61 1 63 14 52 12 54 10 56 6 60 4 62 2 64];
        elseif ephys_size == 32
            chan_order = [13 20 9 24 4 29 8 25 7 26 6 27 5 28 3 30 2 31 1 32 10 23 11 22 12 21 14 19 15 18 16 17];
        elseif ephys_size == 16
            chan_order = [9 8 11 6 12 5 16 1 13 4 14 3 15 2 10 7];
        else
            error('Unexpected channel count: %d', ephys_size);
        end

        data_int16 = data_int16(:, chan_order);

        % write file
        outFile = fullfile(outputdir, [sessionName '.dat']);

        fid = fopen(outFile,'w');
        fwrite(fid, data_int16', 'int16');
        fclose(fid);

        fprintf('Saved: %s\n', outFile);

    catch ME
        fprintf('FAILED: %s\n', sessionName);
        disp(ME.message);
        continue;
    end

end