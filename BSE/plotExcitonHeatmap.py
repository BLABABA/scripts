import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import itertools

path = "plot_exciton_wfn_data/KECLAH/846test"
path = "plot_exciton_wfn_data/TBZHCE/1622"
path = "plot_exciton_wfn_data/TBZHCE/2022"
path = "plot_exciton_wfn_data/TBZHCE/2444"

datalist = os.listdir(path)

for val in datalist[:]:
    if not val.startswith("exciton_"):
        datalist.remove(val)

def extractdata(filename, finez=4, finey=4):
    with open(filename, 'r') as f:
        data = f.readlines()
    data = data[1:]
    for i, val in enumerate(data):
        data[i] = val[:-2].split()
    data = np.array(data).astype(float)
    for i, ival in enumerate(data):
        for j, jval in enumerate(data[:3]):
            if data[i][j] < 0:
                data[i][j] += 1
    return data

fig = plt.figure(num=None,figsize=(7, 5), dpi=80,facecolor='w', edgecolor='k', frameon=True)
data = extractdata(os.path.join(path, "exciton_01"))
index = np.where(data[:, 2] == data[0][2])[0]
val = data[index]
val = val[val[:, 0].argsort()]
print(val)
heatval = np.zeros((24, 4))
for i in range(heatval.shape[0]):
    for j in range(heatval.shape[1]):
        heatval[i][j] = val[i*4 + j][3]
#plt.imshow(heatval, cmap='hot', interpolation='nearest')
ax = sns.heatmap(heatval, linewidth=0.0, square=True, cmap="hot")
plt.show()

## scattering map ###
plt.scatter(data[index][:, 0], data[index][:, 1], c=data[index][:, 3], cmap='jet')
plt.colorbar()
plt.show()

colorlist = itertools.cycle(['b', 'r', 'k', 'g', 'y', 'c', 'm'])

def plotOnecut(data, shiftlen, finey=4, finez=4, plotVerticle=False):
    partlist = []
    for i in range(shiftlen):
        index = np.where(data[:, 2] == data[i][2])[0]
        val = data[index]
#        val = np.sort(data[index], axis=0)
        # reverse according to y axis
#        tmpindex = np.arange(val.shape[0])
#        for i in range(val.shape[0]):
#            if i%(finey) == 0 and (i//(finey))%2 == 1:
#                tmpindex[i:i+(finey)] = tmpindex[i:i+(finey)][::-1]
#        print(tmpindex)
#        val = val[tmpindex]
        partlist.append(val)
#    print(partlist)
    lastdist = 0
    vlist = []
    color = next(colorlist)
    for i, val in enumerate(partlist):
#        if i != 0:
#            continue
        tmpdata = np.zeros((len(val), 2))
        tmpdata[:, 1] += val[:, 3]
        for i, coord in enumerate(val):
            if i == 0:
                tmpdata[i][0] = lastdist
                vlist.append(lastdist)
                continue
            tmpdata[i][0] = lastdist + np.linalg.norm(val[i][:3]-val[i-1][:3], 2)
            lastdist = tmpdata[i][0]
        excitonplot = plt.plot(tmpdata[:, 0], tmpdata[:, 1], color=color)
    if plotVerticle:
        for val in vlist[1:]:
            plt.vlines(val, min(data[:, 3]), max(data[:, 3])*1.2, colors='k', \
                       linestyles='dashed')
    return tmpdata[i][0], max(data[:, 3]), excitonplot

fig = plt.figure(num=None,figsize=(7, 5), dpi=80,facecolor='w', edgecolor='k', frameon=True)
excitonplotlist = []
for i in range(4):
    data = extractdata(os.path.join(path, "exciton_0"+str(i+1)))
    xmax, ymax, excitonplot = plotOnecut(data, shiftlen = 4, plotVerticle=True)
    excitonplotlist.append(excitonplot)
#    plt.axis([0, xmax, 0, ymax*1.8])
plt.xlabel("K Path", fontname='Helvatica', fontsize=16)
# x ticks
plt.tick_params(
    axis='x',            # changes apply to the x-axis
    which='both',        # both major and minor ticks are affected
    bottom=False,        # ticks along the bottom edge are off
    top=False,           # ticks along the top edge are off
    labelbottom=False)   # labels along the bottom edge are off
#plt.xticks(nameVal, name, fontname="Arial", fontsize=16)
plt.ylabel("$\sum |A(k)|^2$ (eV)",fontname='Helvatica', fontsize=16)
# y ticks
plt.tick_params(
    axis='y',            # changes apply to the y-axis
    which='both',        # both major and minor ticks are affected
    left=False,        # ticks along the bottom edge are off
    right=False,           # ticks along the top edge are off
    labelbottom=False)   # labels along the bottom edge are off
plt.yticks([])
plt.yticks(fontname="Helvatica", fontsize=20)
#plt.legend(("Exciton 01", "Exciton 02", "Exciton 03", "Exciton 04"), \
#(excitonplotlist[0][0],excitonplotlist[1][0],excitonplotlist[2][0],excitonplotlist[3][0]))

plt.show()
#fig.savefig('TBZHCE_2444_tmp', dpi=100, bbox_inches='tight')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
