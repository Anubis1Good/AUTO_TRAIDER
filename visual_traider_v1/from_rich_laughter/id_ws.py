from from_rich_laughter.work_strategies import PTA4_WDDCr,PTA4_WLISICA,PTA8_WDOBBY_FREEr,PTA4_WDVCr,OGTA4_DOG,LTA_KROSH,LTA_OKROSHKA,PTA4_WDDCrVG,PTA4_WDDCrE,PTA10_WIZARD,LTA_SAVUNIA,LTA_KOPATYCH,LTA_PIN,LTA_NUSHA,LTA_LOSYASH


ids_wss = { 
    # 'ex': PTA4_WDDCr(period=3,threshold=50),
    '0': PTA4_WDDCr(period=11,threshold=30),
    '1': PTA8_WDOBBY_FREEr(period=6,multiplier=0.5,threshold=30),
    '2': PTA4_WDDCr(period=10,threshold=20), 
    '3': PTA4_WDVCr(period=11,threshold=30),
    '4': OGTA4_DOG(period=25,threshold=30),
    '5': PTA4_WLISICA(period=7,divider=2,threshold=30),
    '6': LTA_OKROSHKA(period=10,period_chop=15),
    '7': PTA4_WDDCr(period=6,threshold=30), 
    '8': PTA4_WDDCrVG(period=11,threshold=30), 
    '9': LTA_KROSH(period=5,threshold=15), 
    '10': PTA4_WDDCrE(period=6,threshold=30), 
    '11': PTA4_WDDCr(period=21,threshold=30),
    '12': PTA8_WDOBBY_FREEr(period=11,multiplier=0.5,threshold=30),
    '13': PTA10_WIZARD(period=30,period2=55,period3=3,threshold=15,threshold_adx=20),
    '14': LTA_SAVUNIA(period=30,threshold=25),
    '15': LTA_KOPATYCH(period=10,threshold=40),
    '16': PTA10_WIZARD(period=20,period2=55,period3=12,threshold=25,threshold_adx=20),
    '17': LTA_PIN(period=10,period2=7,threshold=50,solution=5),
    '18': LTA_NUSHA(period=10,threshold=20),
    '19': OGTA4_DOG(period=20,threshold=40),
    '20': PTA4_WDDCrE(period=10,threshold=20), 
    '21': PTA8_WDOBBY_FREEr(period=11,multiplier=2,threshold=30),
    '22': LTA_LOSYASH(period=10,threshold=45),

    }
