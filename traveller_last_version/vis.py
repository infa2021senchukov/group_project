import pygame

screen_height = 1000
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))


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

back_counter = 0
front_counter = 0
left_counter = 0
right_counter = 0
hero_image = f_5

back_pic = [b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8, b_9]
front_pic = [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9]
left_pic = [l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_8, l_9]
right_pic = [r_1, r_2, r_3, r_4, r_5, r_6, r_6, r_7, r_8, r_8, r_9]

for j in (back_pic, right_pic, left_pic, front_pic):
    for i in j:
        i.set_colorkey((0, 0, 0))


