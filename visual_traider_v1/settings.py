# from pprint import pprint
# from traider_bots.Begginer2 import Begginer2
from traider_bots.SimpleTrander import SimpleTraider
def configurtion_traiders():
    traiders = []
    with open('config.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('-')
            glass = tuple(map(int,line[0].split(',')))
            chart = tuple(map(int,line[1].split(',')))
            traiders.append(SimpleTraider(glass,chart))
    return traiders


# pprint(configurtion_traiders())