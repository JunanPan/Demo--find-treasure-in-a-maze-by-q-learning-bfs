import pandas as pd
from maze_env import Maze
from RL_brain import QLearningTable



q_table = pd.read_excel('./q_table.xlsx', index_col=0)

def update():
    for episode in range(100):
        # initial observation
        observation = env.reset()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            #RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
    # end of game
    print('game over')
    env.destroy()



if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)),e_greedy=1)
    RL.q_table = q_table
    env.after(100, update)
    env.mainloop()