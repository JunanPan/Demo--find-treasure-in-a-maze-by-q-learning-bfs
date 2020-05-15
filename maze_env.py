"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example. The RL is in RL_brain.py.

"""


import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


UNIT = 40   # pixels
MAZE_H = 5  # grid height    1111111
MAZE_W = 5  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # hell障碍物 #111111111111111111
        
        # 迷宫环境由 4*4(160*160;像素)的方格拼接而成，
        # 每个方格的大小为40*40(像素)，
        # 方格中的矩形大小为30*30(像素)，
        
        hell1_center = origin + np.array([UNIT, UNIT])
        # 其中创建矩形块的函数为：
        # canvas.create_rectangle(x1,y1,x2,y2)
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        # hell
        hell2_center = origin + np.array([UNIT * 3, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')
        # hell
        hell3_center = origin + np.array([UNIT * 2, UNIT * 3])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')

        # create oval 宝藏
        oval_center = origin + UNIT * 3
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()
    '''
    初始红色矩形块的observation由env.reset()函数得来，
    本来值为[5.0,5.0,35.0,35.0]。
    '''
    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)#1111111111111
        #生成0-25，但要去除障碍物和宝藏处
        new = np.random.choice([i for i in range(25) if i not in [6, 13, 17, 18]])
        #[6, 13, 17, 18]正好是障碍物和宝藏的按顺序位置标记
        origin = np.array([20, 20]) + np.array([UNIT * (new % 5), UNIT * (new // 5)])
        #//5得到行，%5得到列 （20，20）是初始位置的中心
        self.rect = self.canvas.create_rectangle(
            #位置标记块大小是30，所以往上下左右都是15
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        '''
        输入：采取的动作
        输出：下一个状态探索者所在位置、奖励、是否完成本次回合

        '''
        s = self.canvas.coords(self.rect)
        #首先获取红色矩形块的位置
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:#判断边界
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT
        elif action == 3:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT


        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent
        #根据当前位置和采取的动作更新当前的位置状态，
        # 获得下一个状态s_
        s_ = self.canvas.coords(self.rect)  # next state

        # reward function

        if s_ == self.canvas.coords(self.oval):
            #如果下一状态到达黄色圆圈则获得+1的正奖励
            reward = 1
            done = True#如果下个状态为黄色圆圈或黑色矩阵，都结束本回合；
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),self.canvas.coords(self.hell3)]:
            reward = -1
            #如果到达黑色矩形块则会获得-1的负奖励
            done = True#如果下个状态为黄色圆圈或黑色矩阵，都结束本回合；
            s_ = 'terminal'
        else:
            #到达其他位置获得的奖励为0
            reward = 0
            done = False#否则继续

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break

if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()