import pygame

pic_menu = pygame.image.load("mainmenugame.png").convert()
pic_how = pygame.image.load("how.png").convert()
pic_start = pygame.image.load("start.png").convert()

place = 'menu'

class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.h = h
        self.w = w

    def press(self):
        mouse = pygame.mouse.get_pos()
        if mouse[0] < self.x + self.w and mouse[0] > self.x and mouse[1] < self.y + self.h and mouse[1] > self.y:
            return True
        return False




start_b = Button(143, 598, 435, 162)
how_b = Button(1115, 32, 56 ,56)









