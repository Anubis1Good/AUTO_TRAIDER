from utils.traid_utils import not_idea

class VisualTraider():
    def __init__(self,glass_region:tuple,chart_region:tuple,name:str='none') -> None:
        self.region_glass = (
            glass_region[0],
            glass_region[1],
            glass_region[2],
            glass_region[3]-25
            )
        self.region_pos = (
            glass_region[0],
            glass_region[3]-25,
            glass_region[2],
            glass_region[3]
            )
        self.region_chart = chart_region
        self.Not_idea = not_idea
        self.current_state = self.Not_idea
        self.name = name
        self.traider_name = 'VisualTraider'
    
    def __repr__(self):
        return f'{self.name}: glass - {self.region_glass}, chart - {self.region_chart}'

    def run(self,img):         
        self.current_state(img,self.region_glass)

    def test(self,img):
        print(f'{self.name} test')
        



 