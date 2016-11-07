from meya import Component


class CheckTimeZoneExists(Component):

    def start(self):
        # read in the timezone from the user
        timezone_offset = self.db.user.get("timezone")
        try:
            timezone_offset = int(timezone_offset)
            action = "has_timezone"
        except:
            action = "no_timezone"

        return self.respond(message=None, action=action)