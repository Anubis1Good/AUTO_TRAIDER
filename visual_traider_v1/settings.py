from VisualTraider import VisualTraider
def configurtion_traiders():
    traiders = []
    with open('config.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            line = tuple(map(int,line.split(',')))
            traiders.append(VisualTraider(line[0], line[1], line[2], line[3],line[4]))
    return traiders


