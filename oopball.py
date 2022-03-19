# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:15:33 2022

@author: dongs
"""

import pygame
import random
import numpy as np

pygame.init()

black = (64,64,64)
white = (255,255,255)
darker_white = (200,200,200)
red = (255,0,0)
blue = (0,0,200)
lightyellow = (255,255,102)

display_size = 1000
display_output = [display_size, display_size]
screen = pygame.display.set_mode(display_output)
pygame.display.set_caption("Bouncing balls")
Bounce = False
clock = pygame.time.Clock()

ball_size = 10
frame_rate = 60
big_radius_circle = 500
time_for_ball_to_spawn0 = 40 # number of while loops for the ball to spawn
ball_speed = 5

time_for_ball_to_spawn = time_for_ball_to_spawn0


colour0 = lightyellow #central colour
colour1 = black
background_colour = darker_white #background colour

ball_list = []
counter = 0
score = 0
difficulty = 0

font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

dt = 0.5

spawn_rate = time_for_ball_to_spawn * frame_rate -1
# in case you decide to change frame rate, doing this makes the number of loops 
# for ball to spawn the same as time_for_ball_to_spawn.

gameover = False

def show_score(x,y):
    scorev = font.render("Score: " + str(score), True, blue)
    screen.blit(scorev, (x,y))
    
def game_over():
    
    global gameover
    display_game_over = font.render("Game Over", True , red)
    screen.blit(display_game_over, (int(display_size/3), int(display_size/6) ))
    display_restart = font.render("Press r to restart", True, red)
    screen.blit(display_restart, (int(display_size/3), int(3*display_size/12)))
    if (nearmisses != 21):
        nearmiss = font.render("Dodged by " + str(nearmisses-20) + " pixels", True, red)
        screen.blit(nearmiss, (int(display_size/3), int(5*display_size/12)))
    hit = font.render("Hit by " + str(20 - hit_dist ) + " pixels", True, red)
    screen.blit(hit, (int(display_size/3), int(4*display_size/12)))
    gameover = True
    
class Ball:
    
    '''
    the incoming balls, centre ball is when angle = 0
    '''
    
    def __init__(self, angle, speed, radius, big_radius,  clr, counter_for_time, a = 0):
        #big radius is the size of the circle that the big balls spawn from
        #it's mainly here so i can make the central ball by big_rad = 0
        
        self.__posx = big_radius + big_radius * np.cos(angle)
        self.__posy = big_radius + big_radius * np.sin(angle)
        self.__big_radius = big_radius
        self.__radius = radius
        self.__init_time = counter_for_time
        self.__acc = a
        self.__accx = -a * np.cos(angle)
        self.__accy = -a * np.sin(angle)
        
        if speed == 0 and a != 0:
            self.__speedx = - 0.000001 * np.cos(angle)
            self.__speedy = - 0.000001 * np.sin(angle)
            self.__time = counter_for_time + (big_radius_circle - 2 * radius )/ (dt*ball_speed)
            #time taken / number of frames until ball hits as 
            # O--->     o to          Oo
        else:
            self.__time = counter_for_time + (big_radius_circle - 2 * radius )/ (dt*speed)
            self.__speedx = -speed * np.cos(angle)
            self.__speedy = -speed * np .sin(angle)
        
        #time taken/ number of frames for the incoming ball to hit the centre ball
        self.__radius = radius
        
        
        if clr == 0:
            self.__colour = colour0
        else:
            self.__colour = colour1
            
        #only two colours, so i have used 0 and 1 to distinguish between the two colours
        #doing this since i'll need to change between the two
        
    def get_speed(self):
        return self.__speedx, self.__speedy
    
    def get_pos(self):
        return self.__posx, self.__posy
    
    def get_colour(self):
        return self.__colour
    
    def get_time(self):
        return self.__time
    
    def get_final_time(self):
        #time  / number of frames taken to phase through as such:
        # O ------>    o   to           oO---->
        if self.__acc == 0:
            t = (self.__big_radius + 2 * self.__radius) / (dt * np.linalg.norm([self.get_speed()]))
        else:
            t = np.sqrt(2 * self.__big_radius /( self.__acc * (dt **2)))
        return t + self.__init_time
        
    def move(self, dt):
        self.__posx += self.__speedx * dt
        self.__posy += self.__speedy * dt
        
    def accerelate(self, dt):
        self.__speedx += self.__accx * dt
        self.__speedy += self.__accy * dt
        
    def draw_ball(self):
        
        pygame.draw.circle(screen , self.__colour, [self.__posx, self.__posy], self.__radius, 0)
        
    def change_colour(self):
        if self.__colour == colour0:
            self.__colour = colour1
        else:
            self.__colour = colour0
        

'''
if speed = 0, s = 1/2 at^2, 
s = ut 
a = 2u / t
 u = ball_speed,
 s = big_radius_circle - 2* ball_size 
 t = s / u 
 a = 2u ( s/u) = 2u^2 / s
'''
        
nearmisses = 21
hit_dist = 20
centre_ball = Ball(np.pi/4, ball_speed, ball_size, big_radius_circle * 2 / (2 + np.sqrt(2)), 1, 0)

while Bounce == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Bounce = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                centre_ball.change_colour()
                
            elif event.key == pygame.K_r and gameover:
                gameover = False
                ball_list = []
                counter = 0
                score = 0
                diffuclty = 0
                spawn_rate = 10000000000
    
    screen.fill(background_colour)
    
    pygame.draw.circle(screen, colour1, [display_size /2 , display_size /2] , big_radius_circle + 5, 0 )
    pygame.draw.circle(screen, background_colour, [display_size /2 , display_size /2] , big_radius_circle, 0 )
    
    centre_ball.draw_ball()
    pygame.draw.line(screen, red, (502,500) , (498, 500), 1)
    pygame.draw.line(screen, red, (500,502) , (500, 498), 1)
    
    spawn_rate += frame_rate
    
    if gameover == True:
        for i in ball_list:
            i.draw_ball()         
        #drawing balls but not moving them, giving an illusion that game is paused
        
        clock.tick(frame_rate)
        game_over()
        show_score(textX,textY)
        pygame.display.flip()
        continue

    
    if spawn_rate >= time_for_ball_to_spawn * frame_rate:
    #spawning balls at certain interval
        angle = random.uniform(0,2*np.pi)
        k = random.randint(0,1)
        j = random.randint(0,10)
        #randomly spawn accelerated balls 
        
        if difficulty >= 5 and difficulty < 8and difficulty - 3 >= j:
            #acc is such that the incoming balls never reach the central ball
            #at the same time.
            acc = 2 * (ball_speed ** 2) / (big_radius_circle - 2 * ball_size)
            ball_list.append(Ball(angle, 0, ball_size, big_radius_circle, k , counter, acc ))
            print("FASTBALL")
        elif difficulty > 8 and j <= 5:
            acc = 2 * (ball_speed ** 2) / (big_radius_circle - 2 * ball_size)
            ball_list.append(Ball(angle, 0, ball_size, big_radius_circle, k , counter, acc ))
        else:
            ball_list.append(Ball(angle, ball_speed, ball_size, big_radius_circle, k, counter))
        
        spawn_rate = 0

    #deleting balls that left the circle
    if counter - ball_list[0].get_time() - 2 * ball_size / ball_speed > 2 * big_radius_circle / ball_speed:
        del ball_list[0]
        print(len(ball_list))
   
    
    for i in ball_list:
    
        final_time = i.get_final_time() - counter
        
        if i.get_time() <= counter and final_time >= 0:
            print(final_time)
            if i.get_colour() != centre_ball.get_colour():
                miss = np.linalg.norm([i.get_pos()[0]- 500, i.get_pos()[1] - 500])
                if miss > 20 and miss < nearmisses:
                    nearmisses = miss
                if miss <= 20:
                    hit_dist = miss
                    game_over()
                    continue
                    
                    
            elif final_time == 0:
                score += 1
                
        i.draw_ball()
        i.accerelate(dt)
        i.move(dt) 
        
        
    counter += 1
    
    clock.tick(frame_rate)
    show_score(textX,textY)
    pygame.display.flip()
    if time_for_ball_to_spawn < 27:
        continue
        
    difficulty = score // 10
    time_for_ball_to_spawn = time_for_ball_to_spawn0 - difficulty    
    
pygame.display.quit()
pygame.quit()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        