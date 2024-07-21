import torch
import random
import numpy as np
from collections import deque
from env import EmulationStock
from model_RL import Linear_QNet, QTrainer


model = Linear_QNet(46, 64, 32, 3)
model.load_state_dict(torch.load('./Models/RL_model.pth'))

env = EmulationStock()

        # state = env.give_state()
        # return np.array(state)
while True:
    try:
        state_old = np.array(env.give_state())

        # get move
        final_move = [0,0,0]
        state0 = torch.tensor(state_old, dtype=torch.float)
        prediction = model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1
        print(final_move)
        env.test(final_move)
        # state_new = np.array(env.give_state())      

    except Exception as err:
        print(err)
        env.reset()
