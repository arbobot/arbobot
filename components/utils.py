from datetime import datetime, timedelta
from pytz import timezone
import arrow
import pytz

format = "%Y-%m-%d %H:%M %Z%z"

def getScheduleDelay(hour_loc, min_loc, user_tz):
    # set alarm time with hour and minute picked
    now_loc = datetime.now(tz=pytz.timezone(user_tz)) #11 Nov 2016 22:14
    alarm_time_loc = timezone(user_tz).localize(datetime(now_loc.year, now_loc.month, now_loc.day, hour_loc, min_loc)) #11 Nov 2016 7:10
    print "Users time: " + now_loc.strftime(format)
    print "Users wake up time: " + alarm_time_loc.strftime(format)

    # check if alarm already happened "today"
    if alarm_time_loc < now_loc:
        alarm_time_loc = alarm_time_loc + timedelta(days=1) #12 Nov 2016 7:10

    delta_in_secs = getDifferenceInSecs(alarm_time_loc, now_loc)
    return getUTCTimeFromNow(delta_in_secs)


def getDifferenceInSecs(date1, date2):
    #get difference between two dates
    delta_in_secs =  (date1 - date2).total_seconds()
    print "User notification in: " + str(delta_in_secs/3600) + "hrs"
    return delta_in_secs


def getUTCTimeFromNow(seconds_delay):
    # convert user time to utc servertime
    return timezone('UTC').localize(datetime.utcnow()) + timedelta(seconds=seconds_delay)
