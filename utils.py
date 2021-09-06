from calendar import monthrange
from datetime import datetime

import numpy as np
import numpy.random as rd
from pyroaring import BitMap


def gen_random_tags():
    available_tags = np.arange(1, 11)
    num_of_tags = rd.randint(11)
    return BitMap(rd.choice(available_tags, num_of_tags, replace=False))


def gen_random_date():
    date = datetime.today()
    year = date.year
    month = date.month
    if date.month == 1:
        month = rd.choice([1, 12])
        if month == 12:
            year = year - 1
    else:
        month = rd.choice([month - 1, month])
    day = date.day

    if month == date.month:
        day = rd.randint(1, day + 1)
    else:
        day = rd.randint(1, monthrange(year, month)[1] + 1)
    return datetime(year, month, day)
