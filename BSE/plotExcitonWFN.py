import numpy as np
import matplotlib.pyplot as plt
import os
import itertools

path = "plot_exciton_wfn_data/1068"

datalist = os.listdir(path)
for val in datalist[:]:
    if not val.startswith("exciton_"):
        datalist.remove(val)

def extractdata(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    data = data[1:]
    for i, val in enumerate(data):
        data[i] = val[:-2].split()
    data = np.array(data).astype(float)
    outdata = np.zeros((data.shape[0], 2))
    outdata[:, 1] = data[:, -1]
    for i in range(1, len(data)):
        distvec = data[i][:3] - data[i-1][:3]
        outdata[i][0] = np.linalg.norm(distvec, 2) + outdata[i-1][0]
    return outdata

plotdata = dict()
for name in datalist:
    plotdata[name] = extractdata(os.path.join(path, name))

fig = plt.figure(num=None, figsize=(6, 4), dpi=100, \
                 facecolor='w', edgecolor='k', frameon=True)
colorlist = itertools.cycle(['b', 'r', 'k', 'g', 'y', 'c', 'm'])
plotlist = list()
namelist = list()

for key, val in plotdata.items():
    namelist.append(key)
    plotlist.append(plt.plot(val[:, 0], val[:, 1], color = next(colorlist))[0])
plt.legend((plotlist), (namelist))
plt.xlabel("$K$ Path")
plt.ylabel('$\sum |A(k)|^2$')
plt.title('Find K grid = $10 x 6 x 8$')
fig.savefig('1068.png', bbox_inches='tight', dpi=300)