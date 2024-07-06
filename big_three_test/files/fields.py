import base64
from datetime import datetime

from django.core.files.base import ContentFile
from rest_framework import serializers


class BinnaryImageField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            now = datetime.now()
            data = ContentFile(
                base64.b64decode(imgstr),
                name=now.strftime('%d_%m_%Y__%H_%M_%S.') + ext
            )
        return super().to_internal_value(data)
