from rest_framework import mixins, viewsets

from files.filters import FileFilter
from files.models import File
from files.serializers import FileSerializer


class FileListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    '''Класс для отображения списка сохраненных файлов, конкретного
    файлa по id, а также добавления и удаления файлов.'''

    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_class = FileFilter

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'detail': 'Объект успешно удален'}
        return response

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
