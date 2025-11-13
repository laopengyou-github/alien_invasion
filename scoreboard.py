import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    def __init__(self, screen, stats, game_settings):
        '''计分板属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        # 显示得分信息使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.board_width = 100
        self.board_height = 50
        # self.rect = pygame.Rect(0,0,self.width,self.height)

        # 准备初始得分并创建得分图像
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.game_settings.bg_color)
        
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # self.text_surface = self.font.render(str(score),True,self.text_color,None)
        # self.text_rect = self.text_surface.get_rect()
        # self.text_rect.topright = (self.game_settings.screen_width - 10, 10)

    def prep_level(self):
        pass

    def prep_ships(self):
        """显示余下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.screen, self.game_settings)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.ships.draw(self.screen)