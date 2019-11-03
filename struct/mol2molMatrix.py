"""

This function extract all fragments and 
compute the rotational matrix from origin
to the target

Some thoughts:
    - use the single unique atom as an anchor first
    - use the smallest number of this specy and its cloest atoms  as anchor

"""

from dbaAutomator.functions import *
from dbaAutomator.ref import *
from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen import Molecule
import os
import numpy as np
import operator
import collections

def prettyPrint(pdict):
    for key, val in pdict.items():
        print(key, ":", val)

# this should be part of the workflow ref
atomList = ['Si', 'C', 'P', 'N', 'S', 'O']

origin = Molecule.from_file('./data/mol2mol/centermol.xyz')
target = Molecule.from_file('./data/mol2mol/targetmol.xyz')

transVec = target.center_of_mass - origin.center_of_mass

eleCountDict = collections.OrderedDict()
for ele in list(set(origin.species)):
    if origin.species.count(ele) == 1:
        eleCountDict[ele] = origin.species.count(ele)

def getMolVec(mol, singAtomDict):
    molVec = np.array([])
    # list of index indicating those atoms used in building the vector
    indexVecList = list()
    for key in singAtomDict.keys():
        index = mol.species.index(key)
        indexVecList.append(index)
        vec = (mol.sites[index].coords - mol.center_of_mass)
        molVec = np.concatenate((molVec, vec))
    if molVec.shape[0] == 9:
        return molVec.reshape(-1, 3)
    else:
        newmol = mol.copy()
        newmol.append("He", mol.center_of_mass)
        donesite = []
        for index in indexVecList:
            donesite.append(mol.sites[index])
        startsite = newmol.sites[-1]
        donesite.append(startsite)
        distSortIndex = np.argsort(newmol.distance_matrix[-1])
        for index in distSortIndex:
            if not newmol.sites[index] in donesite:
                molVec = np.concatenate((molVec, (newmol.sites[index].coords - mol.center_of_mass)))
                donesite.append(newmol.sites[index])
            if molVec.shape[0] == 9:
                break
        return molVec.reshape(-1, 3)

molVec = getMolVec(origin, eleCountDict)
print(molVec)