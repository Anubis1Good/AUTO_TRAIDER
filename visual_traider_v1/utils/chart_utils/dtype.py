import numpy as np
class HalfBar:
    def __init__(self,x,yh,yl,yv) -> None:
        self.x = x
        self.yh = yh
        self.yl = yl
        self.yv = yv
        self.ym = (self.yh + self.yl)//2
        self.hpt = (self.x,self.yh)
        self.lpt = (self.x,self.yl)
        self.mpt = (self.x,self.ym)
        self.vpt = (self.x,self.yv)
        self.spred = yl - yh
        buff = self.spred//4
        self.pred_yh = self.yh + buff
        self.pred_yl = self.yl - buff
        self.pred_hp = (self.x,self.pred_yh)
        self.pred_lp = (self.x,self.pred_yl)
        self.vsai = int((self.spred / (10000 - self.yv))*10000)
        self.vsaipt = (self.x,self.vsai)
        self.draw_line = np.array([self.hpt,self.lpt])
    
    def __repr__(self) -> str:
        return f'HalfBar x: {self.x} y_high: {self.yh}'
    
    def is_big_volume(self,mean):
        return self.yv < mean

    def to_img_cords(self,func):
        hpt = func(self.hpt)
        lpt = func(self.lpt)
        vpt = func(self.vpt)
        return hpt,lpt,vpt
    
class FullBar(HalfBar):
    def __init__(self, x, yh, yl, yv, yo ,yc,direction) -> None:
        super().__init__(x, yh, yl, yv)
        self.yo = yo
        self.yc = yc
        self.direction = direction