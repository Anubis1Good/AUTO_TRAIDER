# from traider_bots.PT2ov1 import PT2ov
# from traider_bots.PST1 import PST1 
# from traider_bots.PT1 import PT1 
# from traider_bots.ST4 import ST4
# from traider_bots.archive.ST6 import ST6
# from traider_bots.archive.ST1 import ST1,ST1a
# from traider_bots.VisualTraider_v3 import VisualTraider_v3 
# from tas.PTA2_DDC import PTA2_DDC,PTA2a_DDC
# from tas.SleepTA import SleepTA
from sgs.sg_on_bot import *
from traider_bots.AllBots import *

def init_trader(ticker,param_bots):
    bot_name = ''
    for bot in bot_on_ticker:
        if ticker in bot:
            bot_name = bot_on_ticker
    if bot_name in VT2_bots:
        return VT2_bots[bot_name](*param_bots,ticker,mode=1)
    trader = VisualTraider_v3(*param_bots,ticker,mode=1)
    if bot_name in VT3_bots:
        trader.TA = VT3_bots[bot_name][0](trader,*VT3_bots[bot_name][1])
    else:
        trader.TA = SleepTA(trader)
    return trader

def init_test(bot_name,param_bots,ticker):
    if bot_name in VT2_bots:
        return VT2_bots[bot_name](*param_bots,ticker)
    trader = VisualTraider_v3(*param_bots,ticker)
    if bot_name in VT3_bots:
        trader.TA = VT3_bots[bot_name][0](trader,*VT3_bots[bot_name][1])
    else:
        trader.TA = SleepTA(trader)
    return trader
