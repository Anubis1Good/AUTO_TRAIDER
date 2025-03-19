from from_rich_laughter.work_strategies import PTA4_WDDCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDVCr,OGTA4_DOG,LTA_KROSH,LTA_OKROSHKA


ids_wss = { 
    'ex': PTA4_WDDCr(period=3,threshold=50),
    '0': PTA4_WDDCr(period=11,threshold=30),
    '1': PTA8_WDOBBY_FREEr(period=6,multiplier=0.5,threshold=30),
    '2': PTA4_WDDCr(period=4,threshold=30),
    '3': PTA4_WDVCr(period=11,threshold=30),
    '4': OGTA4_DOG(period=25,threshold=30),
    '5': PTA4_WLISICA(period=7,divider=2,threshold=30),
    '6': LTA_OKROSHKA(period=10,period_chop=15),
    
    }
