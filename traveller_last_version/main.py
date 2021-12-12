import math as m
from random import randint

import numpy as np
import pygame.freetype
from pygame.draw import rect, line, arc, polygon

from traveller_input import *
from vis import *

pygame.init()
FPS = 30
tick = 0
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
arrows = []
units = []

'''
фоновая музыка
'''
pygame.mixer.init()
pygame.mixer.music.load('music/The Legend Of Zelda Theme Song.wav')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1, 0)


class Sword:
    """Класс меча:
    x0,y0 - координата начала
    x1, y1 - координаиа конца
    l - длина
    phi - угол поворота
    sharp - статус (происходит удар или нет)
    owner - герой (тот, кому принадлежит меч)"""

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
        '''удар'''
        self.phi = 5 * m.pi / 12
        self.sharp = 1


class Bow:
    """Класс меча:
    w - ширина лука
    h - высота лука
    tension - параметр заряженности лука
    owner - герой (тот, кому принадлежит лук)"""

    '''
    звук выстрела
    '''

    def boom():
        pygame.mixer.init()
        pygame.mixer.music.load(('music/pew.wav'))
        pygame.mixer.music.play()

    def __init__(self, w, h, phi, tension, owner):
        self.h = h
        self.w = w
        self.phi = phi
        self.tension = tension
        self.owner = owner

    def pull(self):
        """начать заряжать выстрел"""
        if self.owner.weapon == 'bow':
            self.tension = 0.1

    def draw(self):
        """выпустить стрелу"""
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
    '''Класс стрелы:
    x,y - координаты стрелы
    orientation - направление полета
    speed - скорость полета'''

    def __init__(self, x, y, orientation, speed):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.speed = speed

    def fly(self):
        '''осуществляет движение стрелы'''
        if self.orientation == 'right':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x - 20, self.y), 3)
            polygon(screen, (0, 0, 0), ([self.x + 5, self.y], [self.x, self.y + 5], [self.x, self.y - 5]))
            self.x = self.x + self.speed
        elif self.orientation == 'left':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x + 20, self.y), 3)
            polygon(screen, (0, 0, 0), ([self.x - 5, self.y], [self.x, self.y + 5], [self.x, self.y - 5]))
            self.x = self.x + self.speed
        elif self.orientation == 'top':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y + 20), 3)
            polygon(screen, (0, 0, 0), ([self.x, self.y - 5], [self.x - 5, self.y], [self.x + 5, self.y]))
            self.y = self.y + self.speed
        elif self.orientation == 'bot':
            line(screen, (0, 0, 0), (self.x, self.y), (self.x, self.y - 20), 3)
            polygon(screen, (0, 0, 0), ([self.x, self.y + 5], [self.x - 5, self.y], [self.x + 5, self.y]))
            self.y = self.y + self.speed


class Wall:
    '''Класс стен:
    x,y - координаты стены
    w - ширина стены
    h - высота стены'''
    '''
    дизайн стен
    '''
    walls_im = pygame.image.load("walls.jpg").convert()

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def stay(self):
        '''будет удалено'''
        rect(screen, (80, 80, 80), (self.x, self.y, self.w, self.h))

    def collision(self, arrows, units):
        '''проверка столкновения со стенами стрел'''
        for j in range(len(arrows)):
            if arrows[j].x < self.x + self.w and arrows[j].x > self.x and arrows[j].y < self.y + self.h and arrows[
                j].y > self.y:
                if arrows[j].orientation == 'left':
                    arrows[j].x = self.x + self.w
                    arrows[j].speed = 0
                if arrows[j].orientation == 'right':
                    arrows[j].x = self.x
                    arrows[j].speed = 0
                if arrows[j].orientation == 'top':
                    arrows[j].y = self.y + self.h
                    arrows[j].speed = 0
                if arrows[j].orientation == 'bot':
                    arrows[j].y = self.y
                    arrows[j].speed = 0


class Unit():
    '''Класс существ:
    x,y - координаты юнита
    width - ширина юнита
    height - ширина юнита
    Vx, Vy - текущие значения скорости по осям
    dV - скорость, которую герой получает при нажатии на кнопку
    orientation - направление взгляда юнита
    hp - здоровье юнита
    weapon - для главного героя оружие, которое он дердит в руках, для врагов статус преследования: 0 - не преследуют,
    1 - преследуют, так как герой подошел слишком близко, 2 - преследуют, так как в них попала стрела
    sword - объект класса Sword, меч героя
    bow - объект класса Bow, лук героя
    buttons - кнопки управления героем
    points - точки маршрута, которые патрулирует враг    
    '''

    def __init__(self, x, y, width, height, Vx, Vy, dV, orientation, hp, weapon, sword, bow, buttons, points):

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
        self.points = points

    def patrol(self, flag, timer):
        '''функция патрулирования врагом территории, позволяющая также ему преследовать героя,
            герою после получения урона дает неуязвимость на короткое время'''
        self.Vx = np.sign((self.points[self.points[0]][0] - self.x) // 10) * self.dV
        self.Vy = np.sign((self.points[self.points[0]][1] - self.y) // 10) * self.dV
        if self.Vx == 0 and self.Vy == 0:
            self.points[0] = self.points[0] % (len(self.points) - 1)
            self.points[0] += 1
        if self.x + self.width > units[0].x and self.x < units[0].x + units[0].width and self.y < units[0].y + units[
            0].height and self.y + self.height > units[0].y and flag == False:
            units[0].hp -= 70
            flag = True
            timer = tick
        if tick - timer == 50:
            timer = 0
            flag = False
        if self.weapon > 0:
            self.points = [1, (units[0].x, units[0].y)]
        if self.x + self.width > units[0].x - 200 and self.x < units[0].x + units[0].width + 200 and self.y < units[
            0].y + units[0].height + 200 and self.y + self.height > units[0].y - 200:
            self.weapon = 1
        if self.weapon == 1 and not (
                self.x + self.width > units[0].x - 350 and self.x < units[0].x + units[0].width + 350 and self.y <
                units[0].y + units[0].height + 350 and self.y + self.height > units[0].y - 350):
            self.weapon = 0
            self.points = units_data[self.buttons][6]
        return ((flag, timer))

    def stay(self):
        '''
        отрисовывает полоски здоровья, выполняет функции связанные с поддержкой меча и лука
        '''
        rect(screen, (0, 255, 0),
             (self.x + 0.25 * self.width, self.y + self.height + 5, self.width * 0.5 * self.hp / 100 + 1, 10))
        rect(screen, (250, 0, 0),
             (self.x + 0.25 * self.width + self.width * 0.5 * self.hp / 100, self.y + self.height + 5,
              self.width * 0.5 * (100 - self.hp) / 100, 10))
        if self.weapon == 'sword':
            self.hold_a_sword()
        if self.weapon == 'bow':
            self.hold_a_bow()

    def change_direction(self, event, walls):
        '''
        меняет скорость и направление юнита
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

    def move(self, walls):
        '''
        передвигает юнита, если нет столкновений со стенами
        '''
        motion_matrix = [-len(walls) + 1, -len(walls) + 1]
        for k in range(len(walls)):
            if self.Vx > 0 and not (
                    self.x + self.width + self.Vx > walls[k].x and self.x < walls[k].x + walls[k].w and self.y < walls[
                k].y + walls[k].h and self.y + self.height > walls[k].y):
                motion_matrix[0] += 1
            if self.Vx < 0 and not (
                    self.x + self.width > walls[k].x and self.x + self.Vx < walls[k].x + walls[k].w and self.y < walls[
                k].y + walls[k].h and self.y + self.height > walls[k].y):
                motion_matrix[0] += 1
            if self.Vy > 0 and not (
                    self.x + self.width > walls[k].x and self.x < walls[k].x + walls[k].w and self.y < walls[k].y +
                    walls[k].h and self.y + self.height + self.Vy > walls[k].y):
                motion_matrix[1] += 1
            if self.Vy < 0 and not (
                    self.x + self.width > walls[k].x and self.x < walls[k].x + walls[k].w and self.y + self.Vy < walls[
                k].y + walls[k].h and self.y + self.height > walls[k].y):
                motion_matrix[1] += 1
        if motion_matrix[0] > 0:
            self.x += self.Vx
        if motion_matrix[1] > 0:
            self.y += self.Vy
        if self.y < -self.height:
            self.y = screen_height - self.height
        if self.y > screen_height:
            self.y = 0
        if self.x < -self.width:
            self.x = screen_width - self.width
        if self.x > screen_width:
            self.x = 0

    def hold_a_sword(self):
        '''
        передвигает юните, если нет столкновений со стенами
        '''
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
        '''
        изменяет натяжение лука, отрисовывает полоску натяжения
        '''
        if (self.bow.tension > 0) and self.bow.tension < 100:
            self.bow.tension += 2.5
        if self.orientation == 'right':
            arc(screen, (0, 0, 0), (
                self.x + self.width - self.bow.w / 2, self.y + self.height / 2 - self.bow.h / 2, self.bow.w,
                self.bow.h),
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
                self.x + self.width / 2 - self.bow.h / 2, self.y + self.height - self.bow.w / 2, self.bow.h,
                self.bow.w),
                m.pi, 0, 3)
        rect(screen, 'yellow',
             (self.x + 0.25 * self.width, self.y + self.height + 20, self.width * 0.5 * self.bow.tension / 100 + 1, 10))
        rect(screen, 'grey', (
            self.x + 0.25 * self.width + self.width * 0.5 * self.bow.tension / 100, self.y + self.height + 20,
            self.width * 0.5 * (100 - self.bow.tension) / 100 + 1, 10))

    def change_weapon(self):
        '''
        меняет оружие героя
        '''
        if self.weapon == 'sword':
            self.weapon = 'bow'
        elif self.weapon == 'bow':
            self.weapon = 'sword'

    def damage(self, arrows, sword, units, i):
        '''
        получение всеми юнитами урона от стрел, меча и удаление их в случае смерти
        '''
        for j in range(len(arrows) - 1, -1, -1):
            if arrows[j].x > self.x and arrows[j].x < self.x + self.width and arrows[j].y > self.y and arrows[
                j].y < self.y + self.height and arrows[j].speed != 0:
                self.hp -= abs(arrows[j].speed)
                self.weapon = 2
                arrows.remove(arrows[j])
        if ((
                    sword.x1 > self.x and sword.x1 < self.x + self.width and sword.y1 > self.y and sword.y1 < self.y + self.height) or
            ((sword.x1 + sword.x0) / 2 > self.x and (sword.x1 + sword.x0) / 2 < self.x + self.width and (
                    sword.y1 + sword.y0) / 2 > self.y and (
                     sword.y1 + sword.y0) / 2 < self.y + self.height)) and self != sword.owner and sword.sharp == 1:
            self.hp -= 30
            sword.phi -= 0.1
            sword.sharp = 0
        if self.hp <= 0:
            units.remove(units[i])


def build_the_level(input_filename):
    '''
    создает уровней по информации из input
    '''
    walls = []
    units = []
    units.append(
        Unit(10, screen_height / 2, 30, 50, 0, 0, 5, 'right', 100, 'sword', None, None, ('w', 's', 'a', 'd'), None))
    sword = Sword(0, 0, 0, 0, 50, 5 * m.pi / 12, 0, units[0])
    bow = Bow(50, 25, 0, 0, units[0])
    units[0].sword = sword
    units[0].bow = bow
    (walls_data, units_data) = read_data_from_file(input_filename)
    for i in range(len(walls_data)):
        walls.append(Wall(walls_data[i][0], walls_data[i][1], walls_data[i][2], walls_data[i][3]))
    for i in range(len(units_data)):
        units.append(
            Unit(units_data[i][0], units_data[i][1], units_data[i][2], units_data[i][3], 0, 0, units_data[i][4],
                 'right', units_data[i][5], 0, None, None, i, units_data[i][6]))
    return ((walls, units, sword, bow, units_data))


def refresh(input_filename, walls, units, sword, bow, arrows, units_data):
    '''
    осуществляет переход на новый уровень
    '''
    if len(units) == 1 and units[0].x > screen_width - units[0].width - 1:
        arrows = []
        Vx = units[0].Vx
        Vy = units[0].Vy
        (walls, units, sword, bow, units_data) = build_the_level(input_filename)
        units[0].Vx = Vx
        units[0].Vy = Vy
    return ((walls, units, sword, bow, arrows, units_data))


def sustain_walls(walls):
    '''
    поддерживает существование стен
    '''
    for i in range(len(walls)):
        walls[i].stay()
        walls[i].collision(arrows, units)


def sustain_units(units, walls, arrows, sword, flag, timer):
    '''
    поддерживает существование юнитов
    '''
    for i in range(len(units) - 1, -1, -1):
        units[i].stay()
        units[i].move(walls)
        units[i].damage(arrows, sword, units, i)
    for i in range(1, len(units), 1):
        (flag, timer) = units[i].patrol(flag, timer)
    return ((flag, timer))


def sustain_arrows(arrows):
    '''
    поддерживает существование стрел
    '''
    for i in range(len(arrows)):
        arrows[i].fly()


def sustain_all(units, walls, arrows, sword, flag, timer):
    '''
    поддерживает существование всех объектов уровня
    '''
    sustain_walls(walls)
    (flag, timer) = sustain_units(units, walls, arrows, sword, flag, timer)
    sustain_arrows(arrows)
    return ((flag, timer))


'''
дизайн фона
'''
bg_im = pygame.image.load("backgroundtraveller.png").convert()

pygame.display.update()
clock = pygame.time.Clock()
finished = False
(walls, units, sword, bow, units_data) = build_the_level("level_" + str(randint(6, 6)) + ".txt")
while not finished:
    clock.tick(FPS)
    (flag, timer) = sustain_all(units, walls, arrows, sword, flag, timer)
    if units[0].hp <= 0:
        finished = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            units[0].change_direction(event, walls)
        elif event.type == pygame.KEYUP:
            units[0].change_direction(event, walls)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if units[0].weapon == 'sword':
                sword.strike()
            if units[0].weapon == 'bow':
                bow.pull()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            units[0].change_weapon()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            bow.draw()
    (walls, units, sword, bow, arrows, units_data) = refresh("level_" + str(randint(1, 2)) + ".txt", walls, units,
                                                             sword, bow, arrows, units_data)
    pygame.display.update()
    # screen.fill((255, 255, 255))
    screen.blit(bg_im, [0, 0])
    vis_unit(units)
    vis_evil_create(units)
    vis_evil(units, tick)
    tick = tick + 1
pygame.quit()
