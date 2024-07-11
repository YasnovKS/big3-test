from django.urls import path

from vision import views

app_name = 'vision'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
