from django.apps import AppConfig
from django.db.models.signals import post_delete


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files'

    def ready(self):
        from files.signals import delete_file
        from files.models import File
        post_delete.connect(receiver=delete_file, sender=File)
        return super().ready()
