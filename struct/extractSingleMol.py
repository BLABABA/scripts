from dbaAutomator.functions import *
from dbaAutomator.ref import *
from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen import Molecule
import os
import numpy as np

inpath = "./data/crystals"
namelist = os.listdir(inpath)
outpath = "./data/singmol"


nocando = []
for name in namelist:
    structID = name[:-3]
    print(structID)
    struct = read(os.path.join(inpath, name))
    struct = AseAtomsAdaptor.get_structure(struct)
    struct.make_supercell([4, 5, 7])
    bondDict = getBondDict(struct, bondCutoff)
    print(bondDict)
    try:
        singleMol = getCentralSingleMol(struct, bondDict)
        #singleMol.to(filename=outpath+"/"+structID+".xyz")
        mol = Molecule([], [])
        for site in singleMol.items():
            mol.append(str(site[1].specie), site[1].coords)
        mol.to(filename=outpath+"/"+structID+"xyz")
    except:
        nocando.append(structID)

print(nocando)
nocando = np.array(nocando)
np.savetxt('nocandolist.csv', nocando, delimiter=' ', fmt='%s')
