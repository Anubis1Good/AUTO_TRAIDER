from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.ProSveT import ProSveT
class PST1(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
    
    def _get_keys(self, img, region) -> dict:
        chart = self._get_chart(img,region)
        candle_mask = self._get_candle_mask(chart)
        volume_mask = self._get_volume_mask(chart)
        candle_cords = self._get_cords_on_mask(candle_mask)
        volume_cords = self._get_cords_on_mask(volume_mask)
        half_bars = self._get_half_bars(candle_mask,candle_cords,volume_cords)
        prosvet = ProSveT(half_bars)
        prosvet.draw_all(chart)
        ices = prosvet.ices
        creeks = prosvet.creeks
        buffer = abs(ices[-2][1] - creeks[-2][1]) // 10
        cur_price = self._get_current_price(chart)
        return {
            'ices':ices,
            'creeks':creeks,
            'buffer':buffer,
            'cur_price':cur_price
        }    
    
    def _get_direction(self,keys):
        last_creek = keys['creeks'][-2][1]
        last_ice = keys['ices'][-2][1]
        cur_price = keys['cur_price'][1]
        buffer = keys['buffer']
        if abs(cur_price - last_ice) < buffer:
            return 'long'
        if abs(cur_price - last_creek) < buffer:
            return 'short'
        
    def _test(self, img):
        m_keys = self._get_keys(img,self.minute_chart_region)
        direction = self._get_direction(m_keys)
        if direction == 'long':
            self._test_send_close(img,'short')
            self._test_send_open(img,'long') 
        if direction == 'short':
            self._test_send_close(img,'long')
            self._test_send_open(img,'short')
        
        
    
    def _traide(self, img):
        return super()._traide(img)