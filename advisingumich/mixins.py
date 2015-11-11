class AdvisingUmichDataCleanupMixin(object):
    def valid_date_or_none(self, dt):
        if dt.id < 0:
            return None
        else:
            return dt
