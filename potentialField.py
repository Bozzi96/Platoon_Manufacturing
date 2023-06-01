import random
import numpy as np
import matplotlib.pyplot as plt

"""
  Args:
    X =  2D array of the Points on X-axis
    Y =  2D array of the Points on Y-axis 
    r = goal size
    loc = goal location
  Return :
    delx and dely
  
  This function is to add the goal and its potential field on the graph.
  α = 50
"""
a = 50 #alpha

def add_goal (X, Y,s, r, loc):

  delx = np.zeros_like(X)
  dely = np.zeros_like(Y)
  for i in range(len(X)):
    for j in range(len(Y)):
      
      d= np.sqrt((loc[0]-X[i][j])**2 + (loc[1]-Y[i][j])**2)
      theta = np.arctan2(loc[1]-Y[i][j], loc[0] - X[i][j])
      if d< r:
        delx[i][j] = 0
        dely[i][j] =0
      elif d>r+s:
        delx[i][j] = a* s *np.cos(theta)
        dely[i][j] = a * s *np.sin(theta)
      else:
        delx[i][j] = a * (d-r) *np.cos(theta)
        dely[i][j] = a * (d-r) *np.sin(theta)
  return delx, dely


"""
  Args:
    X =  2D array of the Points on X-axis
    Y =  2D array of the Points on Y-axis 
    delx = Usual meaning
    dely = Usual Meaninig
    obj = String to tell is the object on the map is Goal or the Obstacle
    fig = Matplotlib figure
    ax = Axis of the figure
    loc = Location of the object
    r = Size of the object
    i = Number of the Object
    color = coloer of the object
    start_goal = starting point of the robot, default = (0,0)
  Returns:
    ax = axis of the figure
  This function plot the quiver plot, draw the goal/ obstacle at the given location
  whith given color and text.  
"""
def plot_graph(X, Y, delx, dely,obj, fig, ax, loc,r,i, color):
  
  #ax.quiver(X, Y, delx, dely)
  ax.add_patch(plt.Circle(loc, r, color=color))
  ax.annotate(obj, xy=loc, fontsize=10, ha="center")
  return ax


"""
  Args:
    X =  2D array of the Points on X-axis
    Y =  2D array of the Points on Y-axis 
    delx = Usual meaning
    dely = Usual Meaninig
    goal = location of the goal 
  Return:
    delx = Usual meaning
    dely = Usual Meaninig
    obstacle = location of the obstacle 
    r = size of the obstacle 
  This function first generate the obstacle with diameter ranging from 1 to 5 i.e. radius 
  ranging from 0.5 to 2.5 randomly. Then it generate location of the obstacle randomly.
  Then inside the nested loop, distance from each point to the goal and ostacle is 
  calculated, Similarly angles are calculated. Then I simply used the formula give and 
  superimposed it to the Goals potential field.Also
  α = 50
  β = 120
  s = 7
  
"""
alpha = 30
beta = 100
def add_obstacle(X, Y , delx, dely, r, s, goal, obstacle):
  for i in range(len(X)):
    for j in range(len(Y)):
      
      d_goal = np.sqrt((goal[0]-X[i][j])**2 + ((goal[1]-Y[i][j]))**2)
      d_obstacle = np.sqrt((obstacle[0]-X[i][j])**2 + (obstacle[1]-Y[i][j])**2)
      theta_goal= np.arctan2(goal[1] - Y[i][j], goal[0]  - X[i][j])
      theta_obstacle = np.arctan2(obstacle[1] - Y[i][j], obstacle[0]  - X[i][j])
      if d_obstacle < r:
        delx[i][j] = -1*np.sign(np.cos(theta_obstacle))*5 +0
        dely[i][j] = -1*np.sign(np.cos(theta_obstacle))*5  +0
      elif d_obstacle>r+s:
        delx[i][j] += 0 
        dely[i][j] += 0
      elif d_obstacle<r+s :
        delx[i][j] += -beta *(s + r - d_obstacle)* np.cos(theta_obstacle)
        dely[i][j] += -beta * (s + r - d_obstacle)*  np.sin(theta_obstacle) 
      if d_goal <r+s:
        if delx[i][j] != 0:
          delx[i][j]  += (alpha * ( d_goal -r) *np.cos(theta_goal))
          dely[i][j]  += (alpha * (d_goal-r) *np.sin(theta_goal))
        else:
          
          delx[i][j]  = (alpha * (d_goal-r) *np.cos(theta_goal))
          dely[i][j]  = (alpha * (d_goal-r) *np.sin(theta_goal))
          
      if d_goal>r+s:
        if delx[i][j] != 0:
          delx[i][j] += alpha* s *np.cos(theta_goal)
          dely[i][j] += alpha* s *np.sin(theta_goal)
        else:
          
          delx[i][j] = alpha* s *np.cos(theta_goal)
          dely[i][j] = alpha* s *np.sin(theta_goal)

   
  return delx, dely, obstacle, r