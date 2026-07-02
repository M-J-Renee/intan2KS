%% 32ch_map

% A1x32 neuronexus probe map for KS
% Data is pre-reordered to physical spatial order in intan_batch2KS.m,
% so chanMap is sequential 1:32. ycoords reflect 50um site spacing.

n_ch = 32;

chanMap   = (1:n_ch)';
connected = true(n_ch, 1);
kcoords   = ones(n_ch, 1);
xcoords   = zeros(n_ch, 1);
ycoords   = (1550:-50:0)';   % 32 values, 50um spacing, tip=1550 base=0

save('A1x32.mat', 'chanMap', 'connected', 'kcoords', 'xcoords', 'ycoords');