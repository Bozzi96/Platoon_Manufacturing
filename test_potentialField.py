# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:57:34 2023

###TODO: Fix starting points, NOT WORKING ?!

@author: bozzi
"""

import numpy as np

import matplotlib.pyplot as plt
import potentialField as pf


x0 =[0,0] #initial position
xg = [20,15] #goal position
x = [x0]
xn = [[10, 10], [6,6]] #obstacle
r = 0.1 #goal size
s = 4 # "attraction" size


X, Y = np.meshgrid(np.arange(-0,100,1),np.arange(-0,100,1))
delx, dely = pf.add_goal(X, Y, r, s, xg)
for i in range(len(xn)):
	delx, dely, loc = pf.add_obstacle(X, Y, delx, dely, r, s, xg, xn[i])

fig, ax = plt.subplots(figsize = (10,10))
for _ in range(1):
	delx, dely = pf.add_goal(X, Y,r, s , xg)
    
	pf.plot_graph(X, Y, delx, dely , 'Goal',fig, ax, xg, 1,0, 'b')

	for j in range(len(xn)):
		delx, dely, loc = pf.add_obstacle(X,Y, delx,dely,r,s,xg, xn[j])
		pf.plot_graph(X, Y, delx, dely , 'Obstacle',fig, ax, loc, r , j+1,'m',)
		ax.add_patch(plt.Circle(loc, 1, color='m'))
stream = ax.streamplot(X,Y,delx,dely, start_points=[x0],linewidth=4)
		
trajectory= stream.lines.get_segments() # Get a 2x2 for each point --> Why???
trajectory = np.delete(trajectory, 0,axis=1)#Remove the second row (useless)
trajectory = np.resize(trajectory, [len(trajectory), 2])
plt.show()