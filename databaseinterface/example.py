from dbBinder import *
import os
import numpy as np
import math

def loaddft():
    newsampleID = np.loadtxt('/home/xingyu/software/JARVIS/jarvis/jarvis/sklearn/alldatafolder/all7391ids.csv', delimiter=' ', dtype='str')
    newsampledata = np.loadtxt('/home/xingyu/software/JARVIS/jarvis/jarvis/sklearn/alldatafolder/all7391data.csv', delimiter=',')
    # clean up newsample
    for i, val in enumerate(newsampleID):
        for j, c in enumerate(val):
            if c == '.':
                newsampleID[i] = val[:j]
                break
    datalist = list()
    for i, name in enumerate(newsampleID):
        tmpdict = dict()
        tmpdict[name] = {}
        tmpdict[name]['descriptors'] = {}
        tmpdict[name]['descriptors']['CFID'] = {}
        tmpdict[name]['descriptors']['CFID']['mean_chem'] = newsampledata[i][1:439].tolist()
        tmpdict[name]['descriptors']['CFID']['cell'] = newsampledata[i][439:443].tolist()
        tmpdict[name]['descriptors']['CFID']['mean_chg'] = newsampledata[i][443:821].tolist()
        tmpdict[name]['descriptors']['CFID']['rdf'] = newsampledata[i][821:921].tolist()
        tmpdict[name]['descriptors']['CFID']['adfa'] = newsampledata[i][921:1100].tolist()
        tmpdict[name]['descriptors']['CFID']['adfb'] = newsampledata[i][1100:1279].tolist()
        tmpdict[name]['descriptors']['CFID']['ddf'] = newsampledata[i][1279:1458].tolist()
        tmpdict[name]['descriptors']['CFID']['nn'] = newsampledata[i][1458:1558].tolist()

        tmpdict[name]['dft'] = {}
        tmpdict[name]['dft']['bandgap'] = float(newsampledata[i][0:1])
        tmpdict[name]['dft']['db'] = "CSD"
        datalist.append(tmpdict)
    
    return newsampleID, newsampledata, datalist

# put data into dict format
# load in feature data
def loaddata():
    newsampleID = np.loadtxt('/home/xingyu/software/JARVIS/jarvis/jarvis/sklearn/alldatafolder/newsample_IDs.csv', delimiter=' ', dtype='str')
    newsampledata = np.loadtxt('/home/xingyu/software/JARVIS/jarvis/jarvis/sklearn/alldatafolder/newsample_data.csv', delimiter=',')
    # clean up newsample
    for i, val in enumerate(newsampleID):
        for j, c in enumerate(val):
            if c == '.':
                newsampleID[i] = val[:j]
                break
    datalist = list()
    for i, name in enumerate(newsampleID):
        tmpdict = dict()
        tmpdict[name] = {}
        tmpdict[name]['descriptors'] = {}
        tmpdict[name]['descriptors']['CFID'] = {}
        tmpdict[name]['descriptors']['CFID']['mean_chem'] = newsampledata[i][0:438].tolist()
        tmpdict[name]['descriptors']['CFID']['cell'] = newsampledata[i][438:442].tolist()
        tmpdict[name]['descriptors']['CFID']['mean_chg'] = newsampledata[i][442:820].tolist()
        tmpdict[name]['descriptors']['CFID']['rdf'] = newsampledata[i][820:920].tolist()
        tmpdict[name]['descriptors']['CFID']['adfa'] = newsampledata[i][920:1099].tolist()
        tmpdict[name]['descriptors']['CFID']['adfb'] = newsampledata[i][1099:1278].tolist()
        tmpdict[name]['descriptors']['CFID']['ddf'] = newsampledata[i][1278:1457].tolist()
        tmpdict[name]['descriptors']['CFID']['nn'] = newsampledata[i][1457:1557].tolist()

        tmpdict[name]['dft'] = {}
        tmpdict[name]['dft']['db'] = "CSD"

        datalist.append(tmpdict)
    
    return newsampleID, newsampledata, datalist

if __name__ == "__main__":
    #newsampleID, newsampledata, datalist = loaddata()
    database = dbcontrol('db')
    database.loaddb()
    nested_key = ['dft', 'bandgap']
    bandgaps = database.getdata(nested_key)
    print(bandgaps)
    for key, val in database.db.items():
        print(key)
        print(val['dft']['bandgap'])
    
    # print('The length of datalist is')
    # print(len(datalist))
    # database.writedata(datalist)
    # database.writedb(outpath='/home/xingyu/matml_workflow/scripts/databaseinterface/harald95000_json')
