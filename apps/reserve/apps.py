from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect


class ReserveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reserve'

    def ready(self):
        mongo_setting = settings.MONGO
        connect(**mongo_setting)