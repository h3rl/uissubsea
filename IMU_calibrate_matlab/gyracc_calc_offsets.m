%% Symbol definition
% Roll      phi         ɸ
% Pitch     theta       θ
% Yaw       psi         Ѱ

clear all;
close all;
if ~exist('device', 'var')
    device = serialport("COM5", 115200);
end

dt = 0.1;
Fs = 1/dt;
%load("magcalib.mat");
load("magcalib_uT.mat");
% for plotting
viewer = HelperOrientationViewer('Title',{'AHRS Filter'});

% glob decl and initial vals, might set to first acc-pitch/roll
pitch = 0;
roll = 0;
FirstTime = true;
dt = 0.0
while true
    flush(device,"input");
    pause(dt);
    if (device.NumBytesAvailable <= 0)
        continue;
    end
    
    line = readline(device);
    line = strip(line);
    a = split(line, ",");
    a = a(1:end-1);
    if~(numel(a) == 9)
        continue;
    end
    b = str2double(a);
    if ~(sum(isnan(b)) == 0)
        continue;
    end
    raw_acc = b(1:3);
    raw_gyr = b(4:6);
    raw_mag = b(7:9);

    % only used if need dps, no need if trigfunc is used
    g = 9.81;
    acc = raw_acc/pow2(15)*2;% g
    acc = acc*g;% m/s2 
    gyr = raw_gyr/pow2(15)*245;% dps
    mag = raw_mag/pow2(15)*4;% gauss
    mag = mag*100;% uTesla
    mag = mag_transform*(mag-mag_center);
    %mag = [magx magy magz];
    if mag(1) == 0
        if mag(2) > 0
            mag_yaw = pi/2;
        else
            mag_yaw = 0;
        end
    else
        mag_yaw = atan2(mag(2), mag(1));
    end
    
    % Wrap yaw to [0, 2*pi]
    if mag_yaw < 0
        mag_yaw = mag_yaw + 2*pi;
    elseif mag_yaw > 2*pi
        mag_yaw = mag_yaw - 2*pi;
    end


    %fprintf("%.0f: (%.1f,%.1f,%.1f)\n",rad2deg(yaw),mag(1),mag(2),mag(3))
    rax = raw_acc(1);
    ray = raw_acc(2);
    raz = raw_acc(3);
    acc_roll = atan2(ray, raz);
    acc_pitch = atan2(-rax, sqrt(ray * ray + raz * raz));

    acc_roll = rad2deg(acc_roll);
    acc_pitch = rad2deg(acc_pitch);

    % comp filter roll and pitch with gyro
    gx = gyr(1);
    gy = gyr(2);
    gz = gyr(3);
    a = 0.01;

    if FirstTime
        FirstTime = false;
        pitch = acc_pitch;
        roll = acc_roll;
    else
        pitch = a*(gx*dt+pitch) + (1-a)*acc_pitch;
        roll = a*(gy*dt+roll) + (1-a)*acc_roll;
    end

    q = quaternion([pitch roll mag_yaw], "euler","XYZ","frame");

    mag_yaw = rad2deg(mag_yaw);
    fprintf("(%.1f,%.1f,%.1f)\n",acc_roll,acc_pitch,mag_yaw);
    
    %q = ecompass(acc.',mag.');
    %e = eulerd(q, 'ZYX', 'frame');
    %decl = -e(1)
    viewer(q);
    drawnow

    Key=get(gcf,'CurrentKey');
    if strcmp(num2str(Key),'uparrow')==1
        break
    end
end