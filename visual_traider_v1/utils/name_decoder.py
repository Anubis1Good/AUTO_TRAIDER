names = {
    'MXI':('MMM5',True),
    'CNY':('CRM5',True),
    'GAZR':('GZM5',True),
    'SBRF':('SRM5',True),
}

def decoder_name(name):
    'return ticker,board,market,engine'
    if name in names:
        ticker = names[name][0]
        fut = names[name][1]
    else:
        ticker = name
        fut = False
    if fut:
        board = "RFUD"
        market = "forts"
        engine= "futures"
    else:
        board = "TQBR"
        market: str = "shares"
        engine: str = "stock"
    return ticker,board,market,engine