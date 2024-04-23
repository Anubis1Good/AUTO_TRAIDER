import pyautogui as pag
from traid_utils import click_bid, reset_bid, click_ask, reset_ask, click_ask
from conditions import check_pos, check_bid
class VisualTraider():
    def __init__(self,left,top,right,bottom) -> None:
        self.region = (left,top,right,bottom)
        self.Send_bid = click_ask
        self.Has_bid = reset_ask
        self.Has_close = reset_bid
        self.Need_close = click_bid
        self.current_state = self.Send_bid

    def run(self):
        
        pag.press('shift')
        pos = check_pos(self.region)
        bid = check_bid(self.region)

        if pos:
            if bid:
                self.current_state = self.Has_close
            else: 
                self.current_state = self.Need_close
        else:
            if bid:
                self.current_state = self.Has_bid
            else:
                self.current_state = self.Send_bid    
  
  
        self.current_state(self.region)
        pag.PAUSE
        print(self.current_state)
     
# test1 = VisualTraider(0,0,1990,1058)

# while True:
#     for i in range(30): 
#         test1.run()
         
#     pag.press('space')


 