# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from meya import Component
from pytz import timezone
from utils import getScheduleDelay
import pytz


class ScheduleMorningWakeup(Component):
    def start(self):
        #set the timezone string set from the user object
        try: user_tz = self.db.user.get("timezone")
        except: user_tz = 'utc'

        #get wake up time picked
        wakeup_time_loc = int(self.db.user.get("wakeup_time"))
        alarm_hour_loc = int(datetime.fromtimestamp(wakeup_time_loc).strftime('%H'))
        alarm_minute_loc = int(datetime.fromtimestamp(wakeup_time_loc).strftime('%M'))
        schedule_time_utc = getScheduleDelay(hour_loc=alarm_hour_loc, min_loc=alarm_minute_loc, user_tz=user_tz)

        # save the result to the flow
        self.db.flow.set("schedule_delay_utc", int(schedule_time_utc.strftime("%s")))
        return self.respond(action="next")
