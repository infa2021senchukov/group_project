import pygame

screen_height = 1000
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))

'''
дизайн фона
'''
bg_im = pygame.image.load("backgroundtraveller.png").convert()


#Изображения для анимации героев загружатся в программу в виде переменных

b_1 = pygame.image.load("hero/b_1.png").convert()
b_2 = pygame.image.load("hero/b_2.png").convert()
b_3 = pygame.image.load("hero/b_3.png").convert()
b_4 = pygame.image.load("hero/b_4.png").convert()
b_5 = pygame.image.load("hero/b_5.png").convert()
b_6 = pygame.image.load("hero/b_6.png").convert()
b_7 = pygame.image.load("hero/b_7.png").convert()
b_8 = pygame.image.load("hero/b_8.png").convert()
b_9 = pygame.image.load("hero/b_9.png").convert()

f_1 = pygame.image.load("hero/f_1.png").convert()
f_2 = pygame.image.load("hero/f_2.png").convert()
f_3 = pygame.image.load("hero/f_3.png").convert()
f_4 = pygame.image.load("hero/f_4.png").convert()
f_5 = pygame.image.load("hero/f_5.png").convert()
f_6 = pygame.image.load("hero/f_6.png").convert()
f_7 = pygame.image.load("hero/f_7.png").convert()
f_8 = pygame.image.load("hero/f_8.png").convert()
f_9 = pygame.image.load("hero/f_9.png").convert()

l_1 = pygame.image.load("hero/l_1.png").convert()
l_2 = pygame.image.load("hero/l_2.png").convert()
l_3 = pygame.image.load("hero/l_3.png").convert()
l_4 = pygame.image.load("hero/l_4.png").convert()
l_5 = pygame.image.load("hero/l_5.png").convert()
l_6 = pygame.image.load("hero/l_6.png").convert()
l_7 = pygame.image.load("hero/l_7.png").convert()
l_8 = pygame.image.load("hero/l_8.png").convert()
l_9 = pygame.image.load("hero/l_9.png").convert()

r_1 = pygame.image.load("hero/r_1.png").convert()
r_2 = pygame.image.load("hero/r_2.png").convert()
r_3 = pygame.image.load("hero/r_3.png").convert()
r_4 = pygame.image.load("hero/r_4.png").convert()
r_5 = pygame.image.load("hero/r_5.png").convert()
r_6 = pygame.image.load("hero/r_6.png").convert()
r_7 = pygame.image.load("hero/r_7.png").convert()
r_8 = pygame.image.load("hero/r_8.png").convert()
r_9 = pygame.image.load("hero/r_9.png").convert()

mb_1 = pygame.image.load("evil/mb_1.png").convert()
mb_2 = pygame.image.load("evil/mb_2.png").convert()
mb_3 = pygame.image.load("evil/mb_3.png").convert()

mf_1 = pygame.image.load("evil/mf_1.png").convert()
mf_2 = pygame.image.load("evil/mf_2.png").convert()
mf_3 = pygame.image.load("evil/mf_3.png").convert()

ml_1 = pygame.image.load("evil/ml_1.png").convert()
ml_2 = pygame.image.load("evil/ml_2.png").convert()
ml_3 = pygame.image.load("evil/ml_3.png").convert()

mr_1 = pygame.image.load("evil/mr_1.png").convert()
mr_2 = pygame.image.load("evil/mr_2.png").convert()
mr_3 = pygame.image.load("evil/mr_3.png").convert()

#Счетчики для пермещений героя

back_counter = 0
front_counter = 0
left_counter = 0
right_counter = 0

#Стартовые изображения героев

hero_image = r_5
evil_image = mf_1

#Списки пизображений для одного полежнения _pic - герой, _mpic - враги

back_pic = [b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8, b_9]
front_pic = [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9]
left_pic = [l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_8, l_9]
right_pic = [r_1, r_2, r_3, r_4, r_5, r_6, r_6, r_7, r_8, r_8, r_9]
back_mpic = [mb_1, mb_2, mb_3]
front_mpic = [mf_1, mf_2, mf_3]
left_mpic = [ml_1, ml_2, ml_3]
right_mpic = [mr_1, mr_2, mr_3]


# Цикл удаляет фон в картинках

for j in (back_pic, right_pic, left_pic, front_pic):
    for i in j:
        i.set_colorkey((255, 255, 255))

for j in (back_mpic, front_mpic, left_mpic, right_mpic):
    for i in j:
        i.set_colorkey((0, 255, 0))

evil_images=[]

def vis_evil(units, tick):
    '''
    В цикле определяется нужное изображения для каждого врага
    После цикла отрисовывается изображение
    В качестве аргументов принимает список юнитов и счетчик
    '''
    global evil_images
    number = 0
    counter = ((tick % 11) // 3) % 3
    for i in units:
        if units.index(i) != 0:
            if i.Vy < 0:
                evil_images[number] = back_mpic[counter]
            elif i.Vy > 0:
                evil_images[number] = front_mpic[counter]
            elif i.Vx < 0:
                evil_images[number] = left_mpic[counter]
            elif i.Vx > 0:
                evil_images[number] = right_mpic[counter]
            else:
                evil_images[number] = mf_1
            screen.blit(evil_images[number], [i.x, i.y])
            number = number + 1

def vis_evil_create(units):
    '''
    Создается список с изображениями по количеству врагов
    В качестве аргументов принимает список юнитов
    '''
    global evil_images
    func_evil_images = []
    for i in units:
        if units.index(i) != 0:
            func_evil_images.append(evil_image)
    evil_images = func_evil_images

def vis_unit(units):
    '''
    В цикле определяется необходимое изображение для героя
    После цикла изображение накладывается на прямоугольник героя
    В качестве аргументов принимает список юнитов
    '''
    global hero_image, back_counter, front_counter, left_counter, right_counter
    if units[0].Vy != 0 or units[0].Vx != 0:
        if units[0].orientation == 'top':
            hero_image = back_pic[back_counter]
            back_counter = (back_counter + 1) % len(back_pic)
        elif units[0].orientation == 'bot':
            hero_image = front_pic[front_counter]
            front_counter = (front_counter + 1) % len(front_pic)
        elif units[0].orientation == 'left':
            hero_image = left_pic[left_counter]
            left_counter = (left_counter + 1) % len(left_pic)
        elif units[0].orientation == 'right':
            hero_image = right_pic[right_counter]
            right_counter = (right_counter + 1) % len(right_pic)
    else:
        if units[0].orientation == 'top':
            hero_image = back_pic[1]
        elif units[0].orientation == 'bot':
            hero_image = front_pic[front_counter]
        elif units[0].orientation == 'left':
            hero_image = left_pic[left_counter]
        elif units[0].orientation == 'right':
            hero_image = right_pic[right_counter]
    screen.blit(hero_image, [units[0].x, units[0].y])


