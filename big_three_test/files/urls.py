from rest_framework import routers

from files import views

app_name = 'files'

router = routers.SimpleRouter()
router.register('files', views.FileListViewSet, basename='file-list')
router.register(
    'files/create', views.FileCreateViewSet, basename='file-create',
)
router.register(
    'files/delete', views.FileRemoveViewSet, basename='file-delete',
)
