%% convert roll, pitch, yaw to quaternion

% roll (x), pitch (Y), yaw (z)
% needs to be rad
cr = cos(roll*0.5);
sr = sin(roll*0.5);
cp = cos(pitch*0.5);
sp = sin(pitch*0.5);
cy = cos(yaw*0.5);
sy = sin(yaw*0.5);

qw = cr * cp * cy + sr * sp * sy;
qx = sr * cp * cy - cr * sp * sy;
qy = cr * sp * cy + sr * cp * sy;
qz = cr * cp * sy - sr * sp * cy;

q = quaternion(qw,qx,qy,qz);