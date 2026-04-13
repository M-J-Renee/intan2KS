%% 16ch_map

% A1x16 neuronexus probe map for KS 
         shank_chs = [7 10 2 15 3 14 4 13 1 16 5 12 6 11 8 9];
 
         kcoords_map = num2cell(shank_chs);
         xcoords_map = num2cell(zeros(size(shank_chs)));

         ycoords_chs = 1500:-100:0; 
         ycoords_map = num2cell(ycoords_chs);