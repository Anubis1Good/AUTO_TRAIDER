import torch
import random
import numpy as np
from collections import deque
from env import EmulationStock
from model_RL import Linear_QNet, QTrainer
from plot_help import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 128
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0.05 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(46, 64, 32, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        


    def get_state(self,env:EmulationStock):
        state = env.give_state()
        return np.array(state)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        # self.epsilon = 5000 - self.n_games
        final_move = [0,0,0]
        if random.random() < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        

        return final_move


def train():
    plot_profit = []
    plot_mean_profit = []
    plot_reward = []
    last_reward =0
    total_profit = 0
    record = 0
    agent = Agent()
    env = EmulationStock()
    while True:
        # get old state
        try:
            state_old = agent.get_state(env)
            # get move
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, profit = env.make_step(final_move)
            state_new = agent.get_state(env)
            # print('+-------------+')
            # print(state_old)
            # print('---------------')
            # print(state_new)
            # print('+-------------+')

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)
            last_reward += reward
            plot_reward.append(last_reward)
            if done:
                # train long memory, plot result
                env.reset()
                agent.n_games += 1
                agent.train_long_memory()
                if profit > record:
                    record = profit
                if agent.n_games%100 == 0:
                    agent.model.save()

                print('Game', agent.n_games, 'Profit', profit, 'Record:', record)

                plot_profit.append(profit)
                total_profit += profit
                mean_score = round((total_profit / agent.n_games),3)
                plot_mean_profit.append(mean_score)
                plot(plot_profit, plot_mean_profit)
        except Exception as err:
            print(err)
            env.reset()



if __name__ == '__main__':
    train()