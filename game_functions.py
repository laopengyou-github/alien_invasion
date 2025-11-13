import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien
from shipboard import Shipboard


def fire_bullet(game_settings,screen,ship,bullets):
    #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings,screen,ship)
        bullets.add(new_bullet)



def check_keydown_event(event, game_settings, screen, ship, bullets):
    print("event.key", event.key, type(event.key))
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(game_settings,screen,ship,bullets)# 1073742049
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_event(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_event(game_settings,screen,aliens,ship,bullets,state,play_button,sb):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings,screen,ship,aliens,bullets,\
                      state,play_button,mouse_x,mouse_y,sb=sb)

def check_play_button(game_settings,screen,ship,aliens,bullets,\
                      state,play_button,mouse_x,mouse_y,sb):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not state.game_active:
        # 重置游戏设置
        game_settings.initialize_dynamic_settings()
        # 游戏过程中隐藏鼠标
        pygame.mouse.set_visible(False)
        # 重置游戏的统计信息
        state.reset_state()

        # 清除所有的外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人并让飞船居中
        create_fleet(game_settings, screen,ship, aliens)
        ship.center_ship()
        # 开始游戏
        state.game_active = True
        # 重置计分板图像
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()





def check_fleet_edge(game_settings,aliens):
    '''有外星人到达边缘时采取相应的措施'''
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(game_settings,aliens)
            break


def change_fleet_direction(game_settings,aliens):
    '''改变飞船舰队的移动方向以及向下移动'''
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1

def update_screen(game_settings,screen,ship,bullets,aliens,state,play_button,sb):
    '''更新屏幕上的图像，并切换到新屏幕'''
    # Update the screen with new data.
    screen.fill(game_settings.bg_color)
    # 画飞船
    ship.blitme()
    #　画子弹
    if state.game_active:
        # bullets.draw.rect(screen)
        for bullet in bullets.sprites():
            bullet.draw()
    # 画外星人
    # for alien in aliens.sprites():
    #     alien.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    if not state.game_active:
        play_button.draw_button()

    
    # 刷新最近画面
    pygame.display.flip()

def check_bullete_alien_collision(bullets,aliens,game_settings, screen,
                                  ship,state,sb):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        print(collisions)
        for alien in collisions.values():
            print(alien)
            state.score += game_settings.alien_points*len(alien)
            sb.prep_score()
            sb.show_score()

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(game_settings, screen, ship, aliens)
        game_settings.increase_speed()
  
def update_bullets(aliens,bullets,game_settings, screen,ship,state,sb):
    '''更新子弹的位置，并删除已消失的子弹'''
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检测是否有子弹击中外星人，如果有就删除相应的子弹和外星人
    check_bullete_alien_collision(bullets,aliens,game_settings, screen,ship,state,sb)

def ship_hit(game_settings,ship,bullets,aliens,state,screen,sb):
    # 将ship_left 减1
    if state.ship_left > 0:
        state.ship_left -= 1
        # 更新计分板
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        
        # 创建一群新的外星人，并将飞船放到屏幕中间
        create_fleet(game_settings,screen,ship,aliens)
        ship.center_ship() 
        # 暂停一段时间让玩家知道ship die
        sleep(0.5)
    else:
        state.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(game_settings,screen,aliens,ship,state,bullets,sb):
    check_fleet_edge(game_settings,aliens)
    aliens.update()

    # 检查alien是否与ship相撞
    if pygame.sprite.spritecollideany(ship,aliens):
        # print("Ship hitted!!!")
        ship_hit(game_settings=game_settings,ship=ship,\
                bullets=bullets,aliens=aliens,state=state,screen=screen,sb=sb)
    # 检查alien是否到达画面底部
    check_aliens_bottom(game_settings=game_settings,ship=ship,\
                bullets=bullets,aliens=aliens,state=state,screen=screen,sb=sb)

def check_aliens_bottom(game_settings,ship,bullets,aliens,state,screen,sb):
    ''' 检测外星人是否到达屏幕底部，并采取响应动作'''
    # 获取屏幕的rect
    screen_rect = screen.get_rect()
    # 轮询检查每个外星人是否到达底部
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings,ship,bullets,aliens,state,screen)
            break


def get_number_aliens_x(self:Alien):
    '''计算每行可容纳多少个外星人'''
    # 计算屏幕宽度减去外星人宽度的两倍，得到可容纳外星人的空间
    avalible_space = self.game_settings.screen_width - (2*self.rect.width)
    number_aliens_x = int(avalible_space/(2*self.rect.width))
    # 返回可容纳外星人的数量，即空间除以外星人宽度的两倍
    return number_aliens_x
def get_number_rows(game_settings,ship_height,alien_height):
    avalible_space_y = game_settings.screen_height - (3*alien_height)- ship_height
    number_rows = int(avalible_space_y/(2*alien_height))
    return  number_rows

def create_alien(game_settings, screen, aliens, alien_number,row_number):
    alien = Alien(screen,game_settings)
    alien_width = alien.rect.width
    alien.x = alien_width+alien_number*2*alien_width
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(game_settings, screen,ship, aliens):
    alien = Alien(screen,game_settings)
    number_aliens_x = get_number_aliens_x(alien)
    # print('一行飞船数为',number_aliens_x)
    number_rows = get_number_rows(game_settings,ship.rect.height,alien.rect.height)
    # column_alien_num = 3
    # alien_width = alien.rect.width
    # alien_height = alien.rect.height

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
                create_alien(game_settings=game_settings,screen=screen,aliens=aliens,alien_number=alien_number,row_number=row_number)


