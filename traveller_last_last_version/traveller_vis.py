import pygame as pg
screen = pg.display.set_mode((1200, 1000))
screen.fill((255,255,255))
import math as m
def download():
    arrow_surf = pg.image.load('arrow.bmp')
    arrow_surf.set_colorkey((255, 255, 255))
    arrow_surf = pg.transform.scale(arrow_surf, (30,10))
    bow_surf = pg.image.load('bow.bmp')
    bow_surf.set_colorkey((255, 255, 255))
    bow_surf = pg.transform.scale(bow_surf, (25,50))
    hero1_surf = pg.image.load('hero1.png')
    hero2_surf = pg.image.load('hero2.png')
    hero1_surf.set_colorkey((255, 255, 255))
    hero1_surf = pg.transform.scale(hero1_surf, (50,50))
    hero2_surf.set_colorkey((255, 255, 255))
    hero2_surf = pg.transform.scale(hero2_surf, (50,50))
    enemy_surf = pg.image.load('enemy.png')
    enemy_surf.set_colorkey((255, 255, 255))
    enemy_surf = pg.transform.scale(enemy_surf, (50,50))
    corpse_surf = pg.image.load('corpse.png')
    corpse_surf.set_colorkey((255, 255, 255))
    corpse_surf = pg.transform.scale(corpse_surf, (50,50))
    sword_surf = pg.image.load('sword.bmp')
    sword_surf.set_colorkey((255, 255, 255))
    sword_surf = pg.transform.scale(sword_surf, (20,50))
    return((arrow_surf,hero1_surf,hero2_surf,enemy_surf,bow_surf,sword_surf,corpse_surf))
def arrows_vis(arrows,arrow_surf):
    for i in range(len(arrows)):
        if arrows[i].orientation == 'right':
            screen.blit(arrow_surf, (arrows[i].x-25,arrows[i].y))
        if arrows[i].orientation == 'left':
            screen.blit(pg.transform.flip(arrow_surf, True, False), (arrows[i].x-5,arrows[i].y))
        if arrows[i].orientation == 'top':
            screen.blit(pg.transform.rotate(arrow_surf, 90), (arrows[i].x-5,arrows[i].y-5))
        if arrows[i].orientation == 'bot':
            screen.blit(pg.transform.flip(pg.transform.rotate(arrow_surf, 90), False, True), (arrows[i].x-5,arrows[i].y-25))
def units_vis(units,corpses,hero1_surf,hero2_surf,enemy_surf, bow_surf, sword_surf,corpse_surf):
    if units[0].orientation == 'right':
        screen.blit(hero1_surf, (units[0].x,units[0].y))
        if units[0].weapon =='bow':
            screen.blit(bow_surf, (units[0].x+units[0].width-20,units[0].y))
        if units[0].weapon =='sword':
            screen.blit(pg.transform.rotate(sword_surf, m.acos((units[0].sword.y1-units[0].sword.y0)/units[0].sword.l)*180/3.14+180), (units[0].sword.x0-15,(units[0].sword.y0+units[0].sword.y1-units[0].sword.l)/2-5))
    if units[0].orientation == 'left':
        screen.blit(pg.transform.flip(hero1_surf, True, False), (units[0].x,units[0].y))
        if units[0].weapon =='bow':
            screen.blit(pg.transform.flip(bow_surf, True, False), (units[0].x-5,units[0].y))
    if units[0].orientation == 'bot':
        screen.blit(hero2_surf, (units[0].x,units[0].y))
        if units[0].weapon =='bow':
            screen.blit(pg.transform.flip(pg.transform.rotate(bow_surf, 90),False, True), (units[0].x,units[0].y+units[0].height-20))
    if units[0].orientation == 'top':
        screen.blit(pg.transform.flip(hero2_surf, False, True), (units[0].x,units[0].y))
        if units[0].weapon =='bow':
            screen.blit(pg.transform.rotate(bow_surf, 90), (units[0].x,units[0].y-5))
    for i in range(1,len(units)):
        screen.blit(enemy_surf, (units[i].x,units[i].y))
    for i in range(len(corpses)):
        screen.blit(corpse_surf, (corpses[i].x,corpses[i].y))
 
