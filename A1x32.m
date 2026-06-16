%% 32ch_map

% A1x32 neuronexus probe map for KS 
chanMap = [ 13 20 9 24 4 29 8 25 7 26 6 27 5 28 3 30 2 31 1 32 10 23 11 22 12 21 14 19 15 18 16 17];
 
kcoords = ones(size(chanMap));
xcoords = num2cell(zeros(size(chanMap)));

ycoords_chs = 1500:-50:0; 
ycoords = num2cell(ycoords_chs);
connected = ones(size(chanMap));