from sgs.sg_on_bot import *
from traider_bots.AllBots import *

def init_trader(ticker,param_bots):
    bot_name = ''
    for bot in bot_on_ticker:
        if ticker in bot_on_ticker[bot]:
            bot_name = bot
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

def init_fast_test(bot_name,param_bots,ticker):
    if bot_name in VT2_bots:
        return VT2_bots[bot_name](*param_bots,ticker,mode=4)
    trader = VisualTraider_v3(*param_bots,ticker,mode=4)
    if bot_name in VT3_bots:
        trader.TA = VT3_bots[bot_name][0](trader,*VT3_bots[bot_name][1])
    else:
        trader.TA = SleepTA(trader)
    return trader
