# -*- coding: utf-8 -*-
import arrow
from utils import toUTC, makeDateFuture
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

        # set alarm time with hour and minute picked
        alarm_time = arrow.utcnow().replace(
            hour=alarm_hour,
            minute=alarm_minute,
            second=0)

        # check if alarm already happened "today"
        if alarm_time < arrow.utcnow():
            alarm_time = alarm_time.replace(days=+1)

        # apply the offset to hours (convert user time to servertime)
        toUTC(alarm_time, self.db.user.get("timezone"))

        # save the result to the flow
        self.db.flow.set("alarm_time", alarm_time.timestamp)
        self.db.flow.set("alarm_time_output", datetime.fromtimestamp(wakeup_time).strftime('%H:%M'))

        return self.respond(action="next")
