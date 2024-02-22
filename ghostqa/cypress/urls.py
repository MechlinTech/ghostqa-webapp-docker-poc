from django.contrib import admin
from django.urls import path

from .views import ExecuteAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
     path('execute/', ExecuteAPIView.as_view(), name='execute-api'),
]
