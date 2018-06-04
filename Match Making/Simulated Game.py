''' 
Title Simulated Game
Creator Sean Duncan
Date 5/26/18

Purpose This is an animated + simulated game of dots that fight eachother 6v6 in square. 
The dots are 'skilled' and have MMR that influences their chances of winning the game.
The dots will use lasers to eliminate eachother, the team with the last dot/s standing wins.

'''

#Import libraries 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import matplotlib.patches as patches
from datetime import datetime
import time

#Number of players
N = 12
pause = False

#Lets the pause mechanic work
def onClick(event):
    global pause
    pause ^= True

#Create the lazers
class laser(object):
  _globVar1 = None
  def __init__(self, side, x, y):

    #initial position
    self.side = side
    self.x = x
    self.y = y

    #blue shoots down, red shoots up
    if self.side == 0:
      self.vely = -0.15
    else:
      self.vely = 0.15

    self.velx = 0

  def shoot(self):
    #straight line
    self.y = self.y + self.vely

  #def __del__(self):
    #print("Laser at (" + str(self.x) + "," + str(self.y) + ") was removed")

#Create a player / dot
class player(object):
  def __init__(self, side, slot):
    #assign passed parameters to object
    self.side = side
    self.slot = slot

    #blue starts up top, red below
    if self.side == 0:
      self.y = 10 - (2 * np.random.random_sample())
    else: 
      self.y = (2 * np.random.random_sample())
    self.x = 10 * np.random.random_sample()
    #self.x = 3
    #give them a velocity
    self.velx = self.generate_new_vel()
    self.vely = self.generate_new_vel()

  def generate_new_vel(self):
    return (np.random.random_sample() - 0.5) / 5

  #def __del__(self):
    #print("Player, team " + str(self.side) + ",  at (" + str(self.x) + "," + str(self.y) + ") was removed")

  def move(self):
    #move randomly
    if self.side == 0:
      if np.random.random_sample() < 0.95:
        self.x = self.x + self.velx
        self.y = self.y + self.vely
      else:

        #if change x direction, shoot laser
        temp = self.generate_new_vel()
        if ((self.x <= 0 <= temp) or (self.x >= 0 >= temp)):
          print("Player shot")

        self.velx = temp
        self.vely = self.generate_new_vel()
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

    else:
      self.velx = 0
      self.vely = 0

def examineDamage(characters, weapons, kills):

  #check for collisions loop through lasers then players
  for i, player in enumerate(characters):

    for j, laser in enumerate(weapons):
      if math.sqrt( (characters[i].x - weapons[j].x) ** 2 + (characters[i].y - weapons[j].y) ** 2) < 0.25 and characters[i].side != weapons[j].side:
        print("Player, team " + str(characters[i].side) + ",  at (" + str(characters[i].x) + "," + str(characters[i].y) + ") was hit and removed")
        del characters[i]
        del weapons[j]
        kills = kills + 1
        break

  return (kills)

###Start the simulation

#Initialize players
playersT1 = [player(0, i) for i in xrange(N/2)]
playersT2 = [player(1, i) for i in xrange(N/2)]
players = np.concatenate((playersT1,playersT2))
lasers = [laser(players[i].side, players[i].x, players[i].y) for i in xrange(N)]

#Animation plot parameters
figure = plt.figure()
axes = plt.axes(xlim = (-2,12), ylim = (-2,12))

p1, = axes.plot([player.x for player in playersT1],
              [player.y for player in playersT1], 
              'bo', 
              markersize = 10)

p2, = axes.plot([player.x for player in playersT2],
              [player.y for player in playersT2], 
              'ro', 
              markersize = 10)

b, = axes.plot([laser.x for laser in lasers],
               [laser.y for laser in lasers], 'g*', markersize = 5)

#UI Improvements
#playing map
axes.add_patch(patches.Rectangle((0, 0), 10, 10, color = '#940dba'))
axes.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 9.6, color = '#ffffff'))

#time stamp
time_template = 'Time = %.1f s'
time_text = axes.text(.43, 0.92, '', transform=axes.transAxes)
win_text = axes.text(.42,.5, '', transform = axes.transAxes)

#track deaths
k1 = 0
k2 = 0

#Animation function, called sequentially 
def animate(i):
  #Create the lazers
  class laser2(object):
    _globVar1 = None
    def __init__(self, side, x, y):

      #initial position
      self.side = side
      self.x = x
      self.y = y

      #blue shoots down, red shoots up
      if self.side == 0:
        self.vely = -0.15
      else:
        self.vely = 0.15

      self.velx = 0

    def shoot(self):
      #straight line
      self.y = self.y + self.vely

    #def __del__(self):
      #print("Laser at (" + str(self.x) + "," + str(self.y) + ") was removed")

  if not pause:
    #Pass kill counts through so indexing doesnt reset or itll throw enumerators off
    global k1
    global k2
    global lasers
    global laser 
    global run_start
    global pause

    #Set time
    t = time.time() - run_start
    time_text.set_text(time_template%(t))

    #Check to see if players took damage
    k1 = examineDamage(playersT1, lasers, k1)
    k2 = examineDamage(playersT2, lasers, k2)

    #move lasers that didn't hit a player one time
    for i, laser in enumerate(lasers):
      #print("Laser at (" + str(lasers[i].x) + "," + str(lasers[i].y) + ") is being tracked")
      lasers[i].shoot()
      if (lasers[i].x > 10 or lasers[i].x < 0 or lasers[i].y > 10 or lasers[i].y < 0):
        print("deleting laser (" + str(lasers[i].x) + "," + str(lasers[i].y) + ")")
        del lasers[i]

    #Move players that were not hit
    for i, player in enumerate(players):
      temp = players[i].velx
      players[i].move()
      
      if (temp > 0 and players[i].velx < 0) or (temp < 0 and players[i].velx > 0):
        print ("Making laser " + str(players[i].side) + " " + str(players[i].x) +  " " + str(players[i].y) )
        #lasers = np.concatenate((lasers, [laser2(players[i].side, players[i].x, players[i].y)]))
    #display lasers
    b.set_data([laser.x for laser in lasers],
               [laser.y for laser in lasers])

    #dispay team 1 blue
    p1.set_data([player.x for player in playersT1],
                [player.y for player in playersT1])
    #display team 2 red
    p2.set_data([player.x for player in playersT2],
                [player.y for player in playersT2])
    #Check if the game is over
    if not playersT1: 
      win_text.set_text("Red Team Wins")
    if not playersT2:
      win_text.set_text("Blue Team Wins!")

    return (p1, p2, b,)

#Call the animator, 
run_start = time.time()
figure.canvas.mpl_connect('button_press_event', onClick)
animator = animation.FuncAnimation(figure, animate, blit=False, repeat = True, frames = 100, interval = 10)

#animator.save('basic_animation.gif', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()













