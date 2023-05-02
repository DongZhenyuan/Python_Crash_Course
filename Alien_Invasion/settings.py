class Settings:
    """存储游戏《外星人入侵》中的所有设置"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 20

        # 外星人设置
        self.fleet_drop_speed = 5

        # 加快游戏的节奏
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        """初始化游戏的动态设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.6

        # fleet_direction 为 1 表示向右，为 -1 表示向左
        self.fleet_direction = 1

        # 记分
        self.alien_points = 10

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # 显示当前击杀每个外星人可得的分数
        # print(self.alien_points)
