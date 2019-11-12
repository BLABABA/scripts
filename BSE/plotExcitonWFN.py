import numpy as np
import matplotlib.pyplot as plt
import os
import itertools

path = "plot_exciton_wfn_data/846"

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
    for i, ival in enumerate(data):
        for j, jval in enumerate(data[:3]):
            if data[i][j] < 0:
                data[i][j] += 1
    outdata = np.zeros((data.shape[0], 2))
    outdata[:, 1] = data[:, -1]
    divideindex = []
    for i in range(1, len(data)):
        dist = np.linalg.norm(data[i][:3] - data[i-1][:3], 2)
        if dist > 0.5:
            outdata[i][0] = outdata[i-1][0]
            divideindex.append(i)
        else:
            outdata[i][0] = dist + outdata[i-1][0]
    print(divideindex)
    return (outdata, divideindex)

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
    plotlist.append(plt.plot(val[0][:, 0], val[0][:, 1], linestyle=':', color = next(colorlist), linewidth=1.5)[0])
#    for index in val[1]:
#        plt.vlines(val[0][index], 0, 1, colors='k', linestyles='solid')
plt.legend((plotlist), (namelist))
#plt.axis([-1, 27, 0.0, 0.02])
plt.xlabel("$K$ Path")
plt.ylabel('$\sum |A(k)|^2$')
plt.title('Fine K grid = $8 x 4 x 6$')
fig.savefig('846.png', bbox_inches='tight', dpi=300)