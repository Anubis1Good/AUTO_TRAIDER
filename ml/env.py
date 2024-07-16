import os
from random import choice
import pandas as pd
import numpy as np
import cv2
from info_for_study import sec_codes
from help_about_VT import get_chart_point,get_last_points_trend,get_current_level
from help_our_func import change_amount_points

df_path = './DataFrames'
img_path = './DataForLearning'
days = os.listdir(df_path)

class EmulationStock:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.name = choice(sec_codes)
        self.day = choice(days)
        self.df = pd.read_csv(f'{df_path}/{self.day}/{self.name}.csv')
        self.position = 0
        self.price_pos = 0
        self.profit = 0
        self.global_profit = 0
        self.img_path = f'{img_path}/{self.day}/images/'
        self.step = 0
        self.zero_pos = 0
        self.limit = self.df.shape[0] - 5
        print(self.name,self.day)

    def give_state(self):
        img = cv2.imread(self.img_path+self.df.iloc[self.step]['img'])
        tops,bottoms = get_chart_point(img)
        slope,top_trend,bottom_trend = get_last_points_trend(tops,bottoms)
        tops = tops[:,1:].flatten()
        bottoms = bottoms[:,1:].flatten()
        norm = np.max(bottoms)
        tops = change_amount_points(tops,10)/norm
        bottoms = change_amount_points(bottoms,10)/norm
        top_trend = top_trend[1]/norm
        bottom_trend = bottom_trend[1]/norm
        y_cur_price = get_current_level(img)/norm
        state = list(tops) + list(bottoms)
        state.append(top_trend)
        state.append(bottom_trend)
        state.append(slope)
        state.append(y_cur_price)
        state.append(self.position)
        return tuple(state)
        
            
# DataForLearning\9.07.24\images\MRKV1720516447.2800508.png
    def change_pos(self,action):
        if action == self.position and action != 0:
            return -10000
        else:
            self.position += action
            if action == 0:
                return -1
            else:
                if self.position == 0:
                    self.zero_pos += 1
                    self.price_pos = 0
                    if self.zero_pos < 8:
                        return -10
                    self.zero_pos = 0
                    return -10000
                else:
                    self.price_pos = self.df.iloc[self.step]['price']
                    return 10
    
    def make_step(self,action):
        if np.array_equal(action, [1, 0, 0]):
            delta_pos = 0
        if np.array_equal(action, [0, 1, 0]):
            delta_pos = 1
        if np.array_equal(action, [0, 0, 1]):
            delta_pos = -1
        reward = self.change_pos(delta_pos)
        if self.position == -1:
            self.profit = int((1 - (self.df.iloc[self.step]['price']/self.price_pos)) * 10000)
        if self.position == 1:
            self.profit = int(((self.df.iloc[self.step]['price']/self.price_pos)-1) * 10000)
        reward += self.profit
        self.step += 1
        
        done = True
        if self.step < self.limit:
            done = False
        self.global_profit += self.profit
        return reward, done, self.global_profit

if __name__ == '__main__':
    es = EmulationStock()
    print(es.give_state())
    print(es.make_step([1,0,0]))
    print(es.give_state())
    print(es.make_step([1,0,0]))
    print(es.give_state())
    print(es.make_step([1,0,0]))
    print(es.give_state())
    # print(len(es.give_state()))


