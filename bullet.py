'''
新建子弹类，实例化子弹属性，以及子弹相关的函数，包括根据当前打击敌人的方向修改自己下一步的坐标
'''

from Config import *
import pygame
import math

# 玩家1飞机图 up down right left
bullet1Img_right = pygame.image.load('./images/红方子弹右飞.png')
bullet1Img_left = pygame.image.load('./images/红方子弹左飞.png')
bullet1Img_up = pygame.image.load('./images/红方子弹上飞.png')
bullet1Img_down = pygame.image.load('./images/红方子弹下飞.png')
bullet2Img_right = pygame.image.load('./images/蓝方子弹右飞.png')
bullet2Img_left = pygame.image.load('./images/蓝方子弹左飞.png')
bullet2Img_up = pygame.image.load('./images/蓝方子弹上飞.png')
bullet2Img_down = pygame.image.load('./images/蓝方子弹下飞.png')

bulletImg_dict = {
    'red_left': bullet1Img_left,
    'red_right': bullet1Img_right,
    'red_up': bullet1Img_up,
    'red_down': bullet1Img_down,
    'blue_left': bullet2Img_left,
    'blue_right': bullet2Img_right,
    'blue_up': bullet1Img_up,
    'blue_down': bullet1Img_down,
}


# 完成目标突击时轰炸机的方位角计算
def calculate_2d_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    # 为了符合pygame坐标系，加个负号上去
    dy = -(pos2[1] - pos1[1])
    z = math.sqrt(dx * dx + dy * dy)
    angle = round(math.asin(dy / z) / math.pi * 180)
    if dx == 0 and dy >= 0:
        return 0
    elif dx == 0 and dy <= 0:
        return 180
    if dy == 0 and dx >= 0:
        return 90
    elif dy == 0 and dx <= 0:
        return 270
    if dx > 0 and dy > 0:
        return angle
    elif dx > 0 and dy < 0:
        return angle * -1 + 90
    elif dx < 0 and dy < 0:
        return (90 - angle * -1) + 180
    elif dx < 0 and dy > 0:
        return angle + 270

# 计算两点（子弹、目标飞机）之间的距离
def calclate_distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    # 为了符合pygame坐标系，加个负号上去
    dy = (pos2[1] - pos1[1])
    z = math.sqrt(dx * dx + dy * dy)
    return z

class BULLET:
    # 构造方法传入 发射目标和打击目标
    def __init__(self, ori_air, dis_air):
        self.ori_air = ori_air
        self.dis_air = dis_air
        # 修正子弹发射时和飞机的位置
        if ori_air.color == 'red':
            self.x = ori_air.x + AIR_SIZE/2 - 35
            self.y = ori_air.y + AIR_SIZE/2 - 35
            self.air_speed = PLAYER1_BULLET_SPEED
        else:
            self.x = ori_air.x + AIR_SIZE / 2 - 35
            self.y = ori_air.y + AIR_SIZE / 2 - 35
            self.air_speed = PLAYER2_BULLET_SPEED

        self.calc_bullet_dir()

    # 子弹的方向默认为飞机发射子弹时的方向，且不可改变，该方法仅在init中调用一次
    # 子弹的方向可能有 w s a d四种
    def calc_bullet_dir(self):
        self.dir = self.ori_air.dir

    # 子弹的图片由子弹dir决定（子弹dir一旦发射不可修改）
    def get_now_dir_bullet_pic(self):
        self.now_dir_pic = bulletImg_dict[self.ori_air.color + '_' + self.dir]
        return self.now_dir_pic

    # 目前规定射出的子弹路劲必须是直线路径，仅x 或者 y改变
    def update_point(self):
        if self.dir == 'up':
            self.y -= self.air_speed
        elif self.dir == 'down':
            self.y += self.air_speed
        elif self.dir == 'left':
            self.x -= self.air_speed
        elif self.dir == 'right':
            self.x += self.air_speed


    # 判断当前子弹对象是否射中目标,使用欧氏距离判断
    def judge_hit_dis(self):
        distance = calclate_distance([self.x, self.y], [self.dis_air.x, self.dis_air.y+30])
        # 打击中了返回True
        if self.ori_air.color == 'red':
            if distance <= PLAYER1_HIT_LIMIT_DISTANCE:
                return True
            else:
                return False
        else:
            if distance <= PLAYER2_HIT_LIMIT_DISTANCE:
                return True
            else:
                return False

    # 计算子弹当前方向
    # def calc_bullet_dir(self):
    #     if self.x > self.dis_air.x:
    #         self.dir = 'left'
    #     else:
    #         self.dir = 'right'

    # todo 更正子弹方向并根据dir自动加载当前方向的子弹图片
    # def get_now_dir_bullet_pic(self):
    #     self.calc_bullet_dir()
    #     self.now_dir_pic = bulletImg_dict[self.ori_air.color + '_' + self.dir]
    #     return self.now_dir_pic

    # todo 根据子弹当前位置和敌方飞机坐标 更新下一步子弹的坐标，沿着xy都移动
    # def update_point(self):
    #     # 首先计算子弹当前位置和dis飞机当前位置的夹角
    #     attack_angle = calculate_2d_angle(pos1=[self.x, self.y],
    #                                       pos2=[self.dis_air.x, self.dis_air.y])
    #
    #     # y是越往下越大，x越往右越大
    #     if self.x > self.dis_air.x + AIR_SIZE/2:
    #         self.x -= BULLET_SPEED * math.cos(math.radians(attack_angle))
    #     elif self.x < self.dis_air.x + AIR_SIZE/2:
    #         self.x += BULLET_SPEED * math.cos(math.radians(attack_angle))
    #     if self.y > self.dis_air.y + AIR_SIZE/2:
    #         self.y -= BULLET_SPEED * math.sin(math.radians(attack_angle))
    #     elif self.y < self.dis_air.y + AIR_SIZE/2:
    #         self.y += BULLET_SPEED * math.sin(math.radians(attack_angle))


if __name__ == '__main__':
    x = calculate_2d_angle([0, 0], [-10, 10])
    print(x)
    print(math.cos(math.radians(x)))
