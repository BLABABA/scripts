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

# this should be part of the workflow ref
#atomSet = ('H', 'C', 'N', 'O', 'Si', 'P', 'S')

origin = Molecule.from_file('./data/mol2mol/centermol.xyz')
target = Molecule.from_file('./data/mol2mol/targetmol.xyz')

transVec = target.center_of_mass - origin.center_of_mass

eleCountDict = dict()
for ele in list(set(origin.species)):
    eleCountDict[ele] = origin.species.count(ele)
print("element: number")
for key, val in eleCountDict.items():
    print(key,":",val)
print(transVec)
sorted_elecount = sorted(eleCountDict.items(), key=lambda kv:kv[1])
sorted_dict = collections.OrderedDict(sorted_elecount)

print(sorted_dict)