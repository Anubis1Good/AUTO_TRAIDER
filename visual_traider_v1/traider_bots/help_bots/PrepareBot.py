import cv2
from time import time
import os
from traider_bots.VisualTraider_v2 import VisualTraider_v2


class PrepareBot(VisualTraider_v2):
    def __init__(self, cluster: tuple, dealfeed: tuple, glass: tuple, day: tuple, hour: tuple, minute: tuple, position: tuple, name: str, mode: int = 0) -> None:
        super().__init__(cluster, dealfeed, glass, day, hour, minute, position, name, mode)
        self.traider_name = 'PrepareBot'
        self.save_dir = './learn_data/images'
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def run(self,img):
        name = f'{self.save_dir}_{self.name}_{time()}.png'
        cv2.imwrite(name,img)
