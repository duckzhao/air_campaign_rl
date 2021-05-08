import random

# 游戏进行的轮次
EPISODE = 10000

# 游戏画面更新的频率，越大跑得越快
FPS = 2000

# 窗口大小
WINDOW_WIDTH = 20*75
WINDOW_HIGHT = 20*30

# 飞机元素大小
AIR_SIZE = 128

# 对于飞机而言的游戏窗口行数、列数
WINDOW_ROW = WINDOW_WIDTH/20
WINDOW_COL = WINDOW_HIGHT/20

# 飞机的初始位置
PLAYER1_INIT_X = random.randint(50, 150)
PLAYER1_INIT_Y = random.randint(100, 200)

PLAYER2_INIT_X = WINDOW_WIDTH - random.randint(50, 150)
PLAYER2_INIT_Y = random.randint(100, 200)

# 游戏结束的状态,0表示游戏正常进行中
NOTHING = 0  # 正常对局中
RED_WIN = 1
BLUE_WIN = 2
NO_WIN = 3  # 平局

# 游戏结束类型
NOT_OVER = 0
OUT_OF_MAP = 1
ATTACKED = 2

# 飞机的速度
PLAYER1_AIR_SPEED = 0.5
PLAYER2_AIR_SPEED = 1

# 子弹的飞行速度
PLAYER1_BULLET_SPEED = 2
PLAYER2_BULLET_SPEED = 1.5

# 飞机飞行方向字典,完成数字映射
DIR_DICT = {
    'up': 0,
    'down': 1,
    'left': 2,
    'right': 3
}

# 飞机初始的方向,right left up down
PLAYER1_DIR = 'right'
PLAYER2_DIR = 'left'

# 飞机发射子弹键码，空格 ctrl
PLAYER1_ATTACK_KEY = 32
PLAYER2_ATTACK_KEY = 1073742052

# 飞机装配弹药数设计
PLAYER1_BULLET_NUM = 6
PLAYER2_BULLET_NUM = 6

# 子弹打击中的最小距离判断
PLAYER1_HIT_LIMIT_DISTANCE = 10
PLAYER2_HIT_LIMIT_DISTANCE = 20

# 飞机视野范围设计---直径
PLAYER1_VIEW_SPACE = 200
PLAYER2_VIEW_SPACE = 160

# 飞机的攻击范围
PLAYER1_ATTACK_DISTANCE = 200
PLAYER2_ATTACK_DISTANCE = 160

# 飞机视野范围颜色
PLAYER1_VIEW_COLOR = [255, 0, 0]    # red
PLAYER2_VIEW_COLOR = [0, 0, 255]    # blue

# 玩家1的行为字典
PLAYER1_ACTION_DICT = {
    0: 'up',
    1: 'down',
    2: 'left',
    3: 'right',
    4: 'attack'
}