from dbBinder import *
import os
import numpy as np
import math

smdata = np.loadtxt('results/results.csv', delimiter=',', dtype='str')
smdata = smdata[1:]

with open('results/overlap.txt', 'r') as f:
    data = f.readlines()
data = data[1:]
for i, val in enumerate(data):
    data[i] = val.split()
data = np.array(data)
prediction = list()
names = list()
for i, line in enumerate(data):
    if line[0] in smdata[:, 0]:
        smindex = np.where(smdata[:, 0] == line[0])[0]
        pred1 = -2.40*float(smdata[smindex][0][3]) - 0.82*(float(line[2])-2*float(line[1]) - float(smdata[smindex][0][2])) + 2.68
        pred2 = -6.20*float(smdata[smindex][0][3])/float(smdata[smindex][0][1]) - 0.71*(float(smdata[smindex][0][3])-float(smdata[smindex][0][2])) + 2.67
        pred3 = -5.70*float(smdata[smindex][0][4])/float(smdata[smindex][0][1]) - 0.91*(float(smdata[smindex][0][3])-float(smdata[smindex][0][2])) + 3.32
        #pred4 = -2.04*float(smdata[smindex][0][3]) - 0.66*(float(line[2])-2*float(line[1])-float(smdata[smindex][0][2]))
        if not math.isnan(pred1) and not math.isnan(pred2) and not math.isnan(pred3):
            names.append(line[0])
            prediction.append(pred1)
            prediction.append(pred2)
            prediction.append(pred3)
prediction = np.array(prediction).astype(str).reshape(-1, 3)
names = np.array(names).reshape(-1, 1)
output = np.concatenate((names, prediction), axis=1)

sortedindex = np.argsort(np.sum(output[:, 1:3].astype(float), axis=1))
output = output[sortedindex]

topones = np.array([]).reshape(0, 4)
print('Filtered by three models:')
for data in output:
    if float(data[1]) > -0.86 and float(data[2]) > -0.86 and float(data[3]) > -0.86:
        topones = np.concatenate((topones, data.reshape(-1, 4)), axis=0)

np.savetxt('prediction.csv', output, delimiter=',', fmt='%s')
np.savetxt('topones.csv', topones, delimiter=',', fmt='%s')
