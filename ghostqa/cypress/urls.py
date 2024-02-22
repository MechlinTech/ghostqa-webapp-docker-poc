from django.contrib import admin
from django.urls import path

from .views import ExecuteAPIView,VideosAPIView,ScreenshotsAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
     path('execute/', ExecuteAPIView.as_view(), name='execute-api'),
     path('screenshots/', ScreenshotsAPIView.as_view(), name='screenshots-api'),
     path('videos/', VideosAPIView.as_view(), name='videos-api'),
]
