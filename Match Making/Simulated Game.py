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
import sys
import random

#Number of players
N = 2
pause = False

#For debugging, select what you want printed then print
def verbose(loudOption,printMe):
    if loudOption:
        print(printMe)

#Used for aiming 
def calcAngle(xPart, yPart):
  a = round(math.degrees(math.atan(yPart/xPart)),0)
  if xPart >= 0:
    if yPart >= 0:
      a = a
    else:
      a = a + 360
  else:
    if yPart >= 0:
      a = a + 180
    else:
      a = a + 180

  return a 

#Shot angle calculator
def calcShot(desired, adjustment):
  newAngle = round(desired,0) + round(adjustment,0)
  verbose(False, "Desired Angle = " + str(desired) + " off by = " + str(adjustment) + " new angle = " + str(newAngle))  
  verbose(False, "X portion = " + str(round(np.cos(np.deg2rad(newAngle)),3)) + " Y portion = " + str(round(np.sin(np.deg2rad(newAngle)),3)))
  return (round(np.cos(np.deg2rad(newAngle)),3), round(np.sin(np.deg2rad(newAngle)),3))

#Lets the pause mechanic work
def onClick(event):
    global pause
    pause ^= True

#Create a player / dot
#|Add health, elo, mmr
class player(object):
  def __init__(self, side, slot, elo, mmr):
    #assign passed parameters to object
    self.side = side
    self.slot = slot
    self.health = 1
    self.elo = elo
    self.mmr = mmr

    #blue starts up top, red below
    if self.side == 0:
      self.y = 10 - (2 * np.random.random_sample()) 
    else: 
      self.y = (2 * np.random.random_sample())
    self.x = 10 * np.random.random_sample()
    #give them a velocity
    self.velx = self.generate_new_vel()
    self.vely = self.generate_new_vel()

  def generate_new_vel(self):
    return (np.random.random_sample() - 0.5) / 5

  def location(self):
    return "Player located at (" + str(self.x) + "," + str(self.y) + ")"

  def takeAim(self, opponents):
    #get mindistance to each opponent, keep lowest and direction
    minDistance = 20

    for i, opponent in enumerate(opponents):
      opponentDistance = math.sqrt( (self.x - opponent.x) ** 2 + (self.y - opponent.y) ** 2)
      if opponentDistance < minDistance:
        minDistance = opponentDistance
        self.aimX = opponent.x
        self.aimY = opponent.y
        self.aimMomX = opponent.velx
        self.aimMomY = opponent.vely

    verbose(False, "Player " + str(self.slot) + " (" + str(self.side) + ") at (" + str(round(self.x,2)) + "," + str(round(self.y,2)) + ") took aim at (" + str(round(self.aimX,2)) + "," + str(round(self.aimY,2)) + ")" )

  def move(self):
    #move randomly
      if np.random.random_sample() < 0.9:
        self.x = self.x + self.velx
        self.y = self.y + self.vely
      else:

        #if change x direction, shoot laser
        temp = self.generate_new_vel()
        if ((self.x <= 0 <= temp) or (self.x >= 0 >= temp)):
          verbose(False, "Player shot")

        self.velx = temp
        self.vely = self.generate_new_vel()
        self.x = self.x + self.velx
        self.y = self.y + self.vely

      #Don't go outside the boundaries
      if self.side == 0:
        maxHeight = 10
        minHeight = 5
      else:
        maxHeight = 5
        minHeight = 0

      if self.x >= 10:
        self.x = 10
        self.velx = -1 * self.velx
      if self.x <= 0:
        self.x = 0
        self.velx = -1 * self.velx
      if self.y >= maxHeight:
        self.y = maxHeight
        self.vely = -1 * self.vely
      if self.y <= minHeight:
        self.y = minHeight
        self.velx = -1 * self.vely

def examineDamage(characters, weapons):
  deletedW = 0
  deletedC = 0

  #check for collisions loop through lasers then players
  for i, player in enumerate(characters):

    for j, laser in enumerate(weapons):
      if math.sqrt( (characters[i-deletedC].x - weapons[j-deletedW].x) ** 2 + (characters[i-deletedC].y - weapons[j-deletedW].y) ** 2) < 0.15 and characters[i-deletedC].side != weapons[j-deletedW].side:
        #Take one point of damage
        verbose(False, "Player #" + str(characters[i-deletedC].slot) + ", team #" + str(characters[i-deletedC].side) + ",  at (" + str(round(characters[i-deletedC].x,1)) + "," + str(round(characters[i-deletedC].y,1)) + ") was hit and took damage.")
        characters[i-deletedC].health = characters[i-deletedC].health - 1
        weapons = np.delete(weapons, j-deletedW)
        deletedW = deletedW + 1
        if characters[i-deletedC].health == 0:
          verbose(False, "\\/\\/\\/Player #" + str(characters[i-deletedC].slot) + ", team #" + str(characters[i-deletedC].side) + ",  at (" + str(round(characters[i-deletedC].x,1)) + "," + str(round(characters[i-deletedC].y,1)) + ") was hit and ran out of health so they were removed")
          verbose(False, "There are " + str(len(characters)) + " characters and " + str(len(weapons)) + " weapons")
          verbose(False, "/\\/\\/\\Deleting character " + str(i) + " and weapon " + str(j))
          characters = np.delete(characters, i-deletedC)
          deletedC = deletedC + 1
        break

  return (characters, weapons)

def moveLasers(weapons):
    deleted = 0 
    verbose(False, "There are " + str(len(weapons)) + " weapons")
    for i, laser in enumerate(weapons):
      verbose(False, "Weapon positon at (" + str(weapons[i-deleted].x) + "," + str(weapons[i-deleted].y) + ") " 
        + str(weapons[i-deleted].x > 10) + " " + str(weapons[i-deleted].x < 0) + " " + str(weapons[i-deleted].y > 10) + " " + str(weapons[i-deleted].y < 0))
      weapons[i-deleted].shoot()
      if (weapons[i-deleted].x > 10 or weapons[i-deleted].x < 0 or weapons[i-deleted].y > 10 or weapons[i-deleted].y < 0):
        verbose(False, "deleting laser (" + str(round(weapons[i-deleted].x,1)) + "," + str(round(weapons[i-deleted].y,1)) + ")")
        verbose(False, "There are " + str(len(weapons)) + " and need to delete #" + str(i-deleted))
        weapons = np.delete(weapons, i-deleted)
        deleted = deleted + 1

    return weapons

def randInt(range):
  return (1 + math.floor(range * np.random.random_sample()))

def playerSkillInfo(players, team):
  totElo = 0
  totMMR = 0 
  for j, player in enumerate(players):
    verbose(True, "Player #" + str(players[j].slot) + ", team #" + str(players[j].side) + ",  has elo = " + str(round(players[j].elo,0)) + ", and mmr = " + str(round(players[j].mmr,0)))
    totElo += players[j].elo
    totMMR += players[j].mmr

  verbose(True, "Team " + str(team) + " total elo = " + str(totElo) + " and total mmr = " + str(totMMR))

###Start the simulation
#Initialize players
#|add 2d array (or nd array structure)
playersT1 = np.array([player(0, i, randInt(100), randInt(10)) for i in xrange(N/2)])
playersT1 = np.array([player(0, i, 100, 1) for i in xrange(N/2)])
playersT2 = np.array([player(1, i, randInt(100), randInt(10)) for i in xrange(N/2)])
players = np.concatenate((playersT1,playersT2))
lasersT1 = np.array([])
lasersT2 = np.array([])
lasers = np.array([])

#Summary player skill info
playerSkillInfo(playersT1,0)
playerSkillInfo(playersT2,1)
    
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

b1, = axes.plot([laser.x for laser in lasersT1],
               [laser.y for laser in lasersT1], 'g*', markersize = 8)

b2, = axes.plot([laser.x for laser in lasersT2],
               [laser.y for laser in lasersT2], 'g*', markersize = 8)

#UI Improvements
#playing map
axes.add_patch(patches.Rectangle((0, 0), 10, 10, color = '#940dba'))
axes.add_patch(patches.Rectangle((0.2, 0.2), 9.6, 9.6, color = '#ffffff'))
axes.add_patch(patches.Rectangle((0, 5), 10, .2, color = '#940dba'))

#time stamp
time_template = 'Time = %.1f s'
time_text = axes.text(.43, 0.92, '', transform=axes.transAxes)
win_text = axes.text(.42,.08, '', transform = axes.transAxes)

#Track winner
winner = "None"
lastFrame = 9999

#Animation function, called sequentially 
#|will have to make this a repeatable function w/ stop animation
def animate(i):
  #Create the lazers
  class laser(object):
    def __init__(self, side, x, y, momX, momY, playerElo, playerAimX, playerAimY, playerAimMomX, playerAimMomY):

      #Bullet speed factor
      speedFactor = 4

      #initial position
      self.side = side
      self.x = x
      self.y = y
      self.initMomX = momX
      self.initMomY = momY
      self.playerElo = playerElo
      self.playerAimX = playerAimX
      self.playerAimY = playerAimY
      self.playerAimMomX = playerAimMomX
      self.playerAimMomY = playerAimMomY

      #blue shoots down, red shoots up
      xLeg = playerAimX - self.x
      yLeg = playerAimY - self.y
      desiredAngle = calcAngle(xLeg, yLeg)
      rando = random.randint(-90,90)
      inaccuracy = rando * (1 - playerElo / 100)
      verbose(False, "Side " + str(self.side) + " aim X " + str(round(playerAimX,2)) + " aim Y " + str(round(playerAimY,2)) )
      verbose(False, "Side " + str(self.side) + " leg X " + str(round(xLeg,2)) + " leg Y " + str(round(yLeg,2)) )
      verbose(False, "Side " + str(self.side) + " elo = " + str(playerElo) + " angle determined to be " + str(desiredAngle))
      verbose(False, "Side " + str(self.side) + " rando = " + str(rando) + " should be off by " + str(round(inaccuracy,2)) + " degrees." )
      shotX, shotY = calcShot(desiredAngle, inaccuracy)
      normFactor = abs(shotX) + abs(shotY)
      self.velx = shotX / normFactor / speedFactor
      self.vely = shotY / normFactor / speedFactor

    def shoot(self):
      #straight line
      self.y = self.y + self.vely
      self.x = self.x + self.velx

  if not pause:
    #Pass kill counts through so indexing doesnt reset or itll throw enumerators off
    global lasersT1
    global lasersT2
    global lasers
    global playersT1
    global playersT2
    global players
    global run_start
    global pause
    global winner
    global lastFrame
    global plt

    #Set time
    t = time.time() - run_start
    time_text.set_text(time_template%(t))

    #Check to see if players took damage
    playersT1, lasersT2 = examineDamage(playersT1, lasersT2)
    playersT2, lasersT1 = examineDamage(playersT2, lasersT1)
    players = np.concatenate((playersT1,playersT2))
    
    #move lasers that didn't hit a player one time
    lasersT1 = moveLasers(lasersT1)
    lasersT2 = moveLasers(lasersT2)

    #Take aim, find closets opponent and direction
    for j, player in enumerate(playersT1):
      playersT1[j].takeAim(playersT2)
    for j, player in enumerate(playersT2):
      playersT2[j].takeAim(playersT1)

    #Move players that were not hit and shoot if mmr allows
    for j, player in enumerate(players):
      temp = players[j].velx
      players[j].move()
      verbose(False, "Testing laser generation side " + str(players[j].side) + " #" + str(players[j].slot) + " at (" + str(round(players[j].x,1)) +  "," + str(round(players[j].y,1)) + ") | i = " + str(i) + " and mmr = " + str(players[j].mmr) + " so mod = " + str(i % players[j].mmr))
      if (i % (5 * players[j].mmr)) == 0:
        verbose(False, "Generating laser side " + str(players[j].side) + " #" + str(players[j].slot) + " at (" + str(round(players[j].x,1)) +  "," + str(round(players[j].y,1)) + ") | i = " + str(i) + " and mmr = " + str(players[j].mmr))
        if players[j].side == 0:
            lasersT1 = np.concatenate((lasersT1, [laser(players[j].side, players[j].x, players[j].y, players[j].velx, players[j].vely, players[j].elo, players[j].aimX, players[j].aimY, players[j].aimMomX, players[j].aimMomY)]))
        else:
            lasersT2 = np.concatenate((lasersT2, [laser(players[j].side, players[j].x, players[j].y, players[j].velx, players[j].vely, players[j].elo, players[j].aimX, players[j].aimY, players[j].aimMomX, players[j].aimMomY)]))

    #update laser array after checking for hits and creations
    lasers = np.concatenate((lasersT1,lasersT2))

    #|add display targetting lines possibility
    #display lasers
    b1.set_data([laser.x for laser in lasersT1],
               [laser.y for laser in lasersT1])

    b2.set_data([laser.x for laser in lasersT2],
               [laser.y for laser in lasersT2])

    #dispay team 1 blue
    p1.set_data([player.x for player in playersT1],
                [player.y for player in playersT1])

    #display team 2 red
    p2.set_data([player.x for player in playersT2],
                [player.y for player in playersT2])

  #Check if the game is over
  if not playersT1.any() and lastFrame == 9999: 
    lastFrame = i
    win_text.set_text("Red Team Wins!")
    winner = "RED" 
  if not playersT2.any() and lastFrame == 9999:
    lastFrame = i
    win_text.set_text("Blue Team Wins!")
    winner = "BLUE"
  if i == lastFrame + 1:
    time.sleep(1)
    plt.close()

  #helps with debugging run away errors
  time.sleep(0)

  return (p1, p2, b1, b2,)

#Call the animator, 
run_start = time.time()
figure.canvas.mpl_connect('button_press_event', onClick)
animator = animation.FuncAnimation(figure, animate, blit=False, repeat = True, frames = 200, interval = 20)

#|Fix the saving function, do we need rasp pi?
#animator.save('basic_animation.gif', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()

print("THE WINNER IS " + winner + "!")












