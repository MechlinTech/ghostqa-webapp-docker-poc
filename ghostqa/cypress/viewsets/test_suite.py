import json
from io import BytesIO
import mimetypes

import yaml,os
from cypress.build_cypress import generate_cypress_test
from cypress.docker.containers import (get_container,
                                       start_test_inside_conatiner)
from cypress.models import TestSuite
from cypress.serializers.execute import (  # Assuming you have a serializer for TestSuite
    ExecuteSerializers, TestContainersRunsSerializer, TestSuiteSerializer)
from cypress.utils import (check_container_status, convert_to_unix_path,
                           create_directory, directory_exists, get_full_path,
                           list_files_in_directory)
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from PIL import Image as PILImage
from rest_framework import viewsets,mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from ..models import TestArtifacts, TestContainersRuns, TestSuite


class TestSuiteViewSet(mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer

    
    def get_parser_classes(self):
        return [MultiPartParser]
    
    
    
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
        try:
            tests = yaml.safe_load(instance.scenarios_file)
        except Exception as e:
            try:
                tests = json.load(instance.scenarios_file)
            except Exception as json_exception:
                return JsonResponse({
                "Status":"Unable to parse JSON or yaml file",
                "json":f"{json_exception}",
                "yaml":f"{e}"
                },status=400
                                    )
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
    def get_file(self,request,*args, **kwargs):
        view_name = request.resolver_match.url_name
        artifacts = get_object_or_404(TestArtifacts,**kwargs)
        
        if artifacts.type == "screenshot":
            # Open the image using PIL
            file_path = artifacts.files.path
            pil_image = PILImage.open(file_path)

            # Convert the PIL image to bytes
            image_bytes = BytesIO()
            pil_image.save(image_bytes, format="PNG")
            image_data = image_bytes.getvalue()

            # Create the HTTP response with the image data
            response = HttpResponse(image_data, content_type="image/png")
            response["Content-Disposition"] = f'attachment; filename="{file_path}"'
            return response
        if artifacts.type == "video":

            # Open the video file
            chunk_size = 8192  # Adjust the chunk size according to your needs

            # Set appropriate content type for video streaming
            content_type, encoding = mimetypes.guess_type(artifacts.files.path)
            response = HttpResponse(content_type=content_type)
            response["Content-Disposition"] = (
                f'inline; filename="{os.path.basename(artifacts.files.path)}"'
            )

            # Stream the video content
            with open(artifacts.files.path, "rb") as video_file:
                for chunk in iter(lambda: video_file.read(chunk_size), b""):
                    response.write(chunk)

            return response
        return JsonResponse({
            "error":"error"
        },status=400) 
        
             
    @action(methods=['get'],detail=True)
    def monitor_container_run(self,request,*args, **kwargs):
        container_run = get_object_or_404(TestContainersRuns,**kwargs)
        
        
        return JsonResponse({
            **TestContainersRunsSerializer(container_run).data
        })
        
class TestContainersRunsViewset(viewsets.ModelViewSet):
    queryset = TestContainersRuns.objects.all()
    serializer_class = TestContainersRunsSerializer