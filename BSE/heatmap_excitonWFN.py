import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import itertools

path = "plot_exciton_wfn_data/KECLAH/846test"
path = "plot_exciton_wfn_data/TBZHCE/1622"
#path = "plot_exciton_wfn_data/TBZHCE/2022"
#path = "plot_exciton_wfn_data/TBZHCE/2444"

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
    return data

fig, ax = plt.subplots(figsize=(4, 5))
data = extractdata(os.path.join(path, "exciton_01"))
finex = 16
finey = 2
allval = np.array([]).reshape(finex, 0)
for k in range(2):
    index = np.where(data[:, 2] == data[k][2])[0]
    val = data[index]
    val = val[val[:, 0].argsort()]
    heatval = np.zeros((finex, finey))
    for i in range(heatval.shape[0]):
        for j in range(heatval.shape[1]):
            heatval[i][j] = val[i*finey + j][3]
    allval = np.concatenate((allval, heatval), axis=1)
allval = allval / np.max(allval)

print(allval[:, int(allval.shape[1]/2-1):int(allval.shape[1]/2+1)])
tmpplot = allval[:, int(allval.shape[1]/2-1):int(allval.shape[1]/2+1)].copy()
tmpplot = np.mean(tmpplot, 1).reshape(-1, 1)
print(tmpplot.shape)
fig.set_size_inches(3, 5)
sns.heatmap(ax=ax, data=tmpplot, linewidth=0.0, cmap="hot", \
            xticklabels=False, yticklabels=False,\
            cbar_kws={'label': '$\sum |A(k)|^2$'})  #square=True
sns.set(font_scale=1.2)
plt.xlabel("Exciton 01", fontsize=14)
plt.show()
#fig.savefig("Exciton_04_16x2x2.png", dpi=100, bbox_inches='tight')