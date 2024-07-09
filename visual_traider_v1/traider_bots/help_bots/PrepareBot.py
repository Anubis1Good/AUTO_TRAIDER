from traider_bots.VisualTraider import VisualTraider
from utils.prepare_utils.saves import save_img

class PrepareBot(VisualTraider):
    def __init__(self, glass_region: tuple, chart_region: tuple, name: str = 'none') -> None:
        super().__init__(glass_region, chart_region, name)
        self.traider_name = 'PrepareBot'
        self.MainState = save_img
        self.current_state = self.MainState

    def test(self,img):
        chart = self.get_chart(img)
        self.MainState(chart,self.name)
    # save img to learn_data/images
    # save points to learn_data/points
    # save trends to learn_data/trends