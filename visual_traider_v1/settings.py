
# for VisualTraider before v2
def configurtion_traiders(Traider,filename):
    traiders = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('-')
            glass = tuple(map(int,line[0].split(',')))
            chart = tuple(map(int,line[1].split(',')))
            traiders.append(Traider(glass,chart))
    return traiders

def configuration_traiders_v2(filename:str):
    fields = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            field = tuple(map(int,line.split(',')))
            fields.append(field)
    return fields
    
if __name__ == '__main__':
    print(configuration_traiders_v2('./config_dev.txt'))
