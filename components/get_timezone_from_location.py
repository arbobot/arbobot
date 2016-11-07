# -*- coding: utf-8 -*-
import arrow
from datetime import datetime, timedelta
from meya import Component
from pytz import timezone
import pytz


class CalculateAlarm(Component):
    
    def start(self):
        wakeuptime = self.db.user.get("wakeup_time")
        
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        utc = pytz.utc
        utc_dt = utc.localize(datetime.utcfromtimestamp(wakeuptime))
        print utc_dt.strftime(fmt)
        au_tz = timezone('Australia/Sydney')
        au_dt = utc_dt.astimezone(au_tz)
        print au_dt.strftime(fmt)
        
        
        
        print("Wake up time picked was " + datetime.fromtimestamp(int(wakeuptime)).strftime('%H:%M'))
        
        try:
            offset = int(self.db.user.get("timezone"))
        except:
            offset = int(self.db.user.get("timezone_custom") or 0)
        
        alarm_hour = int(datetime.fromtimestamp(int(wakeuptime)).strftime('%H'))
        #int(self.db.user.get("alarm_hour"))
        alarm_minute = int(datetime.fromtimestamp(int(wakeuptime)).strftime('%M'))
        #int(self.db.user.get("alarm_minute"))
        
        
        print("Alarm hour: " + str(alarm_hour));
        print("Alarm minute: " + str(alarm_minute));
        
        
        # calculate alarm time
        
        #if offset is greater than hour then reduce day by 1
        
        # hour
        
        alarm_time = arrow.utcnow().replace(
            hour=(alarm_hour - offset), minute=alarm_minute, second=0)
        
        print alarm_time

        # check if alarm already happened "today"
        if alarm_time < arrow.utcnow():
            alarm_time = alarm_time.replace(days=+1)

        # convert to UNIX time
        unix_time = alarm_time.timestamp

        # save the result to the flow
        self.db.flow.set("alarm_time", unix_time)
        self.db.flow.set("alarm_time_output", datetime.fromtimestamp(int(wakeuptime)).strftime('%H:%M'))

        return self.respond(action="next")