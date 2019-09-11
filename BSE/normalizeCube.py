# this file normalize the cube file by 
# summing over the charge in each voxel
# how to use: 
# just change the filename to your cube file
# name, a new file will be written
# author: Xingyu (Alfred) Liu
# email: xingyu.alfred.liu@gmail.com

import os

filename = '2444hole.cube'
with open(filename, 'r') as f:
    data = f.readlines()
print(data[:10])

for i, val in enumerate(data):
    data[i] = val[:-1].split()
print(data[:10])

for i, val in enumerate(data):
    if len(val) != 4 and len(val) != 5:
        startIndex = i
        print(i)
        break
    
accumu = 0
for i in range(startIndex, len(data)):
    for j in range(len(data[i])):
        accumu += float(data[i][j])
print('The total charge density is:', accumu)

for i in range(startIndex, len(data)):
    for j in range(len(data[i])):
        data[i][j] = str(float(data[i][j]) / accumu)

with open('tmp'+filename, 'w') as f:
    for i in range(len(data)):
        for j in range(len(data[i])):
            f.write(data[i][j]+'   ')
        f.write('\n')
