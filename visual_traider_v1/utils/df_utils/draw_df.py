import pandas as pd
import cv2
import numpy as np

def draw_df_dc(row,chart,colors=((250,100,140),(150,150,240))):
    cv2.circle(chart,(row['x'],row['up_dc']),1,colors[0],-1)
    cv2.circle(chart,(row['x'],row['down_dc']),1,colors[0],-1)
    cv2.circle(chart,(row['x'],row['middle_dc']),1,colors[1],-1)

def draw_df_DC(row,chart,colors=((250,100,140),(150,150,240))):
    cv2.circle(chart,(row['x'],row['max_hb']),1,colors[0],-1)
    cv2.circle(chart,(row['x'],row['min_hb']),1,colors[0],-1)
    cv2.circle(chart,(row['x'],row['avarege']),1,colors[1],-1)

def draw_df_DC_polyline(df:pd.DataFrame,chart,colors=((250,100,140),(150,150,240))):
    x = df['x'].to_numpy().reshape(-1, 1) 
    # print(np.hstack((x,df['max_hb'].to_numpy().reshape(-1, 1) )))
    cv2.polylines(chart,[np.hstack((x,df['max_hb'].to_numpy().reshape(-1, 1) ))],False,colors[0],1)
    cv2.polylines(chart,[np.hstack((x,df['min_hb'].to_numpy().reshape(-1, 1) ))],False,colors[0],1)
    cv2.polylines(chart,[np.hstack((x,df['avarege'].to_numpy().reshape(-1, 1) ))],False,colors[1],1)

def draw_df_VC_polyline(df:pd.DataFrame,chart,colors=((250,100,140),(150,150,240))):
    x = df['x'].to_numpy().reshape(-1, 1) 
    cv2.polylines(chart,[np.hstack((x,df['top_mean'].to_numpy().reshape(-1, 1) ))],False,colors[0],1)
    cv2.polylines(chart,[np.hstack((x,df['bottom_mean'].to_numpy().reshape(-1, 1) ))],False,colors[0],1)
    cv2.polylines(chart,[np.hstack((x,df['avarege_mean'].to_numpy().reshape(-1, 1) ))],False,colors[1],1)

def draw_df_BB_polyline(df:pd.DataFrame,chart,colors=((250,100,140),(150,150,240))):
    x = df['x'].to_numpy().reshape(-1, 1) 
    cv2.polylines(chart,[np.hstack((x,df['bbu'].to_numpy().reshape(-1, 1) ))],False,colors[0],1)
    cv2.polylines(chart,[np.hstack((x,df['bbd'].to_numpy().reshape(-1, 1) ))],False,colors[0],1)
    cv2.polylines(chart,[np.hstack((x,df['sma'].to_numpy().reshape(-1, 1) ))],False,colors[1],1)

def draw_rsi(df:pd.DataFrame,chart,color=(100,200,100)):
    cv2.line(chart,(df.iloc[0]['x'],30),(df.iloc[-1]['x'],30),color,2)
    cv2.line(chart,(df.iloc[0]['x'],70),(df.iloc[-1]['x'],70),color,2)
    x = df['x'].to_numpy().reshape(-1, 1) 
    cv2.polylines(chart,[np.hstack((x,df['rsi'].to_numpy().reshape(-1, 1) ))],False,color,1)

def draw_df_chart(row,chart):
    clr = (100,0,255) if row['direction'] == -1 else (100,255,0)
    cv2.line(chart,(row['x'],row['high']),(row['x'],row['low']),clr,1)