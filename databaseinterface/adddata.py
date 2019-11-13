from dbBinder import *
import os
import numpy as np
import math

database = dbcontrol('/projects/matml_aesp/database/CSD/pahs100')
database.loaddb()
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
    print(tmpdict)
    if data[0] not in database.db.keys():
        pass
    else:
        datalist.append(tmpdict)
database.writedata(datalist)
database.writedb(outpath='/projects/matml_aesp/database/CSD/pahs100test')
