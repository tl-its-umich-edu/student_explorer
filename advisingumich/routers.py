from django.conf import settings


class DataWarehouseRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == settings.ADVISING_PACKAGE:
            return settings.ADVISING_DATABASE
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == settings.ADVISING_PACKAGE:
            return settings.ADVISING_DATABASE
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        if db == settings.ADVISING_DATABASE:
            return None
        return True
