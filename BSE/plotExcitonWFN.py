import numpy as np
import matplotlib.pyplot as plt
import os
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
    # reverse according to z axis
    tmpindex = np.arange(data.shape[0])
    for i in range(data.shape[0]):
        if i%finez == 0 and (i//finez)%2 == 1:
            tmpindex[i:i+finez] = tmpindex[i:i+finez][::-1]
    # reverse according to y axis            
    for i in range(data.shape[0]):
        if i%(finey*finez) == 0 and (i//(finey*finez))%2 == 1:
            tmpindex[i:i+(finey*finez)] = tmpindex[i:i+(finey*finez)][::-1]
    data = data[tmpindex]

    outdata = np.zeros((data.shape[0], 2))
    outdata[:, 1] = data[:, -1]
    divideindex = []
    for i in range(1, len(data)):
        dist = np.linalg.norm(data[i][:3] - data[i-1][:3], 2)
#        outdata[i][0] = dist + outdata[i-1][0]
        if dist > 100:
            outdata[i][0] = outdata[i-1][0]
            divideindex.append(i)
        else:
            outdata[i][0] = dist + outdata[i-1][0]
            
    return (outdata, divideindex)


finex = 4
finey = 4
finez = 16

plotdata = dict()
for name in datalist:
    plotdata[name] = extractdata(os.path.join(path, name), finez=2, finey=2)

fig = plt.figure(num=None, figsize=(10, 4), dpi=100, \
                 facecolor='w', edgecolor='k', frameon=True)
colorlist = itertools.cycle(['b', 'r', 'k', 'g', 'y', 'c', 'm'])
plotlist = list()
namelist = list()

for key, val in plotdata.items():
    if key !="exciton_01":
        continue
    namelist.append(key)
    plotlist.append(plt.plot(val[0][:, 0], val[0][:, 1], \
                             linestyle='-', color = next(colorlist), linewidth=1.5)[0])
#    for index in val[1]:
#        plt.vlines(val[0][index], 0, 1, colors='k', linestyles='solid')
plt.legend((plotlist), (namelist))
#plt.axis([-1, val[0][-1][0], 0.0-0.2*max(val[0][:, 1]), 1.2*max(val[0][:, 1])])
plt.xlabel("$K$ Path")
plt.ylabel('$\sum |A(k)|^2$')
plt.title('Fine K grid = $%d x %d x %d$' %(finex, finey, finez))
#fig.savefig(str(finex)+str(finey)+str(finez)+'.png', bbox_inches='tight', dpi=300)