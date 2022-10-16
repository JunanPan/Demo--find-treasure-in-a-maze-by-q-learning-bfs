import copy
import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk
import random
UNIT = 40   # pixels
MAZE_H = 5  # grid height                    
MAZE_W = 5  # grid width
obstacles = [(2,2),(4,3),(3,4)] 
def generate_start_location():
        x=2
        y=2#一开始初始化为障碍物的位置，保证起点第一次是随机生成
        while (x,y)  in obstacles:#当x，y生成位置是障碍物时，就重新生成 
            x = random.randint(1,5)
            y = random.randint(1,5)
        return x,y
x,y = generate_start_location()
new = (y-1)*5+x-1
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
        # hell#111111111111111111
        hell1_center = origin + np.array([UNIT, UNIT])
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
        # create oval
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
    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20]) + np.array([UNIT * (new % 5), UNIT * (new // 5)])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        # return observation
        return self.canvas.coords(self.rect)
    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
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
        s_ = self.canvas.coords(self.rect)  # next state
        # reward function
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2),self.canvas.coords(self.hell3)]:
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False
        return s_, reward, done
    def render(self):
        time.sleep(1)
        self.update()
def update():
    s = env.reset()
    for a in aa:
        env.render()
        s, r, done = env.step(a)
        # time.sleep(500)
        if done:
            break
def fuzhi(q1, q0):  # 把q0队列复制给q1
    q1.queue = []
    for item1 in q0.queue:
        item2 = copy.deepcopy(item1)
        q1.queue.append(item2)
class Queue():
    def __init__(self):
        # self.size = size
        self.queue = []
    def insert(self, item):
        self.queue.append(item)
    def pop(self):
        a = self.queue[0]
        self.queue.remove(a)
        return a
    def is_empty(self):
        if len(self.queue) == 0:
            return True
    def exist(self, a):
        for item in self.queue:
            if (item.x == a.x) & (item.y == a.y):
                return True
        return False
class now():
    def __init__(self, x, y, pre):
        self.x = x
        self.y = y
        self.pre = pre
q0 = Queue()
q1 = Queue()
# q0用来存放所有遍历过的位置 q1用来存放当前一层的，每一q1就代表一步
step = 0
res = []
def move():  # 操作
    global step
    step += 1
    q2 = Queue()  # q2用来存放下一层的，即由q1产生的子节点
    b = len(q1.queue)
    while (not q1.is_empty()):
        a = q1.pop()
        b = len(q1.queue)
        if (a.x == 4) & (a.y == 4):  # 到达目标状态
            print("totally {} steps".format(step-1))
            print('path:')
            # print('({},{})'.format(a.x, a.y))
            ss = a.pre
            while (ss):
                # print('({},{})'.format(ss.x, ss.y))
                res.append(tuple([ss.x,ss.y]))
                ss = ss.pre
            return
        x = a.x
        y = a.y
        if x != 5:#不能在最右边界了，否则无法再右移         # 右移
            if tuple([x+1,y]) not in obstacles:  # 判断右边是不是障碍物
                a.x += 1
                # b = copy.copy(a)
                b = now(a.x, a.y, a)
                a.next = b
                if not q0.exist(b):
                    q0.insert(b)
                    q2.insert(b)
                a.x -= 1
        if y != 5:#不能在最下边界 才能往下移动         # 下移
            if tuple([x,y+1])  not in obstacles:#判断下面是不是障碍物
                a.y += 1
                # b = copy.copy(a)
                b = now(a.x, a.y, a)
                a.next = b
                if not q0.exist(b):
                    q0.insert(b)
                    q2.insert(b)
                a.y -= 1
        if x != 1:#不能在最左边界         # 左移
            if tuple([x-1,y])  not in obstacles:
                a.x -= 1 #x减少1，左移
                # b = copy.copy(a)
                b = now(a.x, a.y, a)
                a.next = b
                if not q0.exist(b):
                    q0.insert(b)
                    q2.insert(b)
                a.x += 1
        if y != 1:#不能在最上边界         # 上移
            if tuple([x,y-1]) not in obstacles:
                a.y -= 1 #上移
                # b = copy.copy(a)
                b = now(a.x, a.y, a)
                a.next = b
                if not q0.exist(b):
                    q0.insert(b)
                    q2.insert(b)
                a.y += 1     # 现在q1已经为空，该遍历下一层
    fuzhi(q1, q2)  # 更新下一个q1为此时的q2，即向下一层
    move()
aa = []
a = now(x, y, None)
q0.insert(a)
fuzhi(q1, q0)
move()  # 移动操作
# print(res) #res就是得到的移动步骤
res.reverse()
res.append((4,4))
print(res)
for i in range(len(res)-1):
    #res[i],res[i+1]是每紧挨着的一对进行比较，得出移动方式
    #向上移动
    if res[i][0]==res[i+1][0] and res[i][1]-1==res[i+1][1]:
        aa.append(0)    #向上移动
    elif res[i][0]==res[i+1][0] and res[i][1]+1==res[i+1][1]:
        aa.append(1)    #向下移动
    elif res[i][1]==res[i+1][1] and res[i][0]-1==res[i+1][0]:
        aa.append(2)    #向左移动
    elif res[i][1]==res[i+1][1] and res[i][0]+1==res[i+1][0]:
        aa.append(3)    #向右移动
# print("move ways(up：0，down：1，left：2，right：3):",aa)
env = Maze()
env.after(1000, update)
env.mainloop()
