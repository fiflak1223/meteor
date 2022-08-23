import pygame
import math
import random
import time
from sys import exit

pygame.init()
pygame.display.set_caption('METEOR')

class Bullet: #container for bullet data
    def __init__(self, x,y,bRect,bSurf):
        self.alive = True
        self.y = abs(640-x)/30 #distance do y axis (ship)
        self.x = abs(360-y)/30
        self.rect = bRect
        self.surf = bSurf
        if x >= 640 and y <= 360: # I quarter 
            self.x *= -1
        elif x >= 640 and y >= 360: # IV quarter
            pass
        elif x <= 640 and y <= 360: # II quarter
            self.y *= -1
            self.x *= -1
        elif x <= 640 and y >= 360: # III quarter
            self.y *= -1

class Oponent: #container for oponent data
    def __init__(self): #it set x to -200 or 1500 and random y OR y to -100 or 900 and random x
        self.alive = True
        if random.randint(0,1):
            if random.randint(0,1):
                self.x = -200
            else:
                self.x = 1500
            self.y = random.randint(-100,900)
        else:
            if random.randint(0,1):
                self.y = -100
            else:
                self.y = 900
            self.x = random.randint(-200,1500)
        self.surf = pygame.image.load('meteor.png').convert_alpha()
        self.rect = self.surf.get_rect(center = (self.x,self.y))

        self.ydist = abs(640-self.x)/30 
        self.xdist = abs(360-self.y)/30
        if self.x >= 640 and self.y <= 360: # I quarter 
            self.ydist *= -1
        if self.x >= 640 and self.y >= 360: # IV quarter 
            self.xdist *= -1
            self.ydist *= -1
        if self.x <= 640 and self.y <= 360: # II quarter 
            pass
        if self.x <= 640 and self.y >= 360: # III quarter 
            self.xdist *= -1

def getAngleToMouse():
    x,y = pygame.mouse.get_pos()
    dist = math.sqrt((640-x)**2 + (360-y)**2) #distance from mouse pos to centre of ship
    ydist = abs(640-x) #distance from pos mouse to y axis (ship)
    xdist = abs(360-y) #same but for x

    angle = 0
    sin = ydist/dist
    if x >= 640 and y <= 360: # I quarter
        angle = math.degrees(math.asin(sin))
    elif x >= 640 and y >= 360: # IV quarter
        angle = 90 + (90 - math.degrees(math.asin(sin)))
    elif x <= 640 and y <= 360: # II quarter
        angle = 360 - math.degrees(math.asin(sin))
    elif x <= 640 and y >= 360: # III quarter
        angle = 180 + math.degrees(math.asin(sin))
    return -angle

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))

bgc_surf = pygame.image.load('background.png').convert_alpha()

ship_surf = pygame.image.load('ships/ship.png').convert()
ship_rect = ship_surf.get_rect(center = (640,360))
ship_surf.set_colorkey((0,0,0))

score_font = pygame.font.SysFont('verdana',50)

bulletList = []
oponentList = []
frames=0
points=0
while True:
    frames += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and ship_rect.collidepoint(pygame.mouse.get_pos())==False:
            bullet_surf = pygame.image.load('bullet.png').convert_alpha()
            bullet_rect = bullet_surf.get_rect(center = (640,360))

            x,y = pygame.mouse.get_pos()
            bullet = Bullet(x,y,bullet_rect,bullet_surf)
            bulletList.append(bullet)
            
    #background
    screen.blit(bgc_surf,(0,0))
    
    #bullets
    for bullet in bulletList:
        if bullet.alive:
            bullet.rect.x += bullet.y
            bullet.rect.y += bullet.x
            screen.blit(bullet.surf,bullet.rect)

    #oponets
    if frames % 60 == 0: #every 1 sec create oponent
        oponent = Oponent()
        oponentList.append(oponent)

    for oponent in oponentList:
        if oponent.alive:
            if frames % 2:
                oponent.rect.x += oponent.ydist
                oponent.rect.y += oponent.xdist
            screen.blit(oponent.surf,oponent.rect)

    #collide bullet with oponent
    for oponent in oponentList:
        for bullet in bulletList:
            if bullet.rect.colliderect(oponent.rect):
                oponent.alive = False
                bullet.alive = False
                points += 1

    #collide oponent with ship
    for oponent in oponentList:
        if oponent.alive:
            if oponent.rect.colliderect(ship_rect):

                time.sleep(1)
                frames=0
                points = 0
                bulletList = []
                oponentList = []
    
    #deletin bullet and oponent from Main list
    bulletListF = []
    oponentListF = []
    for oponent in oponentList:
        if oponent.alive:
            oponentListF.append(oponent)
    for bullet in bulletList:
        if bullet.alive:
            bulletListF.append(bullet)
    bulletList = bulletListF.copy()
    oponentList = oponentListF.copy()
    
    #ship
    ship_surf_copy = pygame.transform.rotate(ship_surf,getAngleToMouse())
    screen.blit(ship_surf_copy, (640 - int(ship_surf_copy.get_width() / 2),360 - int(ship_surf_copy.get_height() / 2)))

    #score rendering
    screen.blit(score_font.render(str(points),True,(50,50,50)), (635,50))
    
    #update sesction
    pygame.display.update()
    clock.tick(60)
