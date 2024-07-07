from django.db import models

from big_three_test.utils import generate_upload_path


class File(models.Model):
    '''Модель, содержащая данные о медиа-файле.'''
    file = models.FileField(
        upload_to=generate_upload_path,
        verbose_name='Файл',
    )
    file_type = models.CharField(
        max_length=50,
        verbose_name='Тип файла',
    )
    size = models.CharField(
        max_length=50,
        verbose_name='Размер файла',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-created']

    def __str__(self) -> str:
        return self.created.strftime('%d_%m_%Y__%H_%M_%S')
