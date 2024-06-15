import datetime
from enum import Enum


class TimeframeEnum(Enum):
    DAY = datetime.timedelta(days=1)
    WEEK = datetime.timedelta(days=7)
    MONTH = datetime.timedelta(days=30)
    HALFYEAR = datetime.timedelta(days=180)
    YEAR = datetime.timedelta(days=360)
