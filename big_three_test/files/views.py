from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser

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
    parser_classes = (MultiPartParser,)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {'detail': 'Объект успешно удален'}
        return response
