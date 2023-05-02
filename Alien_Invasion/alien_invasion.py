import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()                                          # 初始化背景设置
        pygame.display.set_caption("Alien Invasion")           # 返回一个 surface 对象，表示整个游戏窗口
        self.settings = Settings()
        self.bg_color = self.settings.bg_color                 # 设置背景色
        self.screen = pygame.display.set_mode(                 # 创建一个显示窗口，指定窗口的尺寸
            (self.settings.screen_width, self.settings.screen_height)
        )
        # 下面3行代码用于全屏模式，因为不知道如何退出所以弃用了
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)   # 让 Pygame 生成一个覆盖整个显示器的屏幕
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # 创建外星人舰队
        self._create_fleet()

        # 创建存储游戏信息的实例，并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # 创建一个按钮
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 反复侦听键盘状态
            self._check_event()
            if self.stats.game_active:
                # 更新屏幕
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
            self._update_screen()

    def _update_screen(self):
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 在显示 Play 按钮前显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

# ------------------------------------------ 按键定义 ------------------------------------------ #
    def _check_event(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            # 向上移动飞船
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # 向下移动飞船
            self.ship.moving_down = True
            # 开火
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            # 结束游戏
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # 停止向右移动飞船
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # 停止向左移动飞船
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            # 停止向上移动飞船
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            # 停止向下移动飞船
            self.ship.moving_down = False

# ------------------------------------------ 发射子弹 ------------------------------------------ #
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 检查是否有子弹击中了外星人。如果是，就删除相应的子弹和外星人
        # 这里修改第 3 个参数 True/False，可以控制子弹是否消失
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        # 当整群外星人都被消灭后
        if not self.aliens:
            # 删除现有子弹并创建一群新的外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

# ------------------------------------------ 外星舰队 ------------------------------------------ #
    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人，但只是为了得到长宽参数
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # 计算一行能容纳几个外星人
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)
        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        num_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(num_rows):
            # 创建第n行外星人
            for alien_number in range(number_alien_x):
                # 创建一个外星人并将其加入当前行
                self._create_alien(alien_width, alien_height, alien_number, row_number)

    def _create_alien(self, alien_width, alien_height, alien_number, row_number):
        alien = Alien(self)
        alien.x = alien_width + 2 * alien_width * alien_number
        # 用下一行的公式亦可，效果是上一行的对称。重构之后，需要传入available_space_x这个参数
        # alien.x = available_space_x - 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print('Ship hit!!!')
            self._ship_hit()
        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """有外星人到达屏幕边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

# ------------------------------------------ 当飞船、屏幕底端与外星人碰撞时 ------------------------------------------ #
    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将 ship_left 减 1 并更新剩余飞船的显示图像
            self.stats.ships_left -= 1
            self.sb.prep_ship()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船放置到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(1.0)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到了一样处理
                self._ship_hit()
                break

# ------------------------------------------ Play按钮 ------------------------------------------ #
    def _check_play_button(self, mouse_pos):
        """为玩家单击按钮时开始新游戏"""
        button_click = self.play_button.rect.collidepoint(mouse_pos)
        if button_click and not self.stats.game_active:
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

            # 重置游戏的动态设置
            self.settings.initialize_dynamic_setting()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
