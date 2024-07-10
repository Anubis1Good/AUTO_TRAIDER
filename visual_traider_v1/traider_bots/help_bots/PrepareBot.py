from traider_bots.VisualTraider import VisualTraider
from utils.conditions import get_current_level
from utils.prepare_utils.saves import save_arraylike,save_points
import cv2

class PrepareBot(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple, name: str = 'none') -> None:
        super().__init__(glass_region, chart_region, name)
        self.traider_name = 'PrepareBot'
        self.MainState = save_arraylike
        self.current_state = self.MainState

    def test(self,img):
        chart = self.get_chart(img)
        y_cur_price = get_current_level(chart,(0,0,chart.shape[1],chart.shape[0]))
        self.MainState(chart,self.name)
        save_points(chart,self.name,y_cur_price)
    # save img to learn_data/images
    # save points to learn_data/points
    # save trends to learn_data/trends