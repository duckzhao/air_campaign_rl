'''
新建飞机类，实例化飞机属性，以及飞机相关的函数，包括根据当前方向修改自己下一步的坐标
'''
from Config import *
import pygame
from bullet import BULLET
import math

# 计算两点（飞机、目标飞机）之间的距离
def calclate_distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    # 为了符合pygame坐标系，加个负号上去
    dy = (pos2[1] - pos1[1])
    z = math.sqrt(dx * dx + dy * dy)
    return z

# 玩家1飞机图 up down right left
player1Img_right = pygame.image.load('./images/红方战斗机右飞.png')
player1Img_left = pygame.image.load('./images/红方战斗机左飞.png')
player1Img_up = pygame.image.load('./images/红方战斗机上飞.png')
player1Img_down = pygame.image.load('./images/红方战斗机下飞.png')
player1Img_dict = {
    'up': player1Img_up,
    'down': player1Img_down,
    'left': player1Img_left,
    'right': player1Img_right
}

class PLAYER1:
    def __init__(self):
        self.color = 'red'
        self.reset_()
        # 添加情报系统，包含视野，可打击目标，敌方子弹的位置
        # 初步设计只有在视野范围内的武器才可被打击，先不加入攻击范围
        self.obs = {}

    def reset_(self):
        self.x = random.randint(50, 150)
        self.y = random.randint(100, 500)
        self.air_speed = PLAYER1_AIR_SPEED
        self.dir = PLAYER1_DIR
        self.bullet_num = PLAYER1_BULLET_NUM
        # 飞机视野范围
        self.view_space = PLAYER1_VIEW_SPACE
        self.view_color = PLAYER1_VIEW_COLOR
        self.attack_distance = PLAYER1_ATTACK_DISTANCE

    # 根据dir自动加载当前方向的飞机图片
    def get_now_dir_air_pic(self):
        self.now_dir_pic = player1Img_dict[self.dir]
        return self.now_dir_pic

    # 如何根据键盘事件输入修改飞机方向
    def update_dir(self, key_input):
        if key_input == 'up' and self.dir != 'down':
            self.dir = 'up'
        if key_input == 'down' and self.dir != 'up':
            self.dir = 'down'
        if key_input == 'right' and self.dir != 'left':
            self.dir = 'right'
        if key_input == 'left' and self.dir != 'right':
            self.dir = 'left'

    # 根据方向更新当前飞机的坐标
    def update_point(self):
        # y是越往下越大，x越往右越大
        if self.dir == 'up':
            self.y -= self.air_speed
        elif self.dir == 'down':
            self.y += self.air_speed
        elif self.dir == 'left':
            self.x -= self.air_speed
        elif self.dir == 'right':
            self.x += self.air_speed

    # 飞机发弹函数，当外部event事件触发PLAYER1_ATTACK_KEY时调用，首先判断攻击范围（目前用视野范围代替）是否有敌人，有敌人才能打击
    # todo 可以加入子弹发射数量、时间 间隔等等的限制
    def attack_enemy(self, dis_air):
        # 先判断是否在攻击范围内
        real_distance = calclate_distance([self.x+AIR_SIZE/2, self.y+AIR_SIZE/2],
                                          [dis_air.x+AIR_SIZE/2, dis_air.y+AIR_SIZE/2])
        # print(real_distance, self.attack_distance)
        if real_distance <= self.attack_distance:
            if self.bullet_num > 0:
                bullet = BULLET(self, dis_air)
                self.bullet_num -= 1
                return bullet
            else:
                return None
        else:
            print('距离太远')
            return None

# 玩家2飞机图 up down right left
player2Img_right = pygame.image.load('./images/蓝方轰炸机右飞.png')
player2Img_left = pygame.image.load('./images/蓝方轰炸机左飞.png')
player2Img_up = pygame.image.load('./images/蓝方轰炸机上飞.png')
player2Img_down = pygame.image.load('./images/蓝方轰炸机下飞.png')
player2Img_dict = {
    'up': player2Img_up,
    'down': player2Img_down,
    'left': player2Img_left,
    'right': player2Img_right
}

class PLAYER2:
    def __init__(self):
        self.color = 'blue'
        self.reset_()

    # 初始化玩家的位置
    def reset_(self):
        self.x = WINDOW_WIDTH - random.randint(50, 150)
        self.y = random.randint(100, 500)
        self.air_speed = PLAYER2_AIR_SPEED
        self.dir = PLAYER2_DIR
        self.bullet_num = PLAYER2_BULLET_NUM
        self.view_space = PLAYER2_VIEW_SPACE
        self.view_color = PLAYER2_VIEW_COLOR
        self.attack_distance = PLAYER2_ATTACK_DISTANCE
        # 防止瞬间发弹过多
        self.auto_attack_times = 0

    # 根据dir自动加载当前方向的飞机图片
    def get_now_dir_air_pic(self):
        self.now_dir_pic = player2Img_dict[self.dir]
        return self.now_dir_pic

    # 如何根据键盘事件输入修改飞机方向
    def update_dir(self, key_input):
        if key_input == 'up' and self.dir != 'down':
            self.dir = 'up'
        if key_input == 'down' and self.dir != 'up':
            self.dir = 'down'
        if key_input == 'right' and self.dir != 'left':
            self.dir = 'right'
        if key_input == 'left' and self.dir != 'right':
            self.dir = 'left'

    # 根据方向更新下一步飞机的坐标
    def update_point(self):
        # y是越往下越大，x越往右越大
        if self.dir == 'up':
            self.y -= self.air_speed
        elif self.dir == 'down':
            self.y += self.air_speed
        elif self.dir == 'left':
            self.x -= self.air_speed
        elif self.dir == 'right':
            self.x += self.air_speed

    # 飞机发弹函数，当外部event事件触发PLAYER2_ATTACK_KEY时调用
    # todo 可以加入子弹发射数量、时间 间隔等等的限制
    def attack_enemy(self, dis_air):
        # 先判断是否在攻击范围内
        real_distance = calclate_distance([self.x+AIR_SIZE/2, self.y+AIR_SIZE/2],
                                          [dis_air.x+AIR_SIZE/2, dis_air.y+AIR_SIZE/2])
        # print(real_distance, self.attack_distance)
        if real_distance <= self.attack_distance:
            if self.bullet_num > 0:
                bullet = BULLET(self, dis_air)
                self.bullet_num -= 1
                return bullet
            else:
                return None
        else:
            print('距离太远')
            return None

    # 自动按照一定的规律随机矩形转动
    def auto_update_dir(self):
        # 如果x太大或者太小就随机选择左右方向移动
        if (self.x > WINDOW_WIDTH - 100) and self.dir in ['left', 'right']:
            self.dir = 'left'
        if self.x < 100:
            self.dir = 'right'

    # 每当敌人出现在视野圈内时自动发弹，无限弹药
    def auto_attack_enemy(self, dis_air):
        real_distance = calclate_distance([self.x + AIR_SIZE / 2, self.y + AIR_SIZE / 2],
                                          [dis_air.x + AIR_SIZE / 2, dis_air.y + AIR_SIZE / 2])
        if real_distance <= self.attack_distance and self.auto_attack_times == 0:
            bullet = BULLET(self, dis_air)
            self.auto_attack_times = 100
            return bullet
        else:
            if self.auto_attack_times > 0:
                self.auto_attack_times -= 1
            return None