"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import time

def verbose(loudOption,printMe):
    if loudOption:
        print(printMe)

# Initializing number of dots
N = 1

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim = (-2,12), ylim = (-2,12))
dots = []
lasers = []

d, = ax.plot([dot.x for dot in dots],
              [dot.y for dot in dots], 
              'bo', 
              markersize = 10)

b, = ax.plot([laser.x for laser in lasers],
               [laser.y for laser in lasers], 'g*', markersize = 5)

#circle = plt.Circle((5, 5), 1, color='b', fill=False)
#ax.add_artist(circle)


# animation function.  This is called sequentially
def animate(i):
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


    # Creating dot class
    class dot(object):
        def __init__(self):
            self.side = 1
            self.x = 10 * np.random.random_sample()
            self.y = 10 * np.random.random_sample()
            self.velx = self.generate_new_vel()
            self.vely = self.generate_new_vel()

        def generate_new_vel(self):
            return (np.random.random_sample() - 0.5) / 5

        def location(self):
            return "Player located at (" + str(self.x) + "," + str(self.y) + ")"

        def move(self):
            def distance(x1, y1, x2, y2):
                return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            def inside(x1, y1):
                if distance(x1, y1, 5, 5) <= 1:
                    return True
                else:
                    return False

            def calc_dist(d):
                ret = 0
                for x in dots:
                    if inside(x.x, x.y) and x != d:                            
                        ret = ret + distance(x.x, x.y, d.x, d.y)
                return ret

            # if dot is inside the circle it tries to maximize the distances to
            # other dots inside circle
            if inside(self.x, self.y):
                dist = calc_dist(self)
                for i in xrange(1, 10):
                    self.velx = self.generate_new_vel()
                    self.vely = self.generate_new_vel()
                    self.x = self.x + self.velx
                    self.y = self.y + self.vely
                    if calc_dist(self) <= dist or not inside(self.x, self.y):
                        self.x = self.x - self.velx
                        self.y = self.y - self.vely
            else:
                if np.random.random_sample() < 0.95:
                    self.x = self.x + self.velx
                    self.y = self.y + self.vely
                else:
                    self.velx = self.generate_new_vel()
                    self.vely = self.generate_new_vel()
                    self.x = self.x + self.velx
                    self.y = self.y + self.vely
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
                    self.vely = -1 * self.vely

    #Run the animnation
    global dots 
    global d
    global lasers
    global b
    global plt
    global ax
    global fig

    verbose(True, "LOOP : " + str(i))
    if i == 0:
        #Do nothing, 0 runs twice
        i = i 
        dots =[]
    #First loop
    elif i == 1:
        # Initializing dots
        dots = [dot() for i in xrange(N)]

        for dot in dots:
            verbose(False, "(" + str(dot.x) + "," + str(dot.y) + ")")
    elif (i % 25 == 0 and i > 0):
        for j, dot in enumerate(dots):
            if len(lasers) == 0:
                lasers = [laser(dots[j].side, dots[j].x, dots[j].y)]
            else:
                lasers = np.concatenate(((lasers, [laser(dots[j].side, dots[j].x, dots[j].y)])))
            #print("Laser at (" + str(dots[j].x) + "," + str(dots[j].y + ")"))

    elif i <= 200:

        for dot in dots:
            dot.move()
            verbose(False, "(" + str(dot.x) + "," + str(dot.y) + ")")
        
        for laser in lasers:
            laser.shoot()
    elif i == 200:
        verbose(False, "STOP ANIMATION")


    #time.sleep(.25)
    ax = plt.axes(xlim = (-2,12), ylim = (-2,12))

    #display lasers
    #b.set_data([laser.x for laser in lasers],
     #           [laser.y for laser in lasers], 'g*')


    #dispay team 1 blue
    verbose(True, dots[0].location())
    b.set_data([player.x for player in players],
                [player.y for player in players])

    
    return (b, )


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=200, interval=1, repeat = False)
plt.show()
plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()








