import numpy as np


def change_amount_points(sequence,lenght):
    len_seq = len(sequence)
    if len_seq < lenght:
        average = int(np.average(sequence))
        diff = lenght - len_seq
        add = np.array([average]*diff)
        sequence = np.concatenate((add,sequence))
    return sequence[-lenght:]
