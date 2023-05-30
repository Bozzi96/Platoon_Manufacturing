# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:57:34 2023

@author: bozzi
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import potentialField as pf


x0 =[0,0]
xg = [20,20]
x = [x0]
v = [[0, 0]]
xn = [[6,6]]
r = 1 #goal size
s = 5 # safety size
# dt = 1
# m = 1
# i = 0

# Animated plot
# create empty lists for the x and y data
# xp = []
# yp = []

# # create the figure and axes objects
# fig, ax = plt.subplots()
# def animate(i):
#     xp.append(x[i][0])
#     yp.append(x[i][1])

#     ax.clear()
#     ax.plot(xp, yp)
#     ax.set_xlim([0,20])
#     ax.set_ylim([0,10])



# while math.dist(x[-1], xg) > 1 and i<1000:
# 	F,ang = pfc.potentialFieldController(x[i] , xn, xg)
# 	acc = [float(F[0])/m, float(F[1])/m]
# 	i = i+1
# 	v.append([v[i-1][0] + acc[0]*dt, v[i-1][1] + acc[1]*dt])
# 	x.append([x[i-1][0] + v[i][0]*dt + acc[0]*0.5*dt*dt, x[i-1][1] + v[i][1]*dt + acc[1]*0.5*dt*dt, ang])
# # 	ani = FuncAnimation(fig, animate(i), frames=20, interval=500, repeat=False)
# # 	plt.show()

# plt.plot([row[0] for row in x],[row[1] for row in x])

X, Y = np.meshgrid(np.arange(-0,50,1),np.arange(-0,50,1))
delx, dely = pf.add_goal(X, Y, r, s, xg)
for i in range(len(xn)):
	pf.add_obstacle(X, Y, delx, dely, xg, xn[i])

fig, ax = plt.subplots(figsize = (10,10))
for _ in range(1):
	delx, dely = pf.add_goal(X, Y,1, 1 , xg)
    
	pf.plot_graph(X, Y, delx, dely , 'Goal',fig, ax, xg, 1,0, 'b' )

	for j in range(len(xn)):
		delx, dely, loc, r = pf.add_obstacle(X,Y, delx,dely,xg, xn[j])
		pf.plot_graph(X, Y, delx, dely , 'Obstacle',fig, ax, loc, r , j+1,'m')
		ax.add_patch(plt.Circle(loc, 1, color='m'))
		stream = ax.streamplot(X,Y,delx,dely, start_points=pf.seek_points,linewidth=4, cmap='autu')
		
trajectory= stream.lines.get_segments()
plt.show()