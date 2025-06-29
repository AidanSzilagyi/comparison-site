from django.apps import AppConfig


class CreatelistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'createList'
    
    def ready(self):
        import createList.signals
