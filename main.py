# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Run this the first time
# %matplotlib qt

# =============================================================================
# Setup (Actually don't change these because 80% of the time game will break)
# =============================================================================
# size of the board
boardy = 100
boardx = 200
# length of the bar
barlength = 20 
# bar velocity
barvel = .4   #units/dt
# ball velocity
ballvel = 1.2   #units/dt
# timestep of the game
dt = 1.5  #keep this constant, unless wanting to do slo/fast-mo
# pause time before starting the game
waittime = 50
# total frame
frames = 800

plt.style.use('dark_background')

fig = plt.figure(figsize = (12,7), dpi = 100)
ax = plt.axes(xlim=(0, boardx), ylim=(0, boardy))
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

plot_dash, = ax.plot([], [], '--', c = 'w', lw = 1)
# customize ball and bars' colour here by changing the keyword mfc
plot_ball, = ax.plot([], [], 'o', mec = 'k', mfc = 'w', ms = 10)
plot_barL, = ax.plot([], [], '-', lw = 10)
plot_barR, = ax.plot([], [], '-', lw = 10)

class Ball:
    def __init__(self, position, velocity):
        self.xvel, self.yvel = np.array(velocity).astype(float)
        self.xpos, self.ypos = np.array(position).astype(float)
    
    def show_pos(self):
        print("The ball is at x =", self.xpos, "y =", self.ypos)
  
    def update(self, dt):
        # timestep update
        self.xpos += self.xvel * dt
        self.ypos += self.yvel * dt
        
        # boundary problems
        if self.ypos + 2 >= boardy or self.ypos - 2 <= 0:
            self.yvel = -self.yvel
            
        # collisional area covered by the bar
        # techinically only need to care about the front side(?)
        if (self.xpos >= barR.xpos - 3) or (self.xpos <= barL.xpos + 3):
                # check if position of ball is within height of bar
                if (self.ypos <= barR.ypos + barR.len/2 and\
                    self.ypos >= barR.ypos - barR.len/2) or\
                    (self.ypos <= barL.ypos + barL.len/2 and\
                    self.ypos >= barL.ypos - barL.len/2):
                    # this will fix zigzag problem
                    if (self.xpos > boardx/2 and self.xvel > 0) or\
                        (self.xpos < boardx/2 and self.xvel < 0):
                        self.xvel = -self.xvel

class BarLeft:
    def __init__(self, position, length):
        self.xpos, self.ypos = np.array(position).astype(float) # - length to shorten (?)
        self.len = length
        self.plt = np.array([[position[0], position[0]],\
                             [position[1]-length/2, position[1]+length/2]])
        
    def update(self, dt):
        # If bar hits top/bottom after updating, don't update
        if self.ypos + (dt*barvel) + self.len/2 >= boardy\
            or self.ypos - (dt*barvel) - self.len/2 <= 0:
                if (ball.ypos > (boardy - self.len) and\
                    self.ypos > (boardy - self.len)) or\
                    (ball.ypos < self.len and self.ypos < self.len):
                        return
        # Otherwise, update position based on y-coord of ball.
        # Only update when ball is within half of boardlength.
        if ball.xpos > boardx/2:
            return
        # Do not update if ball is post-collision
        if ball.xvel > 0:
            return 
        
        # Now, make the bar chase the ball
        # Find difference in position
        pos_diff = ball.ypos - self.ypos
        if pos_diff > 0: #and abs(pos_diff) < self.len/2:
            if pos_diff <= dt * (barvel):
                pass
            else:
                self.ypos += barvel * dt
        elif pos_diff < 0: # and abs(pos_diff) < self.len/2:
            if abs(pos_diff) <= dt * (barvel):
                pass
            else:
                self.ypos -= barvel * dt
        # elif ball.
        # Update plot based on position
        self.plt = np.array([[self.xpos, self.xpos],\
                             [self.ypos-self.len/2,\
                              self.ypos+self.len/2]])
    
class BarRight:
    def __init__(self, position, length):
        self.xpos, self.ypos = np.array(position).astype(float) # - length to shorten (?)
        self.len = length
        self.plt = np.array([[position[0], position[0]],\
                             [position[1]-length/2, position[1]+length/2]])
        
    def update(self, dt):
        # If bar hits top/bottom after updating, don't update
        if self.ypos + (dt*barvel) + self.len/2 >= boardy\
            or self.ypos - (dt*barvel) - self.len/2 <= 0:
                if (ball.ypos > (boardy - self.len) and\
                    self.ypos > (boardy - self.len)) or\
                    (ball.ypos < self.len and self.ypos < self.len):
                        return
        # Otherwise, update position based on y-coord of ball.
        # Only update when ball is within half of boardlength.
        if ball.xpos < boardx/2:
            return
        # Do not update if ball is post-collision
        if ball.xvel < 0:
            return 
        
        # Make bars shrink every 2 turns
        # if dt%50 == 0: #extreme
            # self.len -= 1
        # Now, make the bar chase the ball
        # Find difference in position
        pos_diff = ball.ypos - self.ypos
        if pos_diff > 0: #and abs(pos_diff) < self.len/2:
            if pos_diff <= dt * (barvel):
                pass
            else:
                self.ypos += barvel * dt
        elif pos_diff < 0: # and abs(pos_diff) < self.len/2:
            if abs(pos_diff) <= dt * (barvel):
                pass
            else:
                self.ypos -= barvel * dt
        # elif ball.
        # Update plot based on position
        self.plt = np.array([[self.xpos, self.xpos],\
                             [self.ypos-self.len/2,\
                              self.ypos+self.len/2]])

# =============================================================================
# Initial condition
# =============================================================================
    
def init():
    global random_angle, ball, barR, barL
    # random initial angle
    random_angle = np.deg2rad(np.random.choice([np.random.uniform(320, 400),\
                                     np.random.uniform(140, 220)]))
    ball = Ball([boardx/2,boardy/2],\
                [ballvel*np.cos(random_angle), ballvel*np.sin(random_angle)])
    barR = BarRight([boardx-5, boardy/2], barlength)
    barL = BarLeft([5, boardy/2], barlength)
    plot_ball.set_data(ball.xpos, ball.ypos)
    plot_barL.set_data(barL.plt)
    plot_barR.set_data(barR.plt)
    plot_dash.set_data([boardx/2, boardx/2],[0, boardy])
    return plot_ball, plot_barR, plot_barL, plot_dash,

# =============================================================================
# Animation
# =============================================================================

# animation 
def animate(i):
    # let ball stay in the middle for a bit
    if i > waittime: 
        # slowly ramp up ball velocity
        # if i%50 == 0:
            # ball.xvel *= 1.5
            # ball.yvel *= 1.5
        # reset board if bars fail to catch ball
        if ball.xpos > barR.xpos or ball.xpos < barL.xpos:
            if (ball.xpos > boardx and (ball.ypos > barR.ypos or ball.ypos < barR.ypos)) or\
                (ball.xpos < 0 and (ball.ypos > barL.ypos or ball.ypos < barL.ypos)):
                anim.frame_seq = anim.new_frame_seq() 
                init()
        ball.update(dt)
        barR.update(dt)
        barL.update(dt)
        plot_ball.set_data(ball.xpos, ball.ypos)
        plot_barL.set_data(barL.plt[0], barL.plt[1])
        plot_barR.set_data(barR.plt[0], barR.plt[1])
    return plot_ball, plot_barR, plot_barL, plot_dash,
        

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=frames, #change length of the animation
                               interval=.1, # change to slow/fast motion
                                blit=True,
                                repeat = True
                               )

# =============================================================================
# Save movie
# =============================================================================
# path2save = r"/Users/jwt/Documents/Code/Ball_Game/"
# anim.save(path2save+'ball_game_stage6.mp4', fps=30,
#           extra_args=['-vcodec', 'libx264'])

plt.show()
