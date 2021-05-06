import pygame
from Config import *
import time
from player import PLAYER1, PLAYER2

# 加载imageziyuan
# 背景图
bgImg = pygame.image.load('./images/Background.png')
#  ico
icoImg = pygame.image.load('./images/ico.png')

# 加载背景音乐和独立音乐
# pygame.mixer.music.load('path')  # 加载背景音乐
# pygame.mixer.music.play(-1)  # 设置背景音乐循环播放
# bao_sound = pygame.mixer.Sound('path')  # 加载爆炸音效
# bao_sound.play()    # 播放爆炸音效一次

# 初始化pygame
pygame.init()
screen = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HIGHT))
pygame.display.set_caption('air campaign')
pygame.display.set_icon(icoImg)


# 判断游戏是否结束
def judge_game_over(player_list):
    global GAME_STATE
    # 如果玩家数量少于2，则游戏结束
    if len(player_list) < 2:
        return True

    for player in player_list:
        # 判断是否越界，每个方向越界的数值不同，不能统一用飞机像素大小
        if player.x + AIR_SIZE/2 <= 0 or player.y + AIR_SIZE/2 <= 0:
            print('超出边界')
            GAME_STATE = RED_WIN if (player.color == 'blue') else BLUE_WIN
            return True
        elif player.x > WINDOW_WIDTH - AIR_SIZE/2 or player.y > WINDOW_HIGHT - AIR_SIZE/2:
            print('超出边界')
            GAME_STATE = RED_WIN if (player.color == 'blue') else BLUE_WIN
            return True

# 监听外部事件输入，以改变飞机的移动方向，或者发弹---该函数可修改为rl的接口
# 玩家1和玩家2的键盘事件监听都在该函数中实现
def listen_key_input(pygame_event, palyer1, player2):
    if pygame_event.type == pygame.KEYDOWN:
        # 玩家1
        # w
        if pygame_event.key == 119:
            player1.update_dir('up')
        # s
        elif pygame_event.key == 115:
            player1.update_dir('down')
        # a
        elif pygame_event.key == 97:
            player1.update_dir('left')
        # d
        elif pygame_event.key == 100:
            player1.update_dir('right')
        # space
        elif pygame_event.key == PLAYER1_ATTACK_KEY:
            temp_bullet = player1.attack_enemy(dis_air=player2)
            if temp_bullet:
                bullet_list.append(temp_bullet)

        # 玩家2
        # w
        if pygame_event.key == 1073741906:
            player2.update_dir('up')
        # s
        elif pygame_event.key == 1073741905:
            player2.update_dir('down')
        # a
        elif pygame_event.key == 1073741904:
            player2.update_dir('left')
        # d
        elif pygame_event.key == 1073741903:
            player2.update_dir('right')
        # space
        elif pygame_event.key == PLAYER2_ATTACK_KEY:
            temp_bullet = player2.attack_enemy(dis_air=player1)
            if temp_bullet:
                bullet_list.append(temp_bullet)


# 对玩家输入事件的监听进行修改,将玩家2的游戏策略变为 以一定规律移动和发弹
def listen_key_input_2():
    pass


if __name__ == '__main__':
    while True:
        # 游戏主循环
        running = True

        # 记录实例化的飞机对象，不区分红蓝
        player_list = []

        # 记录实例化的子弹对象，不区分红蓝
        bullet_list = []

        # 实例化飞机对象
        player1 = PLAYER1()
        player_list.append(player1)
        player2 = PLAYER2()
        player_list.append(player2)

        # 判断游戏是否进行中的函数
        GAME_STATE = 0

        while running:
            # pygame的绘图是图层叠加的方式，因此背景图第一个画
            screen.blit(bgImg, dest=(0, 0))
            # 判断每一轮游戏窗口输入的事件
            for event in pygame.event.get():
                # 判断输入事件是否为窗口退出事件
                if event.type == pygame.QUIT:
                    running = False
                listen_key_input(event, player1, player2)
                # print(event)

            # 画出每一轮飞机的位置
            for player in player_list:
                screen.blit(player.get_now_dir_air_pic(), dest=(player.x, player.y))

            # 画出飞机的视野范围，以圈的形式画出
            for player in player_list:
                pygame.draw.circle(screen, player.view_color,
                                   [player.x+AIR_SIZE/2, player.y+AIR_SIZE/2], player.view_space, 2)

            # 更新下一轮飞机位置的移动情况--- todo 暂时不可以停止飞行？
            for player in player_list:
                player.update_point()

            # 判断每个子弹的击中情况
            new_bullet_list = []
            for bullet in bullet_list:
                # 如果打中了
                if bullet.judge_hit_dis():
                    # 移除被打击的飞机目标
                    # todo 此处可添加飞机击中的爆炸特效图片
                    player_list.remove(bullet.dis_air)
                    print('{}目标被击中'.format(bullet.dis_air.color))
                    GAME_STATE = RED_WIN if (bullet.ori_air.color == 'red') else BLUE_WIN
                else:
                    new_bullet_list.append(bullet)
            bullet_list = new_bullet_list

            # 画出每一轮子弹的位置
            for bullet in bullet_list:
                screen.blit(bullet.get_now_dir_bullet_pic(), dest=(bullet.x, bullet.y))

            # 更新下一轮子弹位置的移动情况---随着dis飞机的移动而移动
            for bullet in bullet_list:
                bullet.update_point()

            # 判断是否游戏结束
            if judge_game_over(player_list):
                print('游戏结束')
                if GAME_STATE == RED_WIN:
                    print('红方胜利')
                else:
                    print('蓝方胜利')
                print('开始下一局游戏')
                running = False
            # 更新画布，以显示所绘制的图案
            pygame.display.update()