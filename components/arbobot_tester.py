from utils import toUTC, makeDateFuture
import pytz, datetime
import parsedatetime as pdt #https://github.com/bear/parsedatetime

alarm_time = "";
cal = pdt.Calendar()
now = datetime.datetime.now()

while alarm_time != "exit":
    alarm_time = raw_input('What time do you want to set an alarm for?')
    for time_string in [alarm_time]: #"tomorrow at 6am"
        alarm_dt = (cal.parseDT(time_string, now)[0])
        print("%s:\t%s" % (time_string, alarm_dt))
        print("%s:\t%s" % ("Converted to UTC", toUTC(alarm_dt, "Australia/Sydney")))
        print('');
