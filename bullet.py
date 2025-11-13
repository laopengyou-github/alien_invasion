import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''一个对飞船发射子弹进行管理的类'''
    def __init__(self,game_settings,screen,ship):
        '''在飞船所处的位置创建一个子弹对象'''
        super().__init__()# python2.7中super(Bullet,self).__init__()等价于python3中的super().__init__()，此处二者均可使用
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,game_settings.bullet_width,game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed_factor

    def update(self):
        '''向上移动子弹'''
        # 更新表示子弹的rect的位置
        self.y -= self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw(self):
        '''在屏幕上绘制子弹'''
        pygame.draw.rect(self.screen,self.color,self.rect)



