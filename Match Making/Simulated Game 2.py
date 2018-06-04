#Import libraries 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import matplotlib.patches as patches
from datetime import datetime
import time

N=1

players = []
axes = plt.axes(xlim = (-2,12), ylim = (-2,12))

#Animation plot parameters
figure = plt.figure()

def animate(i):
  #Create a player / dot
  class player(object):
    def __init__(self, side, slot):
      #assign passed parameters to object
      self.side = side
      self.slot = slot
      self.y = 10 * np.random.random_sample()
      self.x = 10 * np.random.random_sample()

      #give them a velocity
      self.velx = self.generate_new_vel()
      self.vely = self.generate_new_vel()

    def generate_new_vel(self):
      return (np.random.random_sample() - 0.5) / 5

    def move(self):
      #move randomly
      if np.random.random_sample() < 0.95:
        self.x = self.x + self.velx
        self.y = self.y + self.vely

      #Don't go outside the boundaries
      if self.x >= 10:
        self.x = 10
        self.velx = -1 * self.velx
      if self.x <= 0:
        self.x = 0
        self.velx = -1 * self.velx
      if self.y >= 10:
        self.y = 10
        self.vely = -1 * self.vely
      if self.y <= 0:
        self.y = 0
        self.velx = -1 * self.vely

  print("i is " + str(i))
  
  global players
#  global p1
  global axes

  if i == 0:
    ###Start the simulation

    #Initialize players
    players = [player(0, i) for i in xrange(N)]

  elif (i<=0):
    print("there are " + str(len(players)) + " players")
    #dispay team 1 blue
    for j, player in enumerate(players):
      players[j].move()

  #p1, = axes.plot([player.x for player in players],
   #       [player.y for player in players], 
    #      'bo', 
     #     markersize = 10)
    
  #p1.set_data([player.x for player in players],
              #[player.y for player in players])

  return ( ) #p2, b,)

#Call the animator, 
print("Here")
run_start = time.time()
#figure.canvas.mpl_connect('button_press_event', onClick)
animator = animation.FuncAnimation(figure, animate, blit=False, repeat = True, frames = 200, interval = 20)

#animator.save('basic_animation.gif', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()


























