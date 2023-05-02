import pygame
from pygame.sprite import Sprite
"""
self.rect 参数介绍:
rect.right: 矩形对象右边缘到y轴的距离
rect.left: 矩形对象的左边缘到y轴的距离
rect.top: 矩形对象的上边缘到x轴的距离
rect.bottom: 矩形对象的下边缘到x轴的距离
rect.x: 等价于rect.left
rect.y: 等价于rect.top
由上述陈述可推出如下关系:
rect.bottom = rect.top + rect.height
rect.right = rect.left + rect.width

(0, 0)=================================================> x+
||                                       /|    /|
||<--rect.x-->                          rect.y  |
||<rect.left>|                         rect.top |
||           |___________________________ |/    |
||     /|    |<------  rect.width ------>|      |
||      |    |                           |    rect.bottom
||      |    |                           |      |
||  rect.height                          |      |
||      |    |                           |      |
||      |    |                           |      |
||      |/   --------------------------(x, y)   |/
||<------------  rect.right  ----------->|
||/
|/
/
y+
"""


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其 rect 属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人的初始位置都在屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回 True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """向右或向左移动外星人"""
        """
        Pycharm 会发现这里的重写，并告知用户
        外星人是编组元素，而 Sprite 本身自带 update() 方法
        所以这里相当于重写了 Sprite 的 update() 方法
        """
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
