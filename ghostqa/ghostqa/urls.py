"""
URL configuration for ghostqa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from cypress.viewsets.test_suite import TestSuiteViewSet,TestContainersRunsViewset
from cypress.viewsets.test_suitev2 import TestSuiteV2ViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from performace_test.viewsets.performace_tests import PerformaceViewSet
from performace_test.viewsets.container_runs import ContainersRunsViewSet as PerformanceContainersRunsViewSet
router = DefaultRouter()
# router.register(r'testsuites', TestSuiteViewSet)
router.register(r'test-suitesV2', TestSuiteV2ViewSet)
router.register(r"performance-tests",PerformaceViewSet)
router.register(r"performance-container-runs",PerformanceContainersRunsViewSet)
# router.register(r'container-runs', TestContainersRunsViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/',include('cypress.urls')),
    path('codeengine/api/', include(router.urls)),
    path('codeengine/api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('codeengine/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('codeengine/api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)