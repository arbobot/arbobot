from datetime import datetime, timedelta
from pytz import timezone
import arrow
import pytz

format = "%Y-%m-%d %H:%M:%S %Z%z"


# Given a timezone (eg "America/Los_Angeles") it gives you back the converted UTC time
def toUTC(my_time, str_timezone):
    # Convert to new time zone
    local_tz = timezone (str_timezone)
    local_dt = local_tz.localize(my_time, is_dst=None).astimezone(pytz.utc)
    #print "Old time: " + my_time.strftime(format)
    #print "New time: " + local_dt.strftime(format)
    return local_dt
def makeDateFuture(my_time):
        # check if alarm already happened "today"
        if pytz.utc.localize(my_time) < arrow.utcnow():
            my_time = my_time.replace(days=+1)
