from rest_framework import routers
from django.urls import path, include

from files import views

app_name = 'files'

router = routers.SimpleRouter()
router.register('files', views.FileListViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
