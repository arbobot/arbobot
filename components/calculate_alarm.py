# -*- coding: utf-8 -*-
import arrow
from datetime import datetime, timedelta
from meya import Component
from pytz import timezone
import pytz


class CalculateAlarm(Component):
    
    def start(self):
        #get wake up time picked
        wakeup_time = int(self.db.user.get("wakeup_time"))
        print("Wake up time picked was " + datetime.fromtimestamp(wakeup_time).strftime('%H:%M'))
        alarm_hour = int(datetime.fromtimestamp(wakeup_time).strftime('%H'))
        alarm_minute = int(datetime.fromtimestamp(wakeup_time).strftime('%M'))
        
        # first work out timezone
        if isinstance(self.db.user.get("timezone"), int):
            #normall set by facebook messenger
            offset = int(self.db.user.get("timezone"))
        elif isinstance(self.db.user.get("timezone"), basestring):
            utc = pytz.utc
            utc_dt = utc.localize(datetime.utcfromtimestamp(wakeup_time))
            local_tz = timezone(self.db.user.get("timezone"))
            local_dt = utc_dt.astimezone(local_tz)
            # %z will output format of 1100 for +11 hrs
            offset = int(local_dt.strftime('%z'))/100 
        else :
            offset = 0
            
        # get timezone from location
        print 'Offset is set to ' + str(offset)
    
        # set alarm time with hour and minute picked
        alarm_time = arrow.utcnow().replace(
            hour=alarm_hour, 
            minute=alarm_minute, 
            second=0)

        # check if alarm already happened "today"
        if alarm_time < arrow.utcnow():
            alarm_time = alarm_time.replace(days=+1)
            
        # apply the offset to hours (convert user time to servertime)
        alarm_time= alarm_time + timedelta(hours=offset)
        
        
        print '- Time at user now: ' + str(datetime.fromtimestamp((arrow.utcnow() + timedelta(hours=offset)).timestamp).strftime('%Y-%m-%d %H:%M:%S %Z%z')) 
        print '- Server time now: ' + str(datetime.fromtimestamp(arrow.utcnow().timestamp).strftime('%Y-%m-%d %H:%M:%S %Z%z')) 
        print '- Wake up picked set to: ' + str(datetime.fromtimestamp(wakeup_time).strftime('%Y-%m-%d %H:%M:%S %Z%z')) 
        print '- Alarm set to: ' + str(datetime.fromtimestamp(alarm_time.timestamp).strftime('%Y-%m-%d %H:%M:%S %Z%z')) 

        # save the result to the flow
        self.db.flow.set("alarm_time", alarm_time.timestamp)
        self.db.flow.set("alarm_time_output", str(alarm_hour) + ":" + str(alarm_minute))

        return self.respond(action="next")