import pygame
import math as m
from pygame.draw import circle
from pygame.draw import polygon
from pygame.draw import rect
from pygame.draw import line
from pygame.draw import arc
from random import randint
import math as m
import numpy as np
from traveller_input import *
from traveller_vis import *
pygame.init()

FPS = 60
screen_height=1000
screen_width=1200
screen = pygame.display.set_mode((screen_width, screen_height))
tick=0
flag = False
timer = 0

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
arrows=[]
units=[]
corpses=[]
class Sword:
    def __init__(self,x0,y0,x1,y1,l,phi,sharp,owner):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.l = l
        self.phi = phi
        self.sharp = sharp
        self.owner = owner
    def strike(self):
        self.phi = 5*m.pi/12
        self.sharp = 1
class Bow:
    def __init__(self,w,h,phi,tension,owner):
        self.h = h
        self.w = w
        self.phi = phi
        self.tension = tension
        self.owner = owner
    def pull(self):
        if self.owner.weapon == 'bow':
            self.tension = 0.1
    def draw(self):
        if self.owner.weapon == 'bow':
            if self.owner.orientation == 'right':
                arrows.append(Arrow(self.owner.x+self.owner.width+self.w/2+30,self.owner.y+self.owner.height/2,'right',self.tension/3+10))
                self.tension = 0
            elif self.owner.orientation == 'left':
                arrows.append(Arrow(self.owner.x-self.w/2-30,self.owner.y+self.owner.height/2,'left',-self.tension/3-10))
                self.tension = 0
            elif self.owner.orientation == 'top':
                arrows.append(Arrow(self.owner.x+self.owner.width/2,self.owner.y-self.w/2-30,'top',-self.tension/3-10))
                self.tension = 0
            elif self.owner.orientation == 'bot':
                arrows.append(Arrow(self.owner.x+self.owner.width/2,self.owner.y+self.owner.height+self.w/2,'bot',self.tension/3+10))
                self.tension = 0
class Arrow:
    def __init__(self,x,y,orientation,speed):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.speed = speed
    def fly(self):
        if self.orientation == 'right':
            self.x=self.x+self.speed
        elif self.orientation == 'left':
            self.x=self.x+self.speed
        elif self.orientation == 'top':
            self.y=self.y+self.speed
        elif self.orientation == 'bot':
            self.y=self.y+self.speed        
class Wall:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def stay (self):
        rect(screen,'grey',(self.x,self.y,self.w,self.h))
    def collision(self,arrows,units):
        for j in range(len(arrows)):
            if  arrows[j].x < self.x+self.w and arrows[j].x > self.x and arrows[j].y < self.y+self.h and arrows[j].y > self.y:
                if arrows[j].orientation == 'left':
                    arrows[j].x = self.x+self.w
                    arrows[j].speed =0
                if arrows[j].orientation == 'right':
                    arrows[j].x = self.x
                    arrows[j].speed =0
                if arrows[j].orientation == 'top':
                    arrows[j].y = self.y +self.h
                    arrows[j].speed =0
                if  arrows[j].orientation == 'bot':
                    arrows[j].y = self.y
                    arrows[j].speed = 0
            
class Corpse:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height

class Unit:
    def __init__(self,x,y,width,height,Vx,Vy,dV,orientation,hp,weapon,sword,bow,buttons,points):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.Vx=Vx
        self.Vy=Vy
        self.dV=dV
        self.orientation = orientation
        self.hp=hp
        self.weapon = weapon
        self.sword = sword
        self.bow = bow
        self.buttons = buttons
        self.points = points
    def patrol(self,flag,timer):
        self.Vy=np.sign((self.points[self.points[0]][1]-self.y)//10)*self.dV
        if self.Vy >0:
            self.orientation = 'bot'
        if self.Vy <0:
            self.orientation = 'top'
        self.Vx=np.sign((self.points[self.points[0]][0]-self.x)//10)*self.dV
        if self.Vx >0:
            self.orientation = 'bot'
        if self.Vx <0:
            self.orientation = 'top'
        if self.Vx ==0 and self.Vy == 0:
            self.points[0] = self.points[0] % (len(self.points)-1)
            self.points[0] += 1
        if self.x +self.width > units[0].x and self.x< units[0].x + units[0].width and self.y < units[0].y+units[0].height and self.y+self.height > units[0].y and flag == False:
            units[0].hp -= 70
            flag = True
            timer = tick
        if tick - timer == 50:
            timer = 0
            flag = False
        if self.weapon > 0:
            self.points = [1,(units[0].x,units[0].y)]
        if self.x +self.width > units[0].x -200 and self.x< units[0].x + units[0].width +200 and self.y < units[0].y+units[0].height +200 and self.y+self.height > units[0].y - 200:
            self.weapon = 1
        if self.weapon == 1 and not (self.x +self.width > units[0].x -350 and self.x< units[0].x + units[0].width +350 and self.y < units[0].y+units[0].height +350 and self.y+self.height > units[0].y - 350):
            self.weapon = 0
            self.points = units_data[self.buttons][6]
        return((flag,timer))
    def stay(self):
        '''
        отрисовываем танк
        '''
        rect(screen,'green',(self.x+0.25*self.width,self.y+self.height+5,self.width*0.5*self.hp/100+1,10))
        rect(screen,'red',(self.x+0.25*self.width+self.width*0.5*self.hp/100,self.y+self.height+5,self.width*0.5*(100-self.hp)/100,10))
        if self.weapon == 'sword':
            self.hold_a_sword()
        if self.weapon == 'bow':
            self.hold_a_bow()
    def change_direction(self,event,walls):
        '''
        передвигаем юнита
        '''
        if event.type == pygame.KEYDOWN:
            if event.unicode == str(self.buttons[0]):
                self.Vy -= self.dV
                self.orientation = 'top'
            if event.unicode == str(self.buttons[1]):
                self.Vy += self.dV
                self.orientation = 'bot'
            if event.unicode == str(self.buttons[2]):
                self.Vx -= self.dV
                self.orientation = 'left' 
            if event.unicode == str(self.buttons[3]):
                self.Vx += self.dV
                self.orientation = 'right'
        if event.type == pygame.KEYUP:
            if event.unicode == str(self.buttons[2]):
                self.Vx += self.dV
            if event.unicode == str(self.buttons[3]):
                self.Vx -= self.dV
            if event.unicode == str(self.buttons[0]):
                 self.Vy += self.dV
            if event.unicode == str(self.buttons[1]):
                 self.Vy -= self.dV
                    
    def move(self,walls):
        motion_matrix = [-len(walls)+1,-len(walls)+1]
        for k in range(len(walls)):
            if self.Vx>0 and not (self.x +self.width + self.Vx> walls[k].x and self.x< walls[k].x +walls[k].w and self.y < walls[k].y+walls[k].h and self.y+self.height > walls[k].y):
                motion_matrix[0] += 1
            if self.Vx<0 and not (self.x +self.width > walls[k].x and self.x+ self.Vx< walls[k].x +walls[k].w and self.y < walls[k].y+walls[k].h and self.y+self.height > walls[k].y):
                motion_matrix[0] += 1
            if self.Vy>0 and not (self.x +self.width> walls[k].x and self.x< walls[k].x +walls[k].w and self.y < walls[k].y+walls[k].h and self.y+self.height+self.Vy > walls[k].y):
                motion_matrix[1] += 1
            if self.Vy<0 and not (self.x +self.width > walls[k].x and self.x < walls[k].x +walls[k].w and self.y +self.Vy < walls[k].y+walls[k].h and self.y+self.height > walls[k].y):
                motion_matrix[1] += 1
        if motion_matrix[0]>0:
            self.x += self.Vx
        if motion_matrix[1]>0:
            self.y += self.Vy 
        if self.y<-self.height:
            self.y=screen_height-self.height
        if self.y>screen_height:
            self.y=0
        if self.x<-self.width:
            self.x=screen_width-self.width
        if self.x>screen_width:
            self.x=0
    def hold_a_sword(self):
        if self.orientation == 'right': 
            self.sword.x0 = self.x+self.width
            self.sword.y0 = self.y+self.height/2
            self.sword.x1 = self.x+self.width+self.sword.l*m.cos(self.sword.phi)
            self.sword.y1 = self.y+self.height/2+self.sword.l*m.sin(self.sword.phi)
        if self.orientation == 'left': 
            self.sword.x0 = self.x
            self.sword.y0 = self.y+self.height/2
            self.sword.x1 = self.x-self.sword.l*m.cos(self.sword.phi)
            self.sword.y1 = self.y+self.height/2-self.sword.l*m.sin(self.sword.phi)
        if self.orientation == 'top':
            self.sword.x0 = self.x+self.width/2
            self.sword.y0 = self.y
            self.sword.x1 = self.width/2+self.x+self.sword.l*m.sin(self.sword.phi)
            self.sword.y1 = self.y-self.sword.l*m.cos(self.sword.phi)
        if self.orientation == 'bot':
            self.sword.x0= self.x+self.width/2
            self.sword.y0 = self.y+self.height
            self.sword.x1 = self.width/2+self.x-self.sword.l*m.sin(self.sword.phi)
            self.sword.y1 = self.y+self.height+self.sword.l*m.cos(self.sword.phi)
        #line(screen,(0,0,0),(self.sword.x0,self.sword.y0),
                #(self.sword.x1, self.sword.y1),3)
        if self.sword.sharp == 1 or self.sword.phi < 5*m.pi/12:
            self.sword.phi -= m.pi/30
        if self.sword.phi <= -5*m.pi/12:
            self.sword.sharp = 0
            self.sword.phi = 5*m.pi/12
    def hold_a_bow(self):
        if (self.bow.tension > 0) and self.bow.tension < 100:
            self.bow.tension += 2.5
        rect(screen,'yellow',(self.x+0.25*self.width,self.y+self.height+20,self.width*0.5*self.bow.tension/100+1,10))
        rect(screen,'grey',(self.x+0.25*self.width+self.width*0.5*self.bow.tension/100,self.y+self.height+20,self.width*0.5*(100-self.bow.tension)/100+1,10))
        
    def change_weapon(self):
        if self.weapon == 'sword':
           self.weapon = 'bow'
        elif self.weapon == 'bow':
           self.weapon = 'sword'
    def damage(self,arrows,sword,units, corpses, i):        
        for j in range(len(arrows)-1,-1,-1):
            if arrows[j].x > self.x and arrows[j].x < self.x+self.width and arrows[j].y>self.y and arrows[j].y<self.y+self.height and arrows[j].speed != 0:
                self.hp -= abs(arrows[j].speed)
                self.weapon = 2
                arrows.remove(arrows[j])
        if ((sword.x1 > self.x and sword.x1 < self.x+self.width and sword.y1>self.y and sword.y1<self.y+self.height) or
            ((sword.x1+sword.x0)/2 > self.x and (sword.x1+sword.x0)/2 < self.x+self.width and (sword.y1+sword.y0)/2>self.y and (sword.y1+sword.y0)/2<self.y+self.height)) and self != sword.owner and sword.sharp == 1:
            self.hp -= 30
            sword.phi -= 0.1
            sword.sharp = 0
        if self.hp<=0:
            corpses.append(Corpse(units[i].x,units[i].y,units[i].width,units[i].height))
            units.remove(units[i])

def build_the_level(input_filename):
    walls=[]
    units=[]
    units.append(Unit(10,screen_height/2,50,50,0,0,5,'right',100,'sword',None,None,('w','s','a','d'),None))
    sword = Sword(0,0,0,0,50,5*m.pi/12,0,units[0])
    bow = Bow(50,25,0,0,units[0])
    units[0].sword = sword
    units[0].bow = bow
    (walls_data,units_data) = read_data_from_file(input_filename)
    for i in range (len(walls_data)):
        walls.append(Wall(walls_data[i][0],walls_data[i][1],walls_data[i][2],walls_data[i][3]))
    for i in range (len(units_data)):
        units.append(Unit(units_data[i][0],units_data[i][1],units_data[i][2],units_data[i][3],0,0,units_data[i][4],'right',units_data[i][5],0,None,None,i,units_data[i][6]))
    return((walls,units,sword,bow,units_data))
def refresh(input_filename,walls,units,sword,bow,arrows,units_data):
    if len(units) == 1 and units[0].x>screen_width-units[0].width-1:
        arrows=[]
        Vx=units[0].Vx
        Vy=units[0].Vy
        (walls,units,sword,bow,units_data) = build_the_level(input_filename)
        units[0].Vx=Vx
        units[0].Vy=Vy
    return((walls,units,sword,bow,arrows,units_data))

def sustain_walls(walls):
    for i in range(len(walls)):
        walls[i].stay()
        walls[i].collision(arrows,units)
def sustain_units(units,walls,arrows,sword,flag,timer,corpses):
    for i in range(len(units)-1,-1,-1):
        units[i].stay()
        units[i].move(walls)
        units[i].damage(arrows,sword,units, corpses, i)
    for i in range(1,len(units),1):
        (flag,timer)=units[i].patrol(flag,timer)
    return((flag,timer))
def sustain_arrows(arrows):
    for i in range (len(arrows)):
        arrows[i].fly()
def sustain_all(units,walls,arrows,sword,flag,timer,corpses):
    sustain_walls(walls)
    (flag,timer) = sustain_units(units,walls,arrows,sword,flag,timer,corpses)
    sustain_arrows(arrows)
    return((flag,timer))

pygame.display.update()
clock = pygame.time.Clock()
finished = False
(walls,units,sword,bow,units_data) = build_the_level("level_"+str(randint(1,2))+".txt")
(arrow_surf,hero1_surf,hero2_surf,enemy_surf,bow_surf,sword_surf,corpse_surf)=download()
while not finished:
    clock.tick(FPS)
    (flag,timer) = sustain_all(units,walls,arrows,sword,flag,timer,corpses)
    arrows_vis(arrows,arrow_surf)
    units_vis(units,corpses,hero1_surf,hero2_surf,enemy_surf,bow_surf,sword_surf,corpse_surf)
    if units[0].hp <=0:
        finished = True   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            units[0].change_direction(event,walls)
        elif event.type == pygame.KEYUP:
            units[0].change_direction(event,walls)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if units[0].weapon == 'sword':
                sword.strike()
            if units[0].weapon == 'bow':
                bow.pull()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            units[0].change_weapon()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            bow.draw()
    (walls,units,sword,bow,arrows,units_data) = refresh("level_"+str(randint(1,2))+".txt",walls,units,sword,bow,arrows,units_data)        
    pygame.display.update()
    screen.fill((255,255,255))
    tick=tick+1
pygame.quit()

