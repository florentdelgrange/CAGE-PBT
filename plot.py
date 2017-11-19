import numpy as np
import matplotlib.pyplot as plt
import sys
import numpy as np
import matplotlib.ticker as ticker
from options import *
from clicker import clicker_class

_files = sys.argv[1:]

fig = plt.figure()
for j, _file in enumerate(_files):
    x = []
    y = []
    with open(_file, 'r') as f:
        for line in f:
            x += [float(line.split('\t')[0])]
            y += [float(line.split('\t')[1][:-1])]

    x = np.array(x)
    if Y_SHIFT and j > 0:
        y = list(map(lambda x: x + Y_SHIFT, y))
    y = np.array(y)

    plt.plot(x, y, linewidth=0.8, label=_file.split("/")[-1].split(".")[0])

fig.suptitle(TITLE)
plt.xlabel(X_AXIS)
if X_INVERT:
    plt.gca().invert_xaxis()
if not Y_AXIS:
    frame = plt.gca()
    frame.axes.get_yaxis().set_visible(False)
else:
    plt.ylabel(Y_AXIS)
if GRID:
    plt.grid()
if len(_files) > 1:
    plt.legend()

ax = plt.gca()
stepx = x.max() - x.min()
stepy = y.max() - y.min()
plt.cc = clicker_class(ax, stepx/200, stepy/20)
plt.show()
