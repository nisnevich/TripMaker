from datetime import datetime
from dateutil.relativedelta import *


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

assert diff_month(datetime(2010, 10, 1), datetime(2010, 9, 1)) == 1
assert diff_month(datetime(2010, 10, 1), datetime(2009, 10, 1)) == 12
assert diff_month(datetime(2010, 10, 1), datetime(2009, 11, 1)) == 11
assert diff_month(datetime(2010, 10, 1), datetime(2009, 8, 1)) == 14
assert diff_month(datetime(2017, 2, 28), datetime(2016, 12, 1)) == 2

print(datetime(2017, 11, 30) + relativedelta(months=2))
