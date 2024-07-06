from rest_framework import mixins, viewsets

from files.filters import FileFilter
from files.models import File
from files.serializers import FileSerializer


class FileListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    '''Класс для отображения списка сохраненных файлов
    или конкретного файлв по id.'''

    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_class = FileFilter


class FileCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''Класс представления для создания файла.'''

    serializer_class = FileSerializer


class FileRemoveViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''Класс для удаления файлов.'''

    queryset = File.objects.all()
    serializer_class = FileSerializer

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'detail': 'Объект успешно удален'}
        return response
