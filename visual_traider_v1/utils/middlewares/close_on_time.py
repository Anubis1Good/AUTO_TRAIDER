from datetime import datetime
def only_close(action,hour,minute):
    now = datetime.now()
    chour = now.hour
    cminute = now.minute
    end_minute = minute + 15
    if hour == chour:
        if end_minute > cminute > minute:
            if action == 'long' or action == 'short':
                return None
        if end_minute < cminute:
            return 'close_all'
    return action