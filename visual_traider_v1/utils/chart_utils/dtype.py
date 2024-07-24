class HalfBar:
    def __init__(self,x,yh,yl,yv) -> None:
        self.x = x
        self.yh = yh
        self.yl = yl
        self.yv = yv
        self.hpt = (self.x,self.yh)
        self.lpt = (self.x,self.yl)
        self.mpt = (self.x,(self.yh + self.yl)//2)
        self.vpt = (self.x,self.yv)
    
    def __repr__(self) -> str:
        return f'HalfBar x: {self.x} y_high: {self.yh}'
    
    def is_big_volume(self,mean):
        return self.yv < mean

    def to_img_cords(self,func):
        hpt = func(self.hpt)
        lpt = func(self.lpt)
        vpt = func(self.vpt)
        return hpt,lpt,vpt
    
