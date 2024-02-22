import json

import yaml
from cypress.build_cypress import generate_cypress_test
from cypress.docker.containers import start_test_inside_conatiner,get_container
from cypress.models import TestSuite
from cypress.serializers.execute import (  # Assuming you have a serializer for TestSuite
    ExecuteSerializers, TestSuiteSerializer,TestContainersRunsSerializer)
from cypress.utils import (check_container_status, convert_to_unix_path,
                           create_directory, directory_exists, get_full_path,
                           list_files_in_directory)
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from ..models import TestArtifacts, TestContainersRuns, TestSuite


class TestSuiteViewSet(viewsets.ModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer

    
    def get_parser_classes(self):
        return [MultiPartParser]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(methods=['post'], request=TestSuiteSerializer)
    @action(methods=['post'],detail=False)
    def execute(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        
        container_run = TestContainersRuns.objects.create(
            suite = instance
        )
        container_run.container_name =  f"{instance.name}-{container_run.ref}"
        container_run.container_status =  f"pending"
        container_run.save()
        
        tests = yaml.safe_load(instance.scenarios_file)

        cypress_code = generate_cypress_test(tests)
        name = container_run.container_name
        
        create_directory(f"/automation-tests/{name}/e2e/cypress/integration/")
        create_directory(f"/automation-tests/{name}/e2e/logs")
        with open(
                f"/automation-tests/{name}/e2e/cypress/integration/{name}.cy.js", "w"
            ) as cypress_test_file:
                cypress_test_file.write(cypress_code)

        with open(
                f"/automation-tests/{name}/e2e/cypress.json", "w"
            ) as cypress_json:
                json_data = {"pluginsFile": False, "supportFile": False}
                json.dump(json_data, cypress_json)
                
        volume_path = f"/automation-tests/{name}/e2e"
        volume_path = get_full_path(volume_path)
        volume_path = convert_to_unix_path(volume_path)
        
        if settings.SHARED_PATH:
                volume_path = f"{settings.SHARED_PATH}/{name}/e2e"
        
        start_test_inside_conatiner(container_run.container_name,volume_path,container_run)

        container_run_serilzer = TestContainersRunsSerializer(container_run)
        
        headers = self.get_success_headers(serializer.data)
        return JsonResponse({
           **self.get_serializer(instance).data
        })
        
        
    @action(methods=['get'],detail=True)
    def monitor_container_run(self,request,*args, **kwargs):
        container_run = get_object_or_404(TestContainersRuns,**kwargs)
        
        
        return JsonResponse({
            **TestContainersRunsSerializer(container_run).data
        })
        
class TestContainersRunsViewset(viewsets.ModelViewSet):
    queryset = TestContainersRuns.objects.all()
    serializer_class = TestContainersRunsSerializer