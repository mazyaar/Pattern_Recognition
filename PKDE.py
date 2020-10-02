import numpy as np
import xlrd
import matplotlib.pyplot as plt
import time
from matplotlib import cm

# var
x = []
y = []
x_temp = []
y_temp = []
x_new = []
p_x = []
y_new = []

# main
workbook = xlrd.open_workbook('data.xlsx')
sheet = workbook.sheet_by_index(0)
row = sheet.nrows

for i in range(1, row):
    x.append(float(sheet.cell_value(i, 0)))
    y.append(float(sheet.cell_value(i, 1)))

x_min = np.min(x)
x_max = np.max(x)
y_min = np.min(y)
y_max = np.max(y)
print(f'x-> min : {x_min} / max : {x_max}')
print(f'y-> min : {y_min} / max : {y_max}')

# draw x/y
plt.figure('X/Y')
plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')

# parzen window and draw
baze = [float(input('Start > ')), float(input('End > '))]
h = np.max(baze) - np.min(baze)
D = 2
for i in x:
    if np.min(baze) < i < np.max(baze):
        x_temp.append(i)
        y_temp.append(y[x.index(i)])

for i in y_temp:
    if np.min(baze) < i < np.max(baze):
        y_new.append(i)
        x_new.append(x[y_temp.index(i)])

del x_temp
del y_temp


def fi(i, j, h):
    a = (np.abs(i - j)) / h
    if np.abs(a) < 1 / 2:
        return 1
    else:
        return 0


def k(x0, x_baz, h):
    a = 0
    for i in x_baz:
        a += fi(x0, i, h) * ((np.abs(x0 - i)) / h)
    return a


def parzen_window(x0, x_baz, h, D):
    a = (len(x_baz)) * (h ** D)
    b = 0
    for i in x_baz:
        b += k(x0, x_baz, h) * ((np.abs(x0 - i)) / h)
    return b / a


start = time.time()
for i in x_new:
    p_w = parzen_window(i, x_new, h, D)
    p_x.append(p_w)
    print(f'{i} : {p_w}')

end = time.time()
print(f'time : {end - start}')

print(len(p_x), len(x_new), len(y_new))

fig = plt.figure('3D Parzen')
ax = plt.axes(projection="3d")
ax.plot_trisurf(x_new, y_new, np.array(p_x), cmap=cm.jet)

plt.show()
