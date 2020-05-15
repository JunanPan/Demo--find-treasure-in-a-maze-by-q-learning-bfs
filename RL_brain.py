"""
This part of code is the Q learning brain, which is a brain of the agent.
All decisions are made in here.

"""

import numpy as np
import pandas as pd


class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.lr = learning_rate#学习率
        self.gamma = reward_decay#折扣因子
        self.epsilon = e_greedy#采取贪婪策略中的概率
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        #q表，用dataframe结构存储
    def choose_action(self, observation):
        '''
        输入：红色矩形块当前位置
        输出：动作action

        '''
        self.check_state_exist(observation)
        #检测当前位置是否在 q_table 中存在 （check_state_exist函数）
        # action selection

        #接下来采用𝜖 – 贪婪策略：
        if np.random.uniform() < self.epsilon:#epsilon = e_greedy = 0.9
            # choose best action
            #百分之九十的概率选择Q表中较大Q值的动作
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            #百分之十的概率随机选择动作
            action = np.random.choice(self.actions)
        return action

    #Q表更新函数
    def learn(self, s, a, r, s_):
        '''
        输入：agent当前状态、采取的动作、奖励、采取动作后探索者下一个状态
        输出：最后完成更新的Q表
        '''
        self.check_state_exist(s_)
        #检测下一个状态是否在 q_table 中存在 （check_state_exist）

        q_predict = self.q_table.loc[s, a]
        #根据当前的状态s和采取的动作a结合Q表得出预测值q_predict
        if s_ != 'terminal':
            #如果下一个状态S_不是终点：
            #则按相应公式计算，只计算了其中一部分
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
        #如果下一个状态S_是终点则：q_target = R
            q_target = r  # next state is terminal
        #计算公式剩余部分，从而完成Q表的更新
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
    #检测当前位置是否在 q_table 中存在 （check_state_exist函数）
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )