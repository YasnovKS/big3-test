import os
from http import HTTPStatus
from pathlib import Path

from django.test import Client, TestCase
from django.urls import reverse

from files.models import File


def get_test_picture():
    picture_path = Path(__file__).parent / 'picture_for_test.txt'
    if not os.path.exists(picture_path):
        raise RuntimeError('Тестовое изображение не найдено.')
    with open(picture_path, 'r') as file:
        content = file.read()
    return content


class FileViewTests(TestCase):
    '''Класс для тестирования корректной работы вьюсетов.'''

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        obj_data = {
            'first': {
                "file": 'url/to/file_1',
                'file_type': 'image',
                'size': '100 MB',
            },
            'second': {
                "file": 'url/to/file_2',
                'file_type': 'video',
                'size': '100 MB',
            }
        }
        for data in obj_data.values():
            File.objects.create(**data)

    def setUp(self) -> None:
        self.client = Client()

    def test_create_valid_object(self):
        '''Тестирование создания объекта с корректными данными.'''

        obj_data = {
            "file": get_test_picture(),
        }

        response = self.client.post(
            reverse('files:file-list'), data=obj_data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_create_invalid_object(self):
        '''Тестирование создания объекта с некорректными данными.'''

        obj_data = {
            "file": [
                # удаление подстроки data
                get_test_picture().replace('data', ''),
                # замена валидного расширения файла на невалидное
                get_test_picture().replace('jpeg', 'smth'),
            ]
        }

        response = self.client.post(
            reverse('files:file-list'), data=obj_data
        )
        for file in obj_data.get('file'):
            with self.subTest():
                response = self.client.post(
                    reverse('files:file-list'),
                    data={'file': file},
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_object_list(self):
        '''Тестирование получения списка объектов.'''

        response = self.client.get(reverse('files:file-list'))
        files_count = File.objects.count()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data.get('count'), files_count)

    def test_get_object_detail(self):
        '''Тестирование получения конкретного объекта.'''

        obj = File.objects.first()
        response = self.client.get(
            reverse('files:file-detail', args=(obj.id,))
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data.get('id'), obj.id)

    def test_delete_object(self):
        '''Тестирование удаления объекта.'''

        start_count = File.objects.count()
        if not start_count:
            raise RuntimeError(
                'В базе данных отсутствуют объекты для тестирования'
            )
        obj = File.objects.first()
        response = self.client.delete(
            reverse('files:file-detail', args=(obj.id,))
        )
        end_count = File.objects.count()
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(start_count, end_count + 1)
