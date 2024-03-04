import json
import mimetypes
import os
from io import BytesIO

import yaml
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from PIL import Image as PILImage
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from ..models import PerformaceTestSuite,TestContainersRuns
from ..serializers.performace_tests import PerformaceTestSuiteSerializer
from cypress.utils import (format_javascript,check_container_status, convert_to_unix_path,
                           create_directory, directory_exists, get_full_path,copy_files_and_folders,
                           list_files_in_directory)

from ..docker.containers import start_jmeter_test
class PerformaceViewSet(mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = PerformaceTestSuite.objects.all()
    serializer_class = PerformaceTestSuiteSerializer

    def get_parser_classes(self):
        return [MultiPartParser]
    
    @action(detail=True,methods=['GET'])
    def execute(self, request, *args, **kwargs):
        instance = self.get_object()
        container_run = TestContainersRuns.objects.create(
            suite = instance,
            container_status= f"pending"
        )
        container_run.container_name =  f"{instance.name}-{container_run.ref}"
        container_run.save()
        
        name = container_run.container_name
        volume_path = f"/tests/performace/{name}/"
        volume_path = get_full_path(volume_path)
        volume_path = convert_to_unix_path(volume_path)
        if settings.SHARED_PATH:
                volume_path = f"{settings.SHARED_PATH}/performace/{name}/"
        
        if instance.type == "jmeter":
            create_directory(f"{volume_path}/html-results")
            with open(f"{volume_path}/test.jmx", "wb") as file:
                file.write(instance.test_file.read())
                
            print("STARTING CONTAINER")
            start_jmeter_test(name,volume_path,instance.jthreads,instance.jrampup,container_run)
            
        return Response({
            "status":   "success",
            "data":self.get_serializer(instance).data
        })