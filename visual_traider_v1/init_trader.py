from traider_bots.PT2ov1 import PT2ov
from traider_bots.PST1 import PST1 
from traider_bots.PT1 import PT1 
from traider_bots.ST4 import ST4
from traider_bots.archive.ST6 import ST6
from traider_bots.VisualTraider_v3 import VisualTraider_v3 
from tas.PTA2_DDC import PTA2_DDC
from tas.SleepTA import SleepTA
from sgs.sg_on_bot import *

def init_trader(stock_groups,i,param_bots):
    if stock_groups[i] in PTA2_DDC_15_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,15)
    elif stock_groups[i] in PTA2_DDC_20_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,20)
    elif stock_groups[i] in PTA2_DDC_30_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,30)
    elif stock_groups[i] in PTA2_DDC_40_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,40)
    elif stock_groups[i] in PTA2_DDC_60_group:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = PTA2_DDC(traider,60)
    elif stock_groups[i] in PT1_group:
        traider = PT1(*param_bots,name=stock_groups[i],mode=1)
    elif stock_groups[i] in PST1_group:
        traider = PST1(*param_bots,name=stock_groups[i],mode=1)
    elif stock_groups[i] in PT2ov_group:
        traider = PT2ov(*param_bots,name=stock_groups[i],mode=1)
    elif stock_groups[i] in ST4_group:
        traider = ST4(*param_bots,name=stock_groups[i],mode=1)
    elif stock_groups[i] in ST6_group:
        traider = ST6(*param_bots,name=stock_groups[i],mode=1)
    else:
        traider = VisualTraider_v3(*param_bots,name=stock_groups[i],mode=1)
        traider.TA = SleepTA(traider)
    return traider