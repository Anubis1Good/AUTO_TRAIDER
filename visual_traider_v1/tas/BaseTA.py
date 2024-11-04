from dataclasses import dataclass

@dataclass
class Keys:
    price:int

class BaseTA:
    def __init__(self,trader):
        self.trader = trader
    def get_keys(self,img, region) -> Keys:
        return Keys(1000)
    def get_action(self):
        pass