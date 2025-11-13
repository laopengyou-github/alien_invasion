import pygame


class Shipboard():
    '''显示飞船个数的面板类'''
    def __init__(self, screen, game_settings):
        # 显示位置
        self.screen = screen
        # ship数量
        self.ship_number = game_settings.ship_limit
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘飞船放在屏幕底部中央
        self.rect.top = self.screen_rect.top
        self.rect.left = self.screen_rect.left
        # self.rect.center = self.screen_rect.center

    def draw(self):
        self.screen.blit(self.image, self.rect)
