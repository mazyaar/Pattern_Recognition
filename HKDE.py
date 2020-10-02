import numpy as np
import xlrd
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import stats

# var
x = []
y = []

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

start = [[float(input('start x > '))
             , float(input('end x > '))]
    , [float(input('start y > '))
             , float(input('end y > '))]]
bin_w = int(input('bin_w > '))

# draw x/y
plt.figure('X/Y')
plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')

# draw 2d histogram
plt.figure('Histogram')
plt.hist2d(x, y, bins=bin_w, range=start)

# make 3D histogram and draw
H, Xe, Ye = np.histogram2d(x, y, bins=bin_w, range=start)
H = H.T

fig = plt.figure('3D Histogram')
ax = fig.add_subplot(111, projection='3d')
xpos, ypos = np.meshgrid(Xe[:-1] + Xe[1:], Ye[:-1] + Ye[1:])

xpos = xpos.flatten() / 2.
ypos = ypos.flatten() / 2.
zpos = np.zeros_like(xpos)

dx = Xe[1] - Xe[0]
dy = Ye[1] - Ye[0]
dz = H.flatten()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

# make KDE and draw KDE
xx, yy = np.mgrid[np.min(Xe):np.max(Xe), np.min(Ye):np.max(Ye)]
pos = np.vstack([xx.ravel(), yy.ravel()])
val = np.vstack([x, y])
kernel = stats.gaussian_kde(val)
f = np.reshape(kernel(pos).T, xx.shape)

fig = plt.figure('KDE')
ax = fig.gca()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
cfset = ax.contourf(xx, yy, f, cmap='Reds')
cset = ax.contour(xx, yy, f, colors='k')
ax.clabel(cset, inline=1, fontsize=10)
ax.set_xlabel('X')
ax.set_ylabel('Y')

# 3D KDE
fig = plt.figure('3D KDE')
ax = plt.axes(projection="3d")

ax.plot_surface(xx, yy, f, cmap=cm.jet)
plt.show()

