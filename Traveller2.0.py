import pygame
import math as m
from pygame.draw import circle
from pygame.draw import polygon
from pygame.draw import rect
from pygame.draw import line
from pygame.draw import arc
from random import randint
import math as m
import pygame.freetype

pygame.init()

FPS = 60
screen_height = 1200
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
tick = 0

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
swords = []
bows = []
arrows = []
units = []
walls = []
enemies = []


class Sword:
    def __init__(self, x0, y0, x1, y1, l, phi, sharp, owner):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.l = l
        self.phi = phi
        self.sharp = sharp
        self.owner = owner

    def strike(self):
        self.phi = 5 * m.pi / 12
        self.sharp = 1


class Bow:
    def __init__(self, w, h, phi, tension, owner):
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
                arrows.append(
                    Arrow(self.owner.x + self.owner.width + self.w / 2 + 20, self.owner.y + self.owner.height / 2,
                          'right', self.tension / 3 + 10))
                self.tension = 0
            elif self.owner.orientation == 'left':
                arrows.append(Arrow(self.owner.x - self.w / 2 - 20, self.owner.y + self.owner.height / 2, 'left',
                                    -self.tension / 3 - 10))
                self.tension = 0
            elif self.owner.orientation == 'top':
                arrows.append(Arrow(self.owner.x + self.owner.width / 2, self.owner.y - self.w / 2 - 20, 'top',
                                    -self.tension / 3 - 10))
                self.tension = 0
            elif self.owner.orientation == 'bot':
                arrows.append(
                    Arrow(self.owner.x + self.owner.width / 2, self.owner.y + self.owner.height + self.w / 2, 'bot',
                          self.tension / 3 + 10))
                self.tension = 0


class Arrow:
    def __init__(self, x, y, orientation, speed):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.speed = speed

    def fly(self):
        if self.orientation == 'right':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x - 20, self.y), 3)
            self.x = self.x + self.speed
        elif self.orientation == 'left':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x + 20, self.y), 3)
            self.x = self.x + self.speed
        elif self.orientation == 'top':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y + 20), 3)
            self.y = self.y + self.speed
        elif self.orientation == 'bot':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y - 20), 3)
            self.y = self.y + self.speed


class Wall:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def stay(self):
        rect(screen, 'grey', (self.x, self.y, self.w, self.h))

    def collision(self, arrows, units):
        for j in range(len(arrows)):
            if arrows[j].x < self.x + self.w and arrows[j].y < self.y + self.h and arrows[j].y > self.y and arrows[
                j].orientation == 'left':
                arrows[j].x = self.x + self.w
                arrows[j].speed = 0
            if arrows[j].x > self.x and arrows[j].y < self.y + self.h and arrows[j].y > self.y and arrows[
                j].orientation == 'right':
                arrows[j].x = self.x
                arrows[j].speed = 0
            if arrows[j].y < self.y + self.w and arrows[j].x < self.x + self.w and arrows[j].x > self.x and arrows[
                j].orientation == 'top':
                arrows[j].y = self.y + self.w
                arrows[j].speed = 0
            if arrows[j].y > self.y and arrows[j].x < self.x + self.w and arrows[j].x > self.x and arrows[
                j].orientation == 'bot':
                arrows[j].y = self.y
                arrows[j].speed = 0
        for k in range(len(units)):
            k_cor = (units[k].x, units[k].x + units[k].width, units[k].y , units[k].y + units[k].height)
            w_cor = (self.x, self.x + self.w, self.y , self.y + self.h)
            if k_cor[0] < w_cor[1] and k_cor[1] > w_cor[1] and not (k_cor[3] < w_cor[2] or k_cor[2] > w_cor[3]):
                units[k].x = self.x + self.w+1
            if k_cor[1] > w_cor[0] and k_cor[0] < w_cor[0] and not (k_cor[3] < w_cor[2] or k_cor[2] > w_cor[3]):
                units[k].x = self.x - units[k].width-1
            if k_cor[2] < w_cor[3] and k_cor[3] > w_cor[3] and not (k_cor[1] < w_cor[0] or k_cor[0] > w_cor[1]):
                units[k].y = self.y + self.h+1
            if k_cor[3] > w_cor[2] and k_cor[2] < w_cor[2] and not (k_cor[1] < w_cor[0] or k_cor[0] > w_cor[1]):
                units[k].y = self.y - units[k].height-1
        '''for k in range(len(units)):
            if units[k].x + units[k].width > self.x and units[k].x < self.x + self.w and units[
                k].y < self.y + self.h and units[k].y + units[k].height > self.y and units[k].orientation == 'right':
                units[k].x = self.x - units[k].width
            if units[k].x + units[k].width > self.x and units[k].x < self.x + self.w and units[
                k].y < self.y + self.h and units[k].y + units[k].height > self.y and units[k].orientation == 'left':
                units[k].x = self.x + self.w
            if units[k].x + units[k].width > self.x and units[k].x < self.x + self.w and units[
                k].y < self.y + self.h and units[k].y + units[k].height > self.y and units[k].orientation == 'bot':
                units[k].y = self.y - units[k].height
            if units[k].x + units[k].width > self.x and units[k].x < self.x + self.w and units[
                k].y < self.y + self.h and units[k].y + units[k].height > self.y and units[k].orientation == 'top':
                units[k].y = self.y + self.h
'''

class Unit:
    def __init__(self, x, y, width, height, Vx, Vy, dV, orientation, hp, weapon, sword, bow, buttons):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Vx = Vx
        self.Vy = Vy
        self.dV = dV
        self.orientation = orientation
        self.hp = hp
        self.weapon = weapon
        self.sword = sword
        self.bow = bow
        self.buttons = buttons

    def stay(self):

        rect(screen, 'grey', (self.x, self.y, self.width, self.height))
        rect(screen, 'green',
             (self.x + 0.25 * self.width, self.y + self.height + 5, self.width * 0.5 * self.hp / 100 + 1, 10))
        rect(screen, 'red', (self.x + 0.25 * self.width + self.width * 0.5 * self.hp / 100, self.y + self.height + 5,
                             self.width * 0.5 * (100 - self.hp) / 100 + 1, 10))
        if self.weapon == 'sword':
            self.hold_a_sword()
        if self.weapon == 'bow':
            self.hold_a_bow()

    def acquire(self, swords, bows):
        for i in range(len(swords)):
            if self == swords[i].owner:
                self.sword = swords[i]
        for i in range(len(bows)):
            if bows[i].owner == self:
                self.bow = bows[i]

    def change_direction(self, event, walls):
        '''
        передвигаем юнита
        '''
        if event.type == pygame.KEYDOWN:
            if event.unicode == str(self.buttons[0]):
                self.Vy -= self.dV
                for i in range(len(walls)):
                    if not (self.x + self.width > walls[i].x and self.x < walls[i].x + walls[i].w and self.y < walls[
                        i].y + walls[i].h and self.y + self.height > walls[i].y):
                        self.orientation = 'top'
            if event.unicode == str(self.buttons[1]):
                self.Vy += self.dV
                for i in range(len(walls)):
                    if not (self.x + self.width > walls[i].x and self.x < walls[i].x + walls[i].w and self.y < walls[
                        i].y + walls[i].h and self.y + self.height > walls[i].y):
                        self.orientation = 'bot'
            if event.unicode == str(self.buttons[2]):
                self.Vx -= self.dV
                for i in range(len(walls)):
                    if not (self.x + self.width > walls[i].x and self.x < walls[i].x + walls[i].w and self.y < walls[
                        i].y + walls[i].h and self.y + self.height > walls[i].y):
                        self.orientation = 'left'
            if event.unicode == str(self.buttons[3]):
                self.Vx += self.dV
                for i in range(len(walls)):
                    if not (self.x + self.width > walls[i].x and self.x < walls[i].x + walls[i].w and self.y < walls[
                        i].y + walls[i].h and self.y + self.height > walls[i].y):
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

    def move(self):
        if self.Vx == 0 or self.Vy == 0:
            self.x += self.Vx
            self.y += self.Vy
        else:
            self.Vx = self.Vx / m.sqrt(2)
            self.Vy = self.Vy / m.sqrt(2)
            self.x += self.Vx
            self.y += self.Vy
            self.Vx = self.Vx * m.sqrt(2)
            self.Vy = self.Vy * m.sqrt(2)
        if self.y < -self.height:
            self.y = screen_height - self.height
        if self.y > screen_height:
            self.y = 0
        if self.x < -self.width:
            self.x = screen_width - self.width
        if self.x > screen_width:
            self.x = 0

    def hold_a_sword(self):
        if self.orientation == 'right':
            self.sword.x0 = self.x + self.width
            self.sword.y0 = self.y + self.height / 2
            self.sword.x1 = self.x + self.width + self.sword.l * m.cos(self.sword.phi)
            self.sword.y1 = self.y + self.height / 2 + self.sword.l * m.sin(self.sword.phi)
        if self.orientation == 'left':
            self.sword.x0 = self.x
            self.sword.y0 = self.y + self.height / 2
            self.sword.x1 = self.x - self.sword.l * m.cos(self.sword.phi)
            self.sword.y1 = self.y + self.height / 2 - self.sword.l * m.sin(self.sword.phi)
        if self.orientation == 'top':
            self.sword.x0 = self.x + self.width / 2
            self.sword.y0 = self.y
            self.sword.x1 = self.width / 2 + self.x + self.sword.l * m.sin(self.sword.phi)
            self.sword.y1 = self.y - self.sword.l * m.cos(self.sword.phi)
        if self.orientation == 'bot':
            self.sword.x0 = self.x + self.width / 2
            self.sword.y0 = self.y + self.height
            self.sword.x1 = self.width / 2 + self.x - self.sword.l * m.sin(self.sword.phi)
            self.sword.y1 = self.y + self.height + self.sword.l * m.cos(self.sword.phi)
        line(screen, (0, 0, 0), (self.sword.x0, self.sword.y0),
             (self.sword.x1, self.sword.y1), 3)
        if self.sword.sharp == 1 or self.sword.phi < 5 * m.pi / 12:
            self.sword.phi -= m.pi / 30
        if self.sword.phi <= -5 * m.pi / 12:
            self.sword.sharp = 0
            self.sword.phi = 5 * m.pi / 12

    def hold_a_bow(self):
        if (self.bow.tension > 0) and self.bow.tension < 100:
            self.bow.tension += 2.5
        if self.orientation == 'right':
            arc(screen, (0, 0, 0), (
            self.x + self.width - self.bow.w / 2, self.y + self.height / 2 - self.bow.h / 2, self.bow.w, self.bow.h),
                -m.pi / 2, m.pi / 2, 3)
        if self.orientation == 'left':
            arc(screen, (0, 0, 0),
                (self.x - self.bow.w / 2, self.y + self.height / 2 - self.bow.h / 2, self.bow.w, self.bow.h), m.pi / 2,
                3 * m.pi / 2, 3)
        if self.orientation == 'top':
            arc(screen, (0, 0, 0),
                (self.x + self.width / 2 - self.bow.h / 2, self.y - self.bow.w / 2, self.bow.h, self.bow.w), 0, m.pi, 3)
        if self.orientation == 'bot':
            arc(screen, (0, 0, 0), (
            self.x + self.width / 2 - self.bow.h / 2, self.y + self.height - self.bow.w / 2, self.bow.h, self.bow.w),
                m.pi, 0, 3)
        rect(screen, 'yellow',
             (self.x + 0.25 * self.width, self.y + self.height + 20, self.width * 0.5 * self.bow.tension / 100 + 1, 10))
        rect(screen, 'grey', (
        self.x + 0.25 * self.width + self.width * 0.5 * self.bow.tension / 100, self.y + self.height + 20,
        self.width * 0.5 * (100 - self.bow.tension) / 100 + 1, 10))

    def change_weapon(self):
        if self.weapon == 'sword':
            self.weapon = 'bow'
        elif self.weapon == 'bow':
            self.weapon = 'sword'

    def damage(self, arrows, swords, units):
        for j in range(len(arrows) - 1, -1, -1):
            if arrows[j].x > self.x and arrows[j].x < self.x + self.width and arrows[j].y > self.y and arrows[
                j].y < self.y + self.height and arrows[j].speed != 0:
                self.hp -= abs(arrows[j].speed)
                arrows.remove(arrows[j])
        for k in range(len(swords)):
            if ((swords[k].x1 > self.x and swords[k].x1 < self.x + self.width and swords[k].y1 > self.y and swords[
                k].y1 < self.y + self.height) or
                ((swords[k].x1 + swords[k].x0) / 2 > self.x and (
                        swords[k].x1 + swords[k].x0) / 2 < self.x + self.width and (
                         swords[k].y1 + swords[k].y0) / 2 > self.y and (
                         swords[k].y1 + swords[k].y0) / 2 > self.y < self.y + self.height)) and self != swords[
                k].owner and swords[k].sharp == 1:
                self.hp -= 30
                swords[k].phi -= 0.1
                swords[k].sharp = 0
        if self.hp <= 0:
            units.remove(units[i])

class Enemy(Unit):
    ''' Класс врагов'''
    def stay(self):
        '''
        отрисовываем врага
        '''
        rect(screen,'red',(self.x,self.y,self.width,self.height))
        rect(screen,'green',(self.x+0.25*self.width,self.y+self.height+5,self.width*0.5*self.hp/100+1,10))
        rect(screen,'red',(self.x+0.25*self.width+self.width*0.5*self.hp/100,self.y+self.height+5,self.width*0.5*(100-self.hp)/100+1,10))
        if self.weapon == 'sword':
            self.hold_a_sword()
        if self.weapon == 'bow':
            self.hold_a_bow()
    def move(self):
        ''' Движение врага по горизонтали (потом добавлю другие возможности)'''
        if self.orientation == 'right':
            self.Vx = 3
            self.x += self.Vx
            if self.x >= 300:
                self.orientation = 'left'
        if self.orientation == 'left':
            self.Vx = 3
            self.x -= self.Vx
            if self.x <= 0:
                self.orientation = 'right'
    def hold_a_sword(self):
        '''Меч врага всегда в режиме убийства'''
        if self.orientation == 'right':
            self.sword.x0 = self.x+self.width
            self.sword.y0 = self.y+self.height/2
            self.sword.x1 = self.x+self.width+self.sword.l
            self.sword.y1 = self.y+self.height/2
        if self.orientation == 'left':
            self.sword.x0 = self.x
            self.sword.y0 = self.y+self.height/2
            self.sword.x1 = self.x-self.sword.l
            self.sword.y1 = self.y+self.height/2
        if self.orientation == 'top':
            self.sword.x0 = self.x+self.width/2
            self.sword.y0 = self.y
            self.sword.x1 = self.width/2+self.x
            self.sword.y1 = self.y-self.sword.l
        if self.orientation == 'bot':
            self.sword.x0= self.x+self.width/2
            self.sword.y0 = self.y+self.height
            self.sword.x1 = self.width/2+self.x
            self.sword.y1 = self.y+self.height+self.sword.l
        line(screen,(0,0,0),(self.sword.x0,self.sword.y0),
                (self.sword.x1, self.sword.y1),3)
        self.sword.sharp = 1
    def damage(self,arrows,swords,enemies):
        '''Получение урона врагом (урон выше, чем у игрока)'''
        for j in range(len(arrows)-1,-1,-1):
            if arrows[j].x > self.x and arrows[j].x < self.x+self.width and arrows[j].y>self.y and arrows[j].y<self.y+self.height:
                self.hp -= 10+abs(arrows[j].speed)
                arrows.remove(arrows[j])
        for k in range(len(swords)):
            if ((swords[k].x1 > self.x and swords[k].x1 < self.x+self.width and swords[k].y1>self.y and swords[k].y1<self.y+self.height) or
                ((swords[k].x1+swords[k].x0)/2 > self.x and (swords[k].x1+swords[k].x0)/2 < self.x+self.width and (swords[k].y1+swords[k].y0)/2>self.y and (swords[k].y1+swords[k].y0)/2>self.y<self.y+self.height)) and self != swords[k].owner and swords[k].sharp == 1:
                self.hp -= 30
                swords[k].phi -= 0.1
                swords[k].sharp = 0
        if self.hp<=0:
            enemies.remove(enemies[i])

pygame.display.update()
clock = pygame.time.Clock()
finished = False
enemies.append(Enemy(150, 150, 60, 50, 0, 0, 3, 'right', 60, 'sword', None, None, 0))
units.append(Unit(10, 300, 50, 40, 0, 0, 5, 'right', 75, 'sword', None, None, ('w', 's', 'a', 'd')))
units.append(Unit(300, 300, 50, 40, 0, 0, 10, 'right', 75, None, None, None, None))
swords.append(Sword(0, 0, 0, 0, 50, 5 * m.pi / 12, 0, units[0]))
bows.append(Bow(50, 25, 0, 0, units[0]))
swords.append(Sword(0,0,0,0,0.05,5*m.pi/12,0,enemies[0]))
walls.append(Wall(800, 600, 150, 300))
for i in range(len(enemies)):
    enemies[i].acquire(swords,bows)
for i in range(len(units)):
    units[i].acquire(swords, bows)
while not finished:
    clock.tick(FPS)
    for i in range(len(walls)):
        walls[i].stay()
        walls[i].collision(arrows, units)
    for i in range(len(enemies)-1,-1,-1):
        enemies[i].stay()
        enemies[i].move()
        enemies[i].damage(arrows,swords,enemies)
    for i in range(len(units) - 1, -1, -1):
        units[i].stay()
        units[i].move()
        units[i].damage(arrows, swords, units)
    for i in range(len(arrows)):
        arrows[i].fly()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            units[0].change_direction(event, walls)
        elif event.type == pygame.KEYUP:
            units[0].change_direction(event, walls)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if units[0].weapon == 'sword':
                swords[0].strike()
            if units[0].weapon == 'bow':
                bows[0].pull()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            units[0].change_weapon()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            bows[0].draw()
    pygame.display.update()
    screen.fill((255, 255, 255))
    tick = tick + 1
pygame.quit()
