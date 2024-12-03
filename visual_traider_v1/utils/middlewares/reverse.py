def simple_reverse(action):
    if action:
        if 'long' in action:
            return action.replace('long','short')
        if 'short' in action:
            return action.replace('short','long')
