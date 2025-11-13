from typing import Any
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,screen,game_settings) -> None:
        '''初始化飞船类'''
        super().__init__()
        #　显示的位置
        self.screen = screen
        self.game_settings = game_settings
        # 加载外星人图像并获取其外接矩形
        self.image =pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 每个外星人最初都在屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 移动标志
        self.moving_right = False
        
    def blitme(self):
        # 将self.image绘制到self.rect指定的位置上
        self.screen.blit(self.image,self.rect)

    def check_edge(self):
        screen_rect = self.screen_rect
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    

    def update(self):
        self.x += (self.game_settings.alien_speed_factor*self.game_settings.fleet_direction)
        self.rect.x = self.x