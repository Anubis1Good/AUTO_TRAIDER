import pandas as pd
import cv2

def draw_df_dc(row,chart,colors=((250,100,140),(150,150,240))):
    cv2.circle(chart,(row['x'],row['up_dc']),1,colors[0],-1)
    cv2.circle(chart,(row['x'],row['down_dc']),1,colors[0],-1)
    cv2.circle(chart,(row['x'],row['middle_dc']),1,colors[1],-1)