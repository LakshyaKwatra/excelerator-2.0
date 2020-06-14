from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.upload_files, name='upload_files'),
    path('compare/', include(('compare.urls', 'compare'), namespace='compare'))
]
