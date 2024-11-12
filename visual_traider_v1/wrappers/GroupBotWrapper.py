from utils.test_utils.windows import draw_borders
# from traider_bots.VisualTraider_v2 import VisualTraider_v2

class GroupBotWrapper:
    def __init__(self,trader_type,trader_names:list[str],top:int,width:int,top_chart:int,width_glass:int,top_pos:int,bottom_pos:int,bottom:int,cluster_width:int,mode:int=0,tas=lambda t:None,fast_close=False) -> None:
        self.traders = []
        width_trader = width//len(trader_names)
        for i in range(len(trader_names)):
            trader = trader_type(
                (width_trader*i,top,width_trader*i+cluster_width,top_pos),
                (width_trader*i+cluster_width,top,width_trader*(i+1)-width_glass,top_pos),
                (width_trader*(i+1)-width_glass,top,width_trader*(i+1),top_pos),
                (width_trader*i,top_chart,width_trader*(i+1),bottom),
                (width_trader*i,top_chart,width_trader*(i+1),bottom),
                (width_trader*i,top_chart,width_trader*(i+1),bottom),
                (width_trader*i,top_pos,width_trader*(i+1),bottom_pos),
                name=trader_names[i],
                mode=mode,
                fast_close=fast_close
            )
            trader.TA = tas(trader)
            self.traders.append(trader)

    def run(self,img):
        for trader in self.traders:
            trader.run(img)

    def draw_borders(self,img):
        for trader in self.traders:
            draw_borders(img,trader) 