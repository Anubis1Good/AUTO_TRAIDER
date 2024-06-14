from traider_bots.LRTraider import LRTraider as Traider

def configurtion_traiders():
    traiders = []
    with open('config.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('-')
            glass = tuple(map(int,line[0].split(',')))
            chart = tuple(map(int,line[1].split(',')))
            traiders.append(Traider(glass,chart))
    return traiders


