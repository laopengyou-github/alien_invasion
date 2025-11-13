from settings import Settings
from ship import Ship
from pygame.sprite import Group
import game_functions as gf
import pygame
from game_state import Gamestats
from button import Button
from scoreboard import Scoreboard
from shipboard import Shipboard # 自己写的源代码没有这部分

def run_game():
    # Initialize game and create a screen object.

    pygame.init()

    # 创建一个屏幕对象
    game_settings = Settings()
    # 
    screen = pygame.display.set_mode((game_settings.screen_width,
                                      game_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一个group来存储子弹
    bullets = Group()

    # 创建一个group来存储外星人
    aliens = Group()

    # 创建一艘飞船
    ship = Ship(screen, game_settings)

    # 创建一个外星人
    # alien = Alien(screen, game_settings)
    gf.create_fleet(game_settings, screen, ship, aliens)

    # 打印一行可以显示的外星人个数
    # print('一行可以显示的外星人数为：',alien.count_aliens())
    # 创建一个用于存储游戏统计信息的实例
    stats = Gamestats(game_settings=game_settings)

    # 创建一个按钮对象
    play_button = Button(screen, game_settings, msg="Play")

    # 创建一个计数板对象
    sb = Scoreboard(screen, stats, game_settings)

    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_event(game_settings, screen, aliens, ship, bullets, stats,
                       play_button, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(aliens, bullets, game_settings,  screen, ship,
                              stats, sb)
            gf.update_aliens(game_settings, screen, aliens, ship, stats,
                             bullets, sb)
        # print(len(bullets))
        gf.update_screen(game_settings,  screen,  ship, bullets,  aliens,
                         stats, play_button, sb)
        

run_game()
