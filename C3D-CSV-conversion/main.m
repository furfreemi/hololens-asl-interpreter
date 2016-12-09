test = c3dserver();
disp('Select C3D file for conversion.');
openc3d(test, 1);
targets = get3dtargets(test);
name = input('Enter name for this CSV file: ', 's');
name = strcat(name, '.csv');
struct2csv(targets,name)
disp('File saved to current folder. If you''re not sure what your current folder is, check Documents > MATLAB.');
