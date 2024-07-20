import os
from random import choice
from time import time
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
        self.count_pos = 0
        self.limit = 0
        self.img = None
        self.profit_dir = 0
        self.reset()

    def reset(self):
        self.name = choice(sec_codes)
        self.day = choice(days)
        print(self.count_pos)
        print(self.limit)
        self.df = pd.read_csv(f'{df_path}/{self.day}/{self.name}.csv')
        self.position = 0
        self.price_pos = 0
        self.profit = 0
        self.global_profit = 0
        self.img_path = f'{img_path}/{self.day}/images/'
        self.step = 0
        self.limit = self.df.shape[0] - 5
        print(self.name,self.day)
        self.count_pos = 0

    def give_state(self):
        self.img = cv2.imread(self.img_path+self.df.iloc[self.step]['img'])
        tops,bottoms = get_chart_point(self.img)
        slope,top_trend,bottom_trend = get_last_points_trend(tops,bottoms)
        tops = tops[:,1:].flatten()
        bottoms = bottoms[:,1:].flatten()
        norm = np.max(bottoms)
        tops = change_amount_points(tops,10)/norm
        bottoms = change_amount_points(bottoms,10)/norm
        top_trend = top_trend[1]/norm
        bottom_trend = bottom_trend[1]/norm
        y_cur_price = get_current_level(self.img)/norm
        state = list(tops) + list(bottoms)
        state.append(top_trend)
        state.append(bottom_trend)
        state.append(slope)
        state.append(y_cur_price)
        state.append(self.position)
        state.append(self.profit_dir)
        return tuple(state)
        
    def _calc_profit(self,direction):
        if direction == 1:
            self.profit = ((self.df.iloc[self.step]['price']/self.price_pos)-1) * 100
        elif direction == -1:
            self.profit = (1 - (self.df.iloc[self.step]['price']/self.price_pos)) * 100
        else:
            self.profit = 0
    def _change_pos(self,direction):
        self._calc_profit(direction)
        self.profit -= 0.1
        self.global_profit += self.profit
    def _get_reward_profit(self,reward):
        if self.profit > 0:
            return reward + self.profit
        else:
            return reward + self.profit * 0.1
        
    def _get_profit_dir(self):
        self._calc_profit(self.position)
        if self.profit > 0.05:
            self.profit_dir = 1
        elif self.profit < -0.05:
            self.profit_dir = -1
        else:
            self.profit_dir = 0
# DataForLearning\9.07.24\images\MRKV1720516447.2800508.png
    def change_pos(self,delta_pos):
        reward = -0.1
        if self.position == delta_pos:
            self._calc_profit(self.position)
            return self._get_reward_profit(reward)
        if delta_pos == 0:
            if self.position == 1:
                self._change_pos(1)
            else:
                self._change_pos(-1)
            self.price_pos = 0
            self.position = delta_pos
            return self._get_reward_profit(reward)
        if delta_pos == 1:
            if self.position == -1:
                self._change_pos(1)
            self.price_pos = self.df.iloc[self.step]['price']
            self.position = delta_pos
            # reward += 0.5
            return self._get_reward_profit(reward)
        if delta_pos == -1:
            if self.position == 1:
                self._change_pos(-1)
            self.price_pos = self.df.iloc[self.step]['price']
            self.position = delta_pos
            return self._get_reward_profit(reward)

            
        # if abs(self.position+delta_pos) > 1:
        #     return 0
        # else:
        #     prev_pos = self.position
        #     self.position += delta_pos
        #     if delta_pos == 0:
        #         return 0
        #     else:
        #         if self.position == 0:
        #             reward = 0
        #             if prev_pos == -1:
        #                 self.profit = round(((1 - (self.df.iloc[self.step]['price']/self.price_pos)) * 100),2)
        #                 reward += 0.01
        #             if prev_pos == 1:
        #                 self.profit = round((((self.df.iloc[self.step]['price']/self.price_pos)-1) * 100),2)
        #                 reward += 0.01
        #             self.profit -= 0.05
        #             self.global_profit += self.profit
        #             self.price_pos = 0
        #             return 0
        #         else:
        #             self.price_pos = self.df.iloc[self.step]['price']
        #             self.profit -= 0.05
        #             return 0
    def _convert_action(self,action):
        if np.array_equal(action, [1, 0, 0]):
            delta_pos = 0
        if np.array_equal(action, [0, 1, 0]):
            delta_pos = 1
        if np.array_equal(action, [0, 0, 1]):
            delta_pos = -1
        return delta_pos
    def make_step(self,action):
        delta_pos = self._convert_action(action)
        reward = self.change_pos(delta_pos)
        # if self.position == -1:
        #     self.profit = round(((1 - (self.df.iloc[self.step]['price']/self.price_pos)) * 100),2)
        # if self.position == 1:
        #     self.profit = round((((self.df.iloc[self.step]['price']/self.price_pos)-1) * 100),2)
        # if self.profit > 0:
        #     reward += self.profit
        self.count_pos += abs(delta_pos)
        self.step += 1
        
        done = True
        if self.step < self.limit:
            done = False            
        else:
            self._change_pos(self.position)
            reward = self._get_reward_profit(reward)
        self.profit = 0
        return reward, done, round(self.global_profit,2)
    
    def test(self,action):
        delta_pos = self._convert_action(action)
        reward = self.change_pos(delta_pos)
        cv2.putText(self.img, str(self.position), (30, 30) , cv2.FONT_HERSHEY_SIMPLEX,  
                   1, (255, 255, 255), 3, cv2.LINE_AA)
        model_folder_path = './test/imgs/'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        img_name = model_folder_path + self.name + self.day + 's'+ str(self.step) +'.png'
        cv2.imwrite(img_name,self.img)
        self.step += 1
        if self.step >= self.limit:
            self.reset()

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


