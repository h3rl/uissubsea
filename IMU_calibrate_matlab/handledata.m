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
            yaw = pi/2;
        else
            yaw = 0;
        end
    else
        yaw = atan2(mag(2), mag(1));
    end
    
    % Wrap yaw to [0, 2*pi]
    if yaw < 0
        yaw = yaw + 2*pi;
    end
    
%     declanation = deg2rad(2.40);
%     yaw = yaw + declanation;

    % Wrap yaw to [0, 2*pi]
    if yaw < 0
        yaw = yaw + 2*pi;
    elseif yaw > 2*pi
        yaw = yaw - 2*pi;
    end


    fprintf("%.0f: (%.1f,%.1f,%.1f)\n",rad2deg(yaw),mag(1),mag(2),mag(3))
    ax = acc(1);
    ay = acc(2);
    az = acc(3);

    roll = atan2(ay, az);
    pitch = atan2(-ax, sqrt(ay * ay + az * az));
    q = quaternion([roll pitch yaw], "euler","XYZ","frame");
    
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