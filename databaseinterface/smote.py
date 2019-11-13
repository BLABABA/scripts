from dbBinder import *
import os
import numpy as np
import math
from imblearn.over_sampling import SMOTE, ADASYN


def extractFeatures(db):
    X = list()
    y = list()
    for name in db.keys():
        tmpX = db[name]['descriptors']['CFID']['mean_chem'].copy()
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['cell']))
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['mean_chg']))
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['rdf']))
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['adfa']))
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['adfb']))
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['ddf']))
        tmpX = np.concatenate((tmpX, db[name]['descriptors']['CFID']['nn']))
        tmpX = tmpX.reshape(1, -1)
        X.append(tmpX)
        y.append(db[name]['dft']['bandgap'])
    X = np.array(X)
    y = np.array(y)
    return X.reshape(-1, 1557), y.reshape(-1, 1)


#database = dbcontrol('/projects/matml_aesp/database/OMDB/r_omdb7371')
#database.loaddb()
#print('The length of datalist is')
#print(database.db.keys())

#X, y = extractFeatures(database.db)

#X_resampled, y_resampled = SMOTE().fit_resample(X, y)

