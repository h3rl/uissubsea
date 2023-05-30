


viewer = HelperOrientationViewer('Title',{'Orientation'});

% roll (x), pitch (Y), yaw (z)
% needs to be rad
roll = deg2rad(0);
pitch = deg2rad(0);
yaw = deg2rad(0);
q = quaternion([roll pitch yaw], "euler","XYZ","frame");
%e = eulerd(q, 'ZYX', 'frame');
%decl = -e(1)
viewer(q);
drawnow