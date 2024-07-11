import base64
import json
import logging
import pathlib
import time
from http import HTTPStatus

import cv2
import requests
from django.conf import settings

logger = logging.getLogger('vision')


class CameraConfig:
    '''Класс конфигурации для подключения к камере.'''

    def __init__(self, camera_url: str = None, interval: int = None):
        default_url = 'https://streams.cam72.su/1500-1032/tracks-v1/mono.m3u8'
        default_interval = 1

        # Если url камеры отсутствует, экземпляру присваивается дефолтный url
        # камера на перекрестке в г. Тюмени
        self.camera_url = camera_url if camera_url else default_url

        # В интервале указывается количество секунд между процессами
        # распознавания объектов (по умолчанию - 1 сек)
        self.interval = interval if interval else default_interval

    def get_config_params(self):
        '''Возвращает конфигурационные параметры.'''

        return self.camera_url, self.interval


class DetectionConfig:
    '''Класс конфигурации для распознавания объектов.'''

    detection_objects = {
        'cars': (
            pathlib.Path(__file__).parent / 'detection_cascades/cars.xml'
        ),
        'people': (
            pathlib.Path(__file__).parent / 'detection_cascades/people.xml'
        ),
    }

    def __init__(self, object_type: str = None):
        self.object_type = object_type

    def __object_type_is_valid(self):
        '''Проверяет валидность параметра object_type.'''

        keys = self.detection_objects.keys()
        if self.object_type.lower() not in keys:
            logger.error(
                    'Передан недопустимый для detection_objects параметр '
                    f'{self.object_type}'
                )
            raise AssertionError(
                f'Параметр {self.object_type} не является допустимым '
                'для object_type. Список доступных параметров можно'
                'получить при вызове метода get_allowed_types.'
            )
        return True

    def get_detection(self):
        '''Возвращает каскадный классификатор для объектов.'''

        if self.__object_type_is_valid():
            return cv2.CascadeClassifier(
                self.detection_objects.get(self.object_type)
            )

    def get_allowed_types(self):
        '''Возвращает массив допустимых типов объектов для распознавания.'''

        return self.detection_objects.keys()


class VideoCatch:
    '''Класс для получения видеопотока с онлайн-камеры.'''

    def __init__(
        self,
        camera_config: CameraConfig,
        detection: DetectionConfig,
    ):
        self.camera_url = camera_config.camera_url
        self.interval = camera_config.interval
        self.last_detection_time = time.time()
        self.stream = cv2.VideoCapture(self.camera_url)
        self.detection = detection.get_detection()

    def __get_stream(self):
        '''Возвращает кадр с камеры.'''

        return self.stream.read()

    def __send_api_request(self, data, headers):
        return requests.post(
            f'{settings.DOMAIN}/api/files/', data=data, headers=headers
        )

    def __create_rectangles(self, items, frame):
        '''Создает желтые прямоугольники вокруг распознанных объектов.'''

        for (x, y, w, h) in items:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

    def __get_base64_image(self, buffer):
        '''Представляет контент фрейма в кодировке Base64.'''

        return (
            'data:image/jpeg;base64,' +
            base64.b64encode(buffer).decode('utf-8')
        )

    def __get_request_params(self, content):
        '''Возвращает контент и заголовки запроса.'''

        data = json.dumps({'file': content})
        headers = {
            'Content-Type': 'application/json',
        }
        return data, headers

    def __stop_stream(self):
        '''Останавливает обработку видеопотока.'''

        self.stream.release()
        cv2.destroyAllWindows()

    def process(self):
        '''Метод для запуска процессе обработки видеопотока
        с распознаванием объектов.'''

        logger.info(f'Подключение к камере: {self.camera_url}...')
        start_time = time.time()
        while True:
            success, frame = self.__get_stream()
            if not success:
                logger.error(
                    'Не удалось подключиться к камере по url '
                    f'{self.camera_url}'
                )
                break
            current_time = time.time()
            if current_time - start_time > settings.ALLOWED_TIMEOUT:
                break
            if current_time - self.last_detection_time >= self.interval:
                # Преобразование в оттенки серого
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Обнаружение объектов
                items = self.detection.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30)
                )
                # Рисование прямоугольников вокруг обнаруженных объектов
                self.__create_rectangles(items, frame)

                if len(items):
                    # Получение массива данных фрейма
                    _, buffer = cv2.imencode('.jpg', frame)

                    # Представление в кодировке Base64
                    image_base64 = self.__get_base64_image(buffer)

                    # Создание данных для API запроса
                    data, headers = self.__get_request_params(image_base64)

                    # Отправка данных через API для сохранения изображение
                    # с распознанными объектами
                    response = self.__send_api_request(data, headers)
                    if response.status_code != HTTPStatus.CREATED:
                        logger.error(
                            'Произошла ошибка при отправке запроса на '
                            'сохранение файла.'
                        )
                        break
                    logger.info('Файл успешно сохранен.')
                    obj = response.json()
                    self.__stop_stream()
                    return obj.get('file')
            self.last_detection_time = current_time
        self.__stop_stream()
