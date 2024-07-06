import os

from django.conf import settings


def delete_file(sender, **kwargs):
    '''Метод для удаления файла, связанного с удаленным объектом БД.'''

    instance = kwargs.get('instance')
    if not instance:
        return
    file_instance = instance.file
    file_path = os.path.join(settings.MEDIA_ROOT, file_instance.name)
    if os.path.exists(file_path):
        return os.remove(file_path)
