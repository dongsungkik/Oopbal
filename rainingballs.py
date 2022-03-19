# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 17:01:39 2022

@author: dongs
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:15:33 2022

@author: dongs
"""
'''d'''
import pygame
import random


pygame.init()

black = (64,64,64)
white = (255,255,255)
darker_white = (200,200,200)
red = (255,0,0)
blue = (0,0,200)
lightyellow = (255,255,102)

display_sizex = 300
display_sizey = 500
display_output = [display_sizex, display_sizey]
screen = pygame.display.set_mode(display_output)
pygame.display.set_caption("Bouncing balls")
Bounce = False
clock = pygame.time.Clock()

ball_size = 10
frame_rate = 60
big_radius_circle = 500
time_for_ball_to_spawn0 = 20 # number of while loops for the ball to spawn
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
    screen.blit(display_game_over, (int(display_sizex/5), int(display_sizey/6) ))
    display_restart = font.render("Press r to restart", True, red)
    screen.blit(display_restart, (int(display_sizex/11), int(3*display_sizey/12)))
    gameover = True
    
class Rain:
    
    '''
    the incoming balls, centre ball is when angle = 0
    '''
    
    def __init__(self, x,y, speedx, speedy, sizex, sizey, clr, ax = 0, ay = 0):
        #big radius is the size of the circle that the big balls spawn from
        #it's mainly here so i can make the central ball by big_rad = 0
        
        self.__posx = x
        self.__posy = y
        self.__sizex = sizex
        self.__sizey = sizey
        self.__accx = ax
        self.__accy = ay
        self.__clr = clr
        
        self.__speedx = speedx
        self.__speedy = speedy
        
    def get_speed(self):
        return self.__speedx, self.__speedy
    
    def get_posx(self):
        return self.__posx
    
    def get_posy(self):
        return self.__posy
    
    def get_colour(self):
        return self.__colour
    
    def get_time(self):
        return self.__time
        
    def move(self, dt):
        self.__posx += self.__speedx * dt
        self.__posy += self.__speedy * dt
        
    def accerelate(self, dt):
        self.__speedx += self.__accx * dt
        self.__speedy += self.__accy * dt
        
    def draw_rain(self):
        
        pygame.draw.rect(screen , self.__clr, pygame.Rect(
            self.__posx, self.__posy,
             self.__sizex , self.__sizey))
        
    def check_wall(self, lowerbound, upperbound, dt):
        if self.__posx + self.__speedx * dt < lowerbound or self.__posx + self.__speedx * dt > upperbound :
            pass
        else:
            self.move(dt)
            
    def change_speed(self):
        self.__speedx = - self.__speedx
        
rain_sizex = 5
rain_sizey = 10
rain_drop = 10
block_speed = 10
block_size = 20
rain_list = []

central_block1 = Rain( display_sizex/2 - block_size, display_sizey - block_size, block_speed, 0 , block_size, block_size, black )
central_block2 = Rain( display_sizex/2 + block_size, display_sizey - block_size, -block_speed, 0 , block_size, block_size, black )
while Bounce == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Bounce = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                central_block1.change_speed()
                central_block2.change_speed()
             
            elif event.key == pygame.K_r and gameover:
                gameover = False
                rain_list = []
                counter = 0
                score = 0
                diffuclty = 0
                spawn_rate = 10000000000
            
    screen.fill(background_colour)
        
    spawn_rate += frame_rate
    
    if gameover == True:
        central_block1.draw_rain()
        central_block2.draw_rain()
        pygame.draw.rect( screen, lightyellow, pygame.Rect(central_block1.get_posx(), central_block1.get_posy(), block_size, block_size/2))
        pygame.draw.rect( screen, lightyellow, pygame.Rect(central_block2.get_posx(), central_block2.get_posy(), block_size, block_size/2))
        for i in rain_list:
            i.draw_rain()
        
        #drawing balls but not moving them, giving an illusion that game is paused
        
        clock.tick(frame_rate)
        game_over()
        show_score(textX,textY)
        pygame.display.flip()
        continue

    
    if spawn_rate >= time_for_ball_to_spawn * frame_rate:
    #spawning balls at certain interval
        x = random.uniform(0, display_sizex - rain_sizex)
        rain_list.append(Rain(x , 0, 0, rain_drop, rain_sizex, rain_sizey, blue ))
        
        '''
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
        '''
        spawn_rate = 0

    #deleting balls that left the circle
    
    
    
    
    
    
    central_block1.check_wall(0 , display_sizex/2 - block_size ,dt)
    central_block1.draw_rain()
    central_block2.check_wall(display_sizex/2 , display_sizex - block_size, dt)
    central_block2.draw_rain()
    pygame.draw.rect( screen, lightyellow, pygame.Rect(central_block1.get_posx(), central_block1.get_posy(), block_size, block_size/2))
    pygame.draw.rect( screen, lightyellow, pygame.Rect(central_block2.get_posx(), central_block2.get_posy(), block_size, block_size/2))
    
    for i in rain_list:
        if i.get_posy() > display_sizey:
            del rain_list[0]
            print(len(rain_list))
            score += 1
        i.draw_rain()
        i.accerelate(dt)
        i.move(dt) 
    
    for i in rain_list:
    
        posy = i.get_posy()
        posx = i.get_posx()
        if i.get_posy() >= display_sizey - block_size:
            if  central_block1.get_posx() > posx - block_size and central_block1.get_posx() <= posx + rain_sizex:
                game_over()
                continue
            elif central_block2.get_posx() > posx - block_size and central_block2.get_posx() <= posx + rain_sizex:
                game_over()
                continue
    
        
    counter += 1
    
    clock.tick(frame_rate)
    show_score(textX,textY)
    pygame.display.flip()
    
    #if time_for_ball_to_spawn < 27:
    #    continue
        
    #difficulty = score // 10
    #time_for_ball_to_spawn = time_for_ball_to_spawn0 - difficulty    
    
pygame.display.quit()
pygame.quit()