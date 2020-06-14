from django.urls import path
from . import views


urlpatterns = [
    path('', views.compare_files, name='compare_files'),
]