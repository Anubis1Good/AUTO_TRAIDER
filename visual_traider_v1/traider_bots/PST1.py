from traider_bots.VisualTraider_v2 import VisualTraider_v2
from utils.chart_utils.ProSveT import ProSveT
from utils.chart_utils.indicators import check_zona
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
        pst = ProSveT(half_bars)
        pst.draw_all(chart)
        sell_zona = check_zona(pst.sell_zona,half_bars)
        buy_zona = check_zona(pst.buy_zona,half_bars)
        cur_price = self._get_current_price(chart)
        return {
            'cur_price':cur_price,
            'sell_zona':sell_zona,
            'buy_zona':buy_zona,
        }    
    
    def _get_direction(self,keys):
        if keys['buy_zona']:
            return 'long'
        if keys['sell_zona']:
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