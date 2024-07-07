import mimetypes
import os

from rest_framework import serializers

from files.fields import BinnaryImageField
from files.models import File


class FileSerializer(serializers.ModelSerializer):
    '''Сериализатор для обработки запросов при создании,
    получении и удалении файлов.'''

    file = BinnaryImageField()
    file_type = serializers.CharField(required=False)
    size = serializers.CharField(required=False)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        file = validated_data.get('file')
        file_type = validated_data.get('file_type')
        size = validated_data.get('size')
        # Если поля "тип файла" и "размер" не переданы в запросе,
        # они определяются в сериализаторе
        if file:
            if not file_type:
                validated_data['file_type'] = self.get_file_type(file)
            if not size:
                validated_data['size'] = self.get_file_size(file)
        return super().create(validated_data)

    def get_file_type(self, file):
        # Допустимые типы принимаемых файлов
        allowed_types = ['image', 'video']

        file_type, _ = mimetypes.guess_type(file.name)
        # file_type возвращается в формате "type/extension"
        try:
            file_type = file_type.split('/')[0]
        except AttributeError:
            raise serializers.ValidationError(
                'Поле "Тип файла" содержит недопустимое значение.'
            )
        return file_type if file_type in allowed_types else None

    def get_file_size(self, file):
        # переменная для дальнейшей конвертации полученного размера в MB
        m_bytes = 1_000_000

        file.seek(0, os.SEEK_END)
        return f'{(file.size)/m_bytes:.2f} MB'
