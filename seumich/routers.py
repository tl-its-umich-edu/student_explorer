from django.conf import settings

class SeumichRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'seumich':
            return 'seumich'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'seumich':
            return 'seumich'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'seumich':
            return settings.DATABASES['seumich'].get('MIGRATE', False)
