from datetime import datetime

from src.const.constants import DATE_FORMAT

date = datetime.strptime("2017-02-15", DATE_FORMAT)
print(date.replace(day=1))
print(date)
