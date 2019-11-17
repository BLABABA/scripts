from dbBinder import *
import os
import numpy as np
import math

database = dbcontrol('/projects/matml_aesp/database/CSD/pahs100')
database.loaddb()

#smdata = np.loadtxt('results.csv', delimiter=',', dtype='str')
#smdata = smdata[1:]

#with open('overlap.txt', 'r') as f:
#    data = f.readlines()
#data = data[1:]
#for i, val in enumerate(data):
#    data[i] = val.split()
#data = np.array(data)
#prediction = list()
#names = list()
#for i, line in enumerate(data):
#    if line[0] in smdata[:, 0]:
#        smindex = np.where(smdata[:, 0] == line[0])[0]
#        pred = -2.40*float(smdata[smindex][0][3]) - 0.82*(float(line[2])-2*float(line[1]) - float(smdata[smindex][0][2])) + 2.68
#        if not math.isnan(pred):
#            names.append(line[0])
#            prediction.append(pred)
#prediction = np.array(prediction).astype(str).reshape(-1, 1)
#names = np.array(names).reshape(-1, 1)
#output = np.concatenate((names, prediction), axis=1)
#np.savetxt('prediction.csv', output, delimiter=',', fmt='%s')
        

newdata = np.loadtxt('tmp.csv', delimiter='    ', dtype='str')
print(newdata)

dbkeys = ["bandgap", "Et", "DF", "VBdisp", "CBdisp", "hab", "gap_s", "Et_s", "DF_s", "IP_s", "EA_s", "polarisation", "apc", "density", "epsilon", "weight_s"]

datalist = []
for data in newdata:
    tmpdict = dict()
    tmpdict[data[0]] = dict()
    tmpdict[data[0]]['dft'] = dict()
    for i, key in enumerate(dbkeys):
        try:
            tmpdict[data[0]]['dft'][key] = float(data[i+2])
        except:
            pass
    tmpdict[data[0]]['gwbse'] = dict()
    tmpdict[data[0]]['gwbse']['DF'] = float(data[1])
    tmpdict[data[0]]['dbname'] = 'CSD'
    print(tmpdict)
    if data[0] not in database.db.keys():
        pass
    else:
        datalist.append(tmpdict)
database.writedata(datalist)
database.writedb(outpath='/projects/matml_aesp/database/CSD/pahs100test')
