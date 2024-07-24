import cv2
import numpy as np
from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.indicators import get_SMA, get_bollinger_bands
class WorkBot(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'WorkBot'

    
    def draw_all(self,img,region):
        change_cords = lambda p: self._change_coords(p,region)
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)

        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        colors = (
            (100,200,0),
            (0,200,100),
            (200,0,100)
        )
        mean_volume = self._get_mean(volume_cords)
        vpts = []
        mpts = []
        # lpts = []
        # hpts = []
        for i in range(len(half_bars)):
            hpt,lpt,vpt = half_bars[i].to_img_cords(change_cords)
            mpt = change_cords(half_bars[i].mpt)
            mpts.append(mpt)
            vpts.append(vpt)
            # lpts.append(lpt)
            # hpts.append(hpt)
            if half_bars[i].is_big_volume(mean_volume[1]): 
                cv2.circle(img,vpt,1,(0,200,0))
                cv2.line(img,hpt,lpt,colors[1],1)
        period = 27
        V_sma = get_SMA(np.array(vpts),period)
        # m_sma = get_SMA(np.array(mpts),period)
        m_sma,bbu,bbd = get_bollinger_bands(np.array(mpts))
        # print(m_sma[0])
        # print(bbu[0])
        # l_sma = get_SMA(np.array(lpts),period)
        # h_sma = get_SMA(np.array(hpts),period)
        cv2.polylines(img,[V_sma],False,(176,80,10),2)
        cv2.polylines(img,[m_sma],False,(176,180,10),1)
        cv2.polylines(img,[bbu],False,(176,80,90),2)
        cv2.polylines(img,[bbd],False,(176,80,90),2)
        # cv2.polylines(img,[l_sma],False,(176,180,10),2)
        # cv2.polylines(img,[h_sma],False,(176,80,110),2)
        mean_volume = change_cords(mean_volume)
        cv2.circle(img,mean_volume,1,(150,200,70),3)
        points = self._get_points(half_bars)
        for i in range(points.shape[0]):
            points[i] = change_cords(points[i])
        x,y = self._get_xy(points)
        trend,top_trend,bottom_trend = self._get_trend_lines(x,y)
        cv2.polylines(img,[trend],False,(255,255,255),2)
        cv2.polylines(img,[top_trend],False,(255,255,255),2)
        cv2.polylines(img,[bottom_trend],False,(255,255,255),2)
        # max_volume,min_volume = self._get_limit(volume_cords)
        # min_volume = change_cords(min_volume)
        # max_volume = change_cords(max_volume)
        # cv2.circle(img,min_volume,1,(250,0,0),3)
        # cv2.circle(img,max_volume,1,(200,100,0),3)
        # candle_mask = get_candle_mask(chart)
        # volume_mask = get_volume_mask(chart)
        # res_top = cv2.matchTemplate(candle_mask,TemplateCandle.candle_top,cv2.TM_CCOEFF_NORMED)
        # res_top = np.argwhere(res_top >= 0.9)
        # res_top = res_top[res_top[:, 1].argsort()]

        # volume_cords = get_cords_on_mask(volume_mask)
        # candle_cords = get_cords_on_mask(candle_mask)

        # mean_volume,max_volume = get_statistic_volume(volume_cords)
        # candle_corners = get_corners(candle_mask)
        # print(candle_cords[:5])
        # print(volume_cords[:5])
        # print('-----')
        # candle_cords = candle_cords[candle_cords[:,1].argsort()]
        # volume_cords = volume_cords[volume_cords[:,1].argsort()]
        # print(candle_cords[:5])
        # print(volume_cords[:5])
        # print('======')
        # vol = volume_cords[-1]
        # vol = (vol[1],vol[0])
        # vol = change_cords(vol)
        # cv2.circle(img,vol,2,(240,100,10),2)
        # vol = candle_cords[-1]
        # vol = (vol[1],vol[0])
        # vol = change_cords(vol)
        # cv2.circle(img,vol,2,(140,100,100),2)

        # vol = volume_cords[-1]
        # vol = (vol[1],vol[0])
        # vol = change_cords(vol)
        # print(vol)
        # for i in range(candle_corners.shape[0]):
        #     candle_corners[i] = change_cords(candle_corners[i])
        #     cv2.circle(img,candle_corners[i],1,(0,200,0))
        # print(res_top[i][0])
        # print(candle_cords.shape)
        # candle_cords = candle_cords[candle_cords[:, 1].argsort()]
        # print(candle_cords[:10],'!')

        # half_bars:list[HalfBar] = []
        # for i in range(res_top.shape[0]):
        #     res_top[i] = (res_top[i][0],res_top[i][1]+1)
        #     point_b = candle_cords[np.where(candle_cords[:,1] == res_top[i][1])]
        #     point_v = volume_cords[np.where(volume_cords[:,1] == res_top[i][1])]
        #     y_b = point_b[:,0].max()
        #     y_v = point_v[:,0].min()
        #     half_bars.append(HalfBar(res_top[i][1],res_top[i][0],y_b,y_v))

        # hb = half_bars[-1]
        # break
        



        # print(half_bars)
        # for i in range(res_bottom.shape[0]):
        #     res_bottom[i] = (res_bottom[i][1],res_bottom[i][0])
        #     res_bottom[i] = change_cords(res_bottom[i])
        #     pt = (res_bottom[i][0]+1,res_bottom[i][1]-1)
        #     cv2.circle(img,pt,1,(170,100,170))
        # for i in range(res_vol.shape[0]):
        #     res_vol[i] = (res_vol[i][1],res_vol[i][0])
        #     res_vol[i] = change_cords(res_vol[i])
        #     pt = (res_vol[i][0]+1,res_vol[i][1]+1)
        #     cv2.circle(img,pt,1,(170,150,170))
        # divide_regions = get_divide_chart(candle_corners)
        # for dr in divide_regions:
        #     cv2.rectangle(img,(dr[0],dr[1]),(dr[2],dr[3]),(200,200,100),2)
        # # candle_corners = self._change_coords(candle_corners,region)
        # x,y = get_xy(candle_corners)
        # draw_trendlines_v2(x,y,img)
        
    def _test(self, img):
        self.draw_all(img,self.day_chart_region)
        self.draw_all(img,self.hour_chart_region)
        self.draw_all(img,self.minute_chart_region)
        cv2.imwrite('test.png',img)

