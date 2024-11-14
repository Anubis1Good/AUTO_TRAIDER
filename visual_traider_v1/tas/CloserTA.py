'''
Закрывает сделки
'''

from tas.BaseTA import BaseTA,Keys

class CloserTA(BaseTA):
    def get_action(self, keys:Keys):
        return 'close_all'

