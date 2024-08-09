import cv2
import os
import numpy as np
import numpy.typing as npt
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_bollinger_bands, get_zona, get_SMA, get_dynamics
class ST3(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'ST1'
        self.i = 0
        self.close_long = False
        self.close_short = False

    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        mpts = []
        vpts = []
        for i in range(len(half_bars)):
            mpt = half_bars[i].mpt
            vpt = half_bars[i].vpt
            mpts.append(mpt)
            vpts.append(vpt)
        vpts = np.array(vpts)
        v_sma = get_SMA(vpts,20)
        cur_price = self._get_current_price(chart)
        zona,m_pt_zona = get_zona(half_bars,cur_price,vpts,v_sma)
        sma_sm,bbu_sm,bbd_sm = get_bollinger_bands(np.array(mpts))
        sma_lr,bbu_lr,bbd_lr = get_bollinger_bands(np.array(mpts),k=1,step=40)
        dynamics_sm = round(get_dynamics(sma_sm)/10,2)
        dynamics_lr = round(get_dynamics(sma_lr,20)/20,2)
        dynamics_lr_all = round(get_dynamics(sma_lr,len(sma_lr)-1)/(len(sma_lr)-1),2)
        last_pick = self._get_last_pick(half_bars,bbu_sm,bbd_sm,20)
        # new_experimental
        buffer = chart.shape[0]//4
        end = chart.shape[1]-10
        top_line = 0 + buffer
        bottom_line = chart.shape[0] - buffer

        keys = {
            'cur_price':cur_price,
            'zona':zona,
            'm_pt_zona':m_pt_zona,
            'sma_sm':sma_sm,
            'bbu_sm':bbu_sm,
            'bbd_sm':bbd_sm,
            'sma_lr':sma_lr,
            'bbu_lr':bbu_lr,
            'bbd_lr':bbd_lr,
            'dynamics_sm':dynamics_sm,
            'dynamics_lr':dynamics_lr,
            'dynamics_lr_all':dynamics_lr_all,
            'last_hb':half_bars[-2],
            'last_pick':last_pick,
            'top_line':top_line,
            'bottom_line': bottom_line
        }
        lock = self._check_lock(keys)
        wave = self._get_wave(keys)
        if self.mode != 1:
            cv2.polylines(chart,[sma_sm],False,(200,0,0),1)
            cv2.polylines(chart,[bbu_sm],False,(200,200,0),1)
            cv2.polylines(chart,[bbd_sm],False,(200,0,200),1)
            cv2.polylines(chart,[sma_lr],False,(100,0,0),2)
            cv2.polylines(chart,[bbu_lr],False,(100,200,0),2)
            cv2.polylines(chart,[bbd_lr],False,(100,0,200),2)
            cv2.polylines(chart,[v_sma],False,(230,100,100),1)
            cv2.putText(chart,'Lock: '+str(lock),(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(20,255,255),3)
            cv2.putText(chart,"DSM: " +str(dynamics_sm),(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),1)
            cv2.putText(chart,"DLR: "+str(dynamics_lr),(0,70),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
            cv2.putText(chart,"DLRa: "+str(dynamics_lr_all),(0,90),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,205,155),2)
            cv2.putText(chart,"Wave: "+str(wave),(0,110),cv2.FONT_HERSHEY_SIMPLEX,0.8,(155,205,155),2)
            cv2.line(chart,(0,top_line),(end,top_line),(100,50,200),2)
            cv2.line(chart,(0,bottom_line),(end,bottom_line),(100,250,20),2)
        return keys
       
    def _get_last_pick(self,half_bars,bbu,bbd,step_sma):
        for i in range(len(half_bars)-1,0,-1):
            if half_bars[i].y_in_bar(bbu[i-step_sma][1]):
                return 1
            if half_bars[i].y_in_bar(bbd[i-step_sma][1]):
                return -1
            
            

    
    def _get_wave(self,keys):
        lock = self._check_lock(keys)
        lock_lr = self._check_lock(keys,'lr')
        if keys['zona']:
            if keys['dynamics_sm'] > 1:
                if keys['cur_price'][1] < keys['bbd_lr'][-1][1]:
                    if keys['dynamics_lr'] > 1 and keys['dynamics_lr_all'] > 1:
                        return 'short'
                    else:
                        return 'close_long'
                if lock == -1 and keys['top_line'] < keys['cur_price'][1]:
                    return 'close_short'
            if lock == -1 and keys['top_line'] < keys['cur_price'][1]:
                return 'close_short'
            if keys['dynamics_sm'] < -1:
                if keys['cur_price'][1] > keys['bbu_lr'][-1][1]:
                    if keys['dynamics_lr'] < -1 and keys['dynamics_lr_all'] < -1:
                        return 'long'
                    else:
                        return 'close_short'
                if lock == 1 and keys['bottom_line'] > keys['cur_price'][1]:
                    return 'close_long'
            if lock == 1 and keys['bottom_line'] > keys['cur_price'][1]:
                return 'close_long'
        if 1 > keys['dynamics_lr_all'] > -1:
            if keys['bbd_lr'][-1][1] < keys['cur_price'][1] > keys['bbd_sm'][-1][1] and keys['bottom_line'] < keys['cur_price'][1]:
                return 'long'
            if keys['bbu_lr'][-1][1] > keys['cur_price'][1] < keys['bbu_sm'][-1][1] and keys['top_line'] > keys['cur_price'][1]:
                return 'short'
        if lock_lr == -1 and  keys['dynamics_lr'] > 0.4 and keys['bottom_line'] > keys['cur_price'][1]:
            return 'close_long'
        if lock_lr == 1 and keys['dynamics_lr'] < -0.4 and keys['top_line'] < keys['cur_price'][1]:
            return 'close_short'
            # else:
            #     if keys['cur_price'][1] < keys['sma_lr'][-1][1]:
            #         if lock == 1:
            #             return 'short'
            #     if keys['cur_price'][1] > keys['sma_lr'][-1][1]:
            #         if lock == -1:
            #             return 'long'
                

    def _check_lock(self,keys,bb:str='sm'):
        if keys['cur_price'][1] >= keys['bbd_'+bb][-1][1] <= keys['last_hb'].yl:
            return -1
        if keys['cur_price'][1] <= keys['bbu_'+bb][-1][1] >= keys['last_hb'].yh:
            return 1
        return 0 
        

    def _test(self, img):
        m_keys = self._get_keys(img,self.minute_chart_region)
        wave = self._get_wave(m_keys)
        # self.i+=1
        # cv2.imwrite('./test_images/'+self.name+str(self.i)+'.png',img)
        if wave == 'long':
            self._test_send_close(img,'short')
            self._test_send_open(img,'long') 
        if wave == 'close_long':
            self._test_send_close(img,'long')
        if wave == 'short':
            self._test_send_close(img,'long')
            self._test_send_open(img,'short')
        if wave == 'close_short':
            self._test_send_close(img,'short')

    def _traide(self, img):
        pos = self._check_position(img)
        m_keys = self._get_keys(img,self.minute_chart_region)
        wave = self._get_wave(m_keys)
        if wave:
            if wave == 'long':
                if pos == -1:
                    self.close_short = True
                    self._reverse_pos(img,'long')
                if pos == 0:
                    self._send_open('long')
            if wave == 'close_long':
                if pos == 1:
                    self.close_long = True
                    self._send_close(img,'long')
            if wave == 'short':
                if pos == 1:
                    self.close_long = True
                    self._reverse_pos(img,'short')
                if pos == 0:
                    self._send_open('short')
            if wave == 'close_short':
                if pos == -1:
                    self.close_short = True
                    self._send_close(img,'short')
        elif self.close_long:
            if pos == 1:
                self._send_close(img,'long')
            else:
                self.close_long = False
        elif self.close_short:
            if pos == -1:
                self._send_close(img,'short')
            else:
                self.close_long = False
        else:
            self._reset_req()

# TODO
# Подумать над решением проблемы '30.07.24d', когда были сильные движения в разные стороны