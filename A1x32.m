%% 32ch_map

% A1x32 neuronexus probe map for KS 
shank_chs = [ 13 20 9 24 4 29 8 25 7 26 6 27 5 28 3 30 2 31 1 32 10 23 11 22 12 21 14 19 15 18 16 17];
 
kcoords_map = ones(size(shank_chs));
xcoords_map = num2cell(zeros(size(shank_chs)));

ycoords_chs = 1500:-50:0; 
ycoords_map = num2cell(ycoords_chs);