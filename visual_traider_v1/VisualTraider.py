'''
1. Проверка наличия позиции -> Need_close
2. Проверка наличия заявки на закрытие позиции -> Has_close
3. Проверка наличия заявки на открытие позиции -> Has_bid
4. Иначе -> Send_bid
'''
import pyautogui as pag
import operations as o
from State import State
from conditions import check_pos, check_bid
class VisualTraider():
    def __init__(self,left,top,right,bottom) -> None:
        self.region = (left,top,right,bottom)
        self.Send_bid = State(o.send_bid)
        self.Has_bid = State(o.has_bid)
        self.Has_close = State(o.has_close)
        self.Need_close = State(o.need_close)
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

        
        self.current_state.do_operation(self.region)
        pag.PAUSE

# test1 = VisualTraider(324,49,960,1055)
# test2 = VisualTraider(1280,48,1916,1058)
# while True:
#     for i in range(30):
#         test1.run()
#         test2.run()
#     pag.press('space')
#     print('space')

