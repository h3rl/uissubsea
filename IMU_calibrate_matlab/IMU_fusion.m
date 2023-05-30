%% Symbol definition
% Roll      phi         ɸ
% Pitch     theta       θ
% Yaw       psi         Ѱ

%% Calibration
% acc
% get bias over time by averaging
acc_raw = (acc_raw + bias)

acc_mps2 = earth_gravity*(acc_raw/pow2(15)) % assuming +-2g

%