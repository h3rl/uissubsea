clear all;
close all;
if ~exist('device', 'var')
    device = serialport("COM5", 115200);
end

magdata = [];
while true
    flush(device,"input");
    pause(0.02);
    if (device.NumBytesAvailable <= 0)
        continue;
    end
    
    line = readline(device);
    line = strip(line);
    a = split(line, ",");
    a = a(1:end-1);
    if~(numel(a) == 9)
        continue
    end
    b = str2double(a);
    %raw_acc = b(1:3);
    %raw_gyr = b(4:6);
    raw_mag = b(7:9);

    mag = raw_mag/pow2(15)*4;% gauss
    mag = mag*100;% uTesla
    
    x = mag(1,:)
    y = mag(2,:)
    z = mag(3,:)
    plot3(x,y,z,'r.');
    sz = size(magdata);
    s = sz(1)+1
    magdata(s,1)=x;
    magdata(s,2)=y;
    magdata(s,3)=z;

    hold on;

    Key=get(gcf,'CurrentKey');
    if strcmp(num2str(Key),'uparrow')==1
        break
    end
end
%% plot magdata
x = magdata(1,:);
y = magdata(2,:);
z = magdata(3,:);
plot3(x,y,z,'r.');