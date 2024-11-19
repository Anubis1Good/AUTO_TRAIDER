from datetime import datetime
def only_close(action,hour,minute):
    now = datetime.now()
    chour = now.hour
    cminute = now.minute

    if hour == chour and cminute > minute:
        if action == 'long' or action == 'short':
            return None
    return action