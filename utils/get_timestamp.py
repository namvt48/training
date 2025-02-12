import time
import datetime

year = 2025
month = 1
day = 31
hour = 23
minute = 59
second = 0

dt = datetime.datetime(year, month, day, hour, minute, second)
timestamp = int(time.mktime(dt.timetuple()))
print(timestamp)