# this script is used to plot the bandstructure for results from BerkeleyGW
# the inputs are the bandstructure.dat file and the kpoints file
# KAGFOP

import matplotlib.pyplot as plt
import numpy as np
import math

titlename = "OBOHUL"
# load data
# banddata is the raw bandstructure data
# kpoints is the kpoints raw data
banddata = np.loadtxt('bandstructure.dat', dtype=float)
with open ('kpoints', 'r') as f:
    kpoints = f.readlines()
interList = []
highsimPoint = []
for i, val in enumerate(kpoints):
    line = val.split()
    if len(line) == 0:
        break
    elif len(line) == 1:
        interList.append(int(line[0]))
    else:
        name = str(line[-1][2:])
        for i, char in enumerate(name):
            if char.isdigit():
                name = name[:i] + "_" + name[i:]
                break
        highsimPoint.append(name)
print("The high symmetry points are:", highsimPoint)
print("The invervals between each pair of points are:", interList)

# now get the shift point index and the kpoint index
shiftIndex = []
kpointIndex = [0]
counter = 0
for i, val in enumerate(interList):
    if val != 0:
        counter += (val + 1)
        kpointIndex.append(counter)
    else:
        counter += 1
        shiftIndex.append(counter)
print("The shift index are:", shiftIndex)
print('The kpoint index are:', kpointIndex)
kpointName = []
i = 0
while i < len(interList):
    if interList[i] != 0:
        kpointName.append(highsimPoint[i])
        i += 1
    else:
        kpointName.append(highsimPoint[i]+highsimPoint[i+1])
        i += 2
kpointName.append(highsimPoint[-1])
print("The kpoint names to be printed are:", kpointName)

# get the number of points in one band
numPoint = 1
for i in range(len(banddata)):
    if banddata[i+1][1] != banddata[i][1]:
        break
    else:
        numPoint += 1
# create a data array for band data
QPband = np.zeros(shape=(numPoint, 1))
# this is the list for special points

for i in range(numPoint):
    if i == 0:
        QPband[i][0] == 0
    elif i in shiftIndex:
        QPband[i][0] = QPband[i-1][0]
    else:
        QPband[i][0]=math.sqrt((abs(banddata[i][2])-abs(banddata[i-1][2]))**2+
              (abs(banddata[i][3])-abs(banddata[i-1][3]))**2 +
              (abs(banddata[i][4])-abs(banddata[i-1][4]))**2) + QPband[i-1][0]
# the MF band
MFband = np.copy(QPband)
# insert the band values, this is the QP band
for i in range(int(len(banddata)/numPoint)):
    newcol = banddata[i*numPoint:(i+1)*numPoint, 6]
    QPband = np.append(QPband, newcol.reshape(numPoint, 1), 1)
# insert the band values, this is the MF band
for i in range(int(len(banddata)/numPoint)):
    newcol = banddata[i*numPoint:(i+1)*numPoint, 5]
    MFband = np.append(MFband, newcol.reshape(numPoint, 1), 1)
print(QPband.shape)

# the plot should be shift down shiftVal together
row, col = QPband.shape
shiftVal = max(QPband[:, int((col-1)/2)])

# mark the band gap, indicate the max/min for homo/lumo
lowGapIndex = np.argmax(QPband[:, int((col-1)/2)])
highGapIndex = np.argmin(QPband[:, int((col-1)/2)+1])
bandgapVal = max(QPband[:, int((col-1)/2)]) - min(QPband[:, int((col-1)/2)+1])

upstripMax = max(QPband[:, int((col-1)/2+2)])
upstripMin = min(QPband[:, int((col-1)/2+1)])
lowstripMax = max(QPband[:, int((col-1)/2)])
lowstripMin = min(min(QPband[:, int((col-1)/2-1)]), min(QPband[:, int((col-1)/2)]))
print('bandgap is:', abs(bandgapVal), 'eV')
# start the plot here
fig = plt.figure(num=None, figsize=(9, 7), dpi=80, facecolor='w', 
                 edgecolor='k', frameon=True)
ax = fig.add_subplot(111)
for i in range(len(QPband[0])-1):
    plt.plot(QPband[:,0], QPband[:,i+1]-shiftVal, 'r', lineWidth=1.5)
#    plt.plot(QPband[:,0], QPband[:,i+1]-shiftVal, '.r')
    plt.scatter(QPband[:,0], QPband[:,i+1]-shiftVal, s=6, marker='o', c='red')

# add the band gap plot
plt.plot([QPband[lowGapIndex][0], QPband[highGapIndex][0]], \
         [QPband[lowGapIndex][int((col-1)/2)]-shiftVal, \
          QPband[highGapIndex][int((col-1)/2)+1]-shiftVal], '--b', linewidth=2)

# add the band gap value
plt.text(0.5*(QPband[lowGapIndex][0]+QPband[highGapIndex][0])-0.175, \
    0.5*(QPband[lowGapIndex][int((col-1)/2)]+QPband[highGapIndex][int((col-1)/2)+1])- 
    shiftVal-1, str(abs(bandgapVal))[:4]+' eV', weight='normal', 
    size='xx-large', color='blue')
# add the high symmtry point
plt.axis([0.0, QPband[numPoint-1][0], -3, 5])

# manipulate the kpoint into $*$ format
for i, name in enumerate(kpointName):
    kpointName[i] = "$" + name + "$"
## add high symmetry points
for i in kpointIndex:
    plt.plot([QPband[i][0], QPband[i][0]], [-100, 100], 'K', linewidth=2)
## add the fermi energy
plt.plot([0.0, QPband[numPoint-1][0]], [0.0, 0.0], 'k--', linewidth=1.0)
#
## add x y label
plt.ylabel('$E-E_{F}$ (eV)', fontname="Arial", fontsize=20)
nameVal = []
for i in kpointIndex:
    nameVal += [QPband[i][0]]
    
nameVal.sort()
name = ['$\Gamma$', '$XY$', '$\Gamma$', '$ZR_2$', '$\Gamma$', '$T_2U_2$', '$\Gamma$', '$V_2$']

# x ticks
plt.tick_params(
    axis='x',            # changes apply to the x-axis
    which='both',        # both major and minor ticks are affected
    bottom=False,        # ticks along the bottom edge are off
    top=False,           # ticks along the top edge are off
    labelbottom=True)   # labels along the bottom edge are off
plt.xticks(nameVal, name, fontname="Arial", fontsize=15)
# y ticks
plt.tick_params(
    axis='y',            # changes apply to the x-axis
    which='both',        # both major and minor ticks are affected
    bottom=False,        # ticks along the bottom edge are off
    top=False,           # ticks along the top edge are off
    labelbottom=True)   # labels along the bottom edge are off
plt.yticks(fontname="Helvatica", fontsize=18)
plt.title(titlename, fontname='Helvatica', fontsize=22)
plt.show()

fig.savefig(titlename+'.png', dpi=300, bbox_inches='tight')