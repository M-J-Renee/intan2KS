%% 32ch_map

% A1x32 neuronexus probe map for KS 
Nchan = 32;

chanMap   = (1:Nchan)';
connected = true(Nchan,1);
xcoords   = zeros(Nchan,1);
ycoords   = zeros(Nchan,1);
kcoords   = ones(Nchan,1);

physical_order = [ ...
13 20 9 24 4 29 8 25 7 26 6 27 5 28 ...
3 30 2 31 1 32 10 23 11 22 12 21 ...
14 19 15 18 16 17];

spacing = 50; % µm
depths = (0:Nchan-1)' * spacing;   

for i = 1:Nchan
    ch = physical_order(i);
    ycoords(ch) = depths(i);
end

save('A1x32.mat', ...
    'chanMap','connected','xcoords','ycoords','kcoords');