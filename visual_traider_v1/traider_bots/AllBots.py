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
from tas.BaseTA import BaseTA
from tas.CloserTA import CloserTA
from tas.PTA2_DDC import PTA2_DDC,PTA2a_DDC
from tas.PTA3_ADDC import PTA3_ADDC,PTA3a_ADDC
from tas.SleepTA import SleepTA

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
    'PTA2_DDC_5':(PTA2_DDC,(5,)),
    'PTA2_DDC_10':(PTA2_DDC,(10,)),
    'PTA2_DDC_15':(PTA2_DDC,(15,)),
    'PTA2_DDC_20':(PTA2_DDC,(20,)),
    'PTA2_DDC_30':(PTA2_DDC,(30,)),
    'PTA2_DDC_40':(PTA2_DDC,(40,)),
    'PTA2_DDC_60':(PTA2_DDC,(60,)),
    'PTA2a_DDC_15':(PTA2a_DDC,(15,)),
    'PTA2a_DDC_30':(PTA2a_DDC,(30,)),
    'PTA2a_DDC_60':(PTA2a_DDC,(60,)),
    'PTA3a_DDC_15':(PTA3a_ADDC,(15,1.5)),
    'PTA3_DDC_15':(PTA3_ADDC,(15,1.5))
}



