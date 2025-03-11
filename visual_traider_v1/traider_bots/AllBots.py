from traider_bots.archive.OGT1 import OGT1
from traider_bots.archive.OGT2 import OGT2
from traider_bots.PST1 import PST1,PST1a
from traider_bots.PT1 import PT1
from traider_bots.PT2ov1 import PT2ov
from traider_bots.archive.PT2 import PT2
from traider_bots.archive.PT3 import PT3
from traider_bots.archive.PT4 import PT4
from traider_bots.archive.ST1 import ST1,ST1a
from traider_bots.archive.ST2 import ST2
from traider_bots.archive.ST3 import ST3,ST3a
from traider_bots.ST4 import ST4
from traider_bots.archive.ST5 import ST5
from traider_bots.archive.ST6 import ST6
from traider_bots.archive.ST7 import ST7
from traider_bots.archive.ST8 import ST8
from traider_bots.archive.ST9 import ST9
from traider_bots.archive.ST10 import ST10
from traider_bots.archive.ST11 import ST11
from traider_bots.archive.ST12 import ST12
from traider_bots.archive.ST13 import ST13
from traider_bots.archive.ST14 import ST14
from traider_bots.Collector1 import Collector1
from traider_bots.VisualTraider_v3 import VisualTraider_v3
from traider_bots.VisualTraider_v4 import VisualTraider_v4
from tas.BaseTA import BaseTA
from tas.CloserTA import CloserTA
from tas.SleepTA import SleepTA
from tas.PTA2_DDC import PTA2_DDC,PTA2a_DDC,PTA2_DDC2,PTA2a_DDC2
from tas.PTA3_ADDC import PTA3_ADDC,PTA3a_ADDC,PTA3_ADDC2
from tas.PTA4_WDDC import PTA4_WDDC,PTA4_WDDC2,PTA4_WDDC3,PTA4_WDDC3b,PTA4_WDDCrRL,PTA4_WDVCrRL
from tas.PTA5_MHP import PTA5_MHP
from tas.PTA6_COMA import PTA6_COMA
from tas.PTA7_MS1 import PTA7_MS1
from tas.LTA1_C import LTA1_C,LTA1_C2
from tas.LTA2_SP import LTA2_SP
from tas.OGTA1_Rails import OGTA1_Rails
from tas.STA2_PPP import STA2_PPP,STA2_R_PPP

VT2_bots = {
    'OGT1':OGT1,
    'OGT2':OGT2,
    'PST1':PST1,
    'PST1a':PST1a,
    'PT1':PT1,
    'PT2':PT2,
    'PT2ov':PT2ov,
    'PT3':PT3,
    'PT4':PT4,
    'ST1':ST1,
    'ST1a':ST1a,
    'ST2':ST2,
    'ST3':ST3,
    'ST3a':ST3a,
    'ST4':ST4,
    'ST5':ST5,
    'ST6':ST6,
    'ST7':ST7,
    'ST8':ST8,
    'ST9':ST9,
    'ST10':ST10,
    'ST11':ST11,
    'ST12':ST12,
    'ST13':ST13,
    'ST14':ST14,
    'Collector1':Collector1

}

VT3_bots = {
    'BaseTA':(BaseTA,()),
    'SleepTA':(SleepTA,()),
    'CloserTA':(CloserTA,()),
    'LTA1_C':(LTA1_C,(4,)),
    'LTA1_C2':(LTA1_C2,(5,2.5)),
    'LTA2_SP_25':(LTA2_SP,(0.25,)),
    'PTA2_DDC_15':(PTA2_DDC,(15,)),
    'PTA2_DDC_60':(PTA2_DDC,(60,)),
    'PTA2_DDC_80':(PTA2_DDC,(80,)),
    'PTA2_DDC_100':(PTA2_DDC,(100,)),
    'PTA2_DDC_120':(PTA2_DDC,(120,)),
    'PTA2a_DDC_15':(PTA2a_DDC,(15,)),
    'PTA2a_DDC_30':(PTA2a_DDC,(30,)),
    'PTA2a_DDC_60':(PTA2a_DDC,(60,)),
    'PTA2_DDC2_100':(PTA2_DDC2,(100,)),
    'PTA2a_DDC2_15':(PTA2a_DDC2,(15,)),
    'PTA3_ADDC_30_2':(PTA3_ADDC,(30,2)),
    'PTA3_ADDC2_150':(PTA3_ADDC2,(150,)),
    'PTA4_WDDC_100_10_20':(PTA4_WDDC,(100,10,20)),
    'PTA4_WDDC2_100_10_20':(PTA4_WDDC2,(100,10,20)),
    'PTA4_WDDC3_15_15_30':(PTA4_WDDC3,(15,15,30)),
    'PTA4_WDDC3_100_15_30':(PTA4_WDDC3,(100,15,30)),
    'PTA4_WDDC3b_100_15_30':(PTA4_WDDC3b,(100,15,30)),
    'PTA4_WDDCrRL_11_11_30':(PTA4_WDDCrRL,(11,11,30)),
    'PTA4_WDDCrRL_6_6_30':(PTA4_WDDCrRL,(6,6,30)),
    'PTA4_WDVCrRL_11_11_30':(PTA4_WDVCrRL,(11,11,30)),
    'PTA5_MHP':(PTA5_MHP,()),
    'PTA6_COMA_30_60':(PTA6_COMA,(30,60)),
    'PTA7_MS1_60':(PTA7_MS1,(60,)),
    'OGTA1_Rails':(OGTA1_Rails,()),
    'STA2_PPP_20':(STA2_PPP,(20,20,10,False)),
    'STA2_R_PPP':(STA2_R_PPP,()),
}



