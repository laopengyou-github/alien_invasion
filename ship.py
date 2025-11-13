import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,screen,game_settings) -> None:
        '''初始化飞船并设置其起始位置'''
        super().__init__()
        '''显示的位置'''
        self.screen = screen

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = float(self.screen_rect.centerx)
        self.rect.bottom = float(self.screen_rect.bottom)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 飞船速度
        self.Speed = game_settings.shipSpeed

    def update(self):
        if self.moving_right and (self.rect.bottomright < self.screen_rect.bottomright):
            self.rect.centerx += self.Speed

        if self.moving_left and (self.rect.bottomleft > self.screen_rect.bottomleft):
            self.rect.centerx -= self.Speed

        if self.moving_up and (self.rect.top > self.screen_rect.top):
            self.rect.bottom -= self.Speed

        if self.moving_down and (self.rect.bottom < self.screen_rect.bottom):
            self.rect.bottom += self.Speed


    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.rect.centerx = float(self.screen_rect.centerx)
        self.rect.bottom = float(self.screen_rect.bottom)