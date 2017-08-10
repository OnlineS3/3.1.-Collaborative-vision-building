from django.conf import settings

class CvbappDBRouter(object):
    """
    A router to control app1 db operations
    """
    def db_for_read(self, model, **hints):
        if not settings.DATABASES.has_key('db_cvbapp'):
            return None
        if model._meta.app_label == 'cvbapp':
            return 'db_cvbapp'
        return None

    def db_for_write(self, model, **hints):
        if not settings.DATABASES.has_key('db_cvbapp'):
            return None
        if model._meta.app_label == 'cvbapp':
            return 'db_cvbapp'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if not settings.DATABASES.has_key('db_cvbapp'):
            return None
        if obj1._meta.app_label == 'cvbapp' or obj2._meta.app_label == 'cvbapp':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if not settings.DATABASES.has_key('db_cvbapp'):
            return None
        if db == 'db_cvbapp':
            return app_label == 'cvbapp'
        return None