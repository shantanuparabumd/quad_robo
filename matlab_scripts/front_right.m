% Create the robot model
Ld0 = Link('d', 0, 'a', 0, 'alpha', pi/2);
L0 = Link('d', 0, 'a', 0, 'alpha', 0);
Ld1 = Link('d', -0.06485, 'a', 0, 'alpha', -pi/2);
L1 = Link('d', 0.14, 'a', 0, 'alpha', 0);
Ld2 = Link('d', 0, 'a', 0.5, 'alpha', 0);
L2 = Link('d', 0, 'a', 0, 'alpha', 0);
L3 = Link('d', 0, 'a', 0.45, 'alpha', 0);


robot = SerialLink([Ld0 L0 Ld1 L1 Ld2 L2 L3]);
robot.teach
% Define the joint angles
