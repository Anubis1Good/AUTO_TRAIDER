from dataclasses import dataclass

@dataclass
class Keys:
    cur_price:int

class BaseTA:
    def __init__(self,trader):
        self.trader = trader
    def get_keys(self,img) -> Keys:
        return Keys(1000)
    def get_action(self,keys):
        pass
    def __call__(self, img):
        keys = self.get_keys(img)
        action = self.get_action(keys)
        return action,keys