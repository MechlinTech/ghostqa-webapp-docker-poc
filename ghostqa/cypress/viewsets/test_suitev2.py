import json
from io import BytesIO
import mimetypes

import yaml,os
from cypress.build_cypress import generate_cypress_testv2,generate_test_cases
from cypress.docker.containers import (get_container,
                                       start_test_inside_conatiner,start_test_inside_conatinerV2)
from cypress.models import TestSuite
from cypress.serializers.execute import (  # Assuming you have a serializer for TestSuite
    ExecuteSerializers, TestContainersRunsSerializer, TestSuiteSerializer)
from cypress.utils import (format_javascript,check_container_status, convert_to_unix_path,
                           create_directory, directory_exists, get_full_path,copy_files_and_folders,
                           list_files_in_directory)
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from PIL import Image as PILImage
from rest_framework import viewsets,mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination

from django.conf import settings
from ..models import TestArtifacts, TestContainersRuns, TestSuite
import os

class TestSuiteV2ViewSet(mixins.CreateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializer
    pagination_class = PageNumberPagination
    page_size = 10 
    def get_parser_classes(self):
        return [MultiPartParser]
    
    
    @action(methods=['get'],detail=False)
    def sample_json(self,request,*args, **kwargs):
        try:
           with open(os.path.join(settings.SAMPLES_PATH,'sample.json'), 'r') as file:
                data = json.load(file)
                return JsonResponse(data, safe=False)
        except FileNotFoundError:
            return JsonResponse({'error': 'File not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in file'}, status=500)
    
    @action(methods=['get'],detail=False)
    def sample_yaml(self,request,*args, **kwargs):
        try:
            with open(os.path.join(settings.SAMPLES_PATH,'sample.json'), 'r') as file:
                data = json.load(file)
                yaml_data = yaml.dump(data, default_flow_style=False)
                return HttpResponse(yaml_data, content_type='text/yaml')
                
            #  with open(os.path.join(settings.SAMPLES_PATH,'sample.yaml'), 'r') as file:
            #     data = yaml.safe_load(file)
            #     yaml_data = yaml.dump(data, default_flow_style=False)
        except FileNotFoundError:
            return HttpResponse('File not found', status=404)
        except yaml.YAMLError:
            return HttpResponse('Invalid YAML format in file', status=500)  
        
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
        
        cypress_code = generate_cypress_testv2(tests)
        cypress_code = format_javascript(cypress_code)
        instance.cypress_code = cypress_code
        instance.save()
        name = container_run.container_name
        BASE_DIR  = settings.BASE_DIR
        CYPRESS_CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR,"cypress","cypress"))
        
        volume_path = f"/automation-tests/{name}/cypress"
        volume_path = get_full_path(volume_path)
        volume_path = convert_to_unix_path(volume_path)
        if settings.SHARED_PATH:
                volume_path = f"{settings.SHARED_PATH}/{name}/cypress"
        print(f"{__name__}: volume_path: {volume_path}")
        
        create_directory(f"{volume_path}")
        copy_files_and_folders(CYPRESS_CONFIG_PATH,volume_path)       
        create_directory(f"{volume_path}/e2e/cypress/e2e/")
         
        with open(
                f"{volume_path}/e2e/cypress/e2e/{name}.cy.js", "w"
            ) as cypress_test_file:
                cypress_test_file.write(cypress_code)
        
        # with open(
        #         f"/automation-tests/{name}/e2e/cypress.config.js", "w"
        #     ) as destination_config:
        #         with open(os.path.join(CYPRESS_CONFIG_PATH,"e2e","cypress.config.js"),"r") as source_config:
        #             destination_config.write(source_config.read())
        # with open(
        #         f"/automation-tests/{name}/Dockerfile", "w"
        #     ) as destination_config:
        #         with open(os.path.join(CYPRESS_CONFIG_PATH,"Dockerfile"),"r") as source_config:
        #             destination_config.write(source_config.read())
                                    
        
       
        
        print("STARTING CONTAINER")
        start_test_inside_conatinerV2(container_run.container_name,volume_path,container_run)

        container_run_serilzer = TestContainersRunsSerializer(container_run)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
           **self.get_serializer(instance).data
        })
    @extend_schema(methods=['post'], request=TestSuiteSerializer)
    @action(methods=['post'],detail=False)
    def execute2(self,request,*args, **kwargs):
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
        BASE_DIR  = settings.BASE_DIR
        CYPRESS_CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR,"cypress","cypress"))
        name = container_run.container_name
        
        volume_path = f"/automation-tests/{name}/cypress"
        volume_path = get_full_path(volume_path)
        volume_path = convert_to_unix_path(volume_path)
        if settings.SHARED_PATH:
                volume_path = f"{settings.SHARED_PATH}/{name}/cypress"
        print(f"{__name__}: volume_path: {volume_path}")
        
        create_directory(f"{volume_path}")
        copy_files_and_folders(CYPRESS_CONFIG_PATH,volume_path)       
        create_directory(f"{volume_path}/e2e/cypress/e2e/")
        cypress_code = []
        for suites in tests:
            test_cases = suites.get('testCases', [])
            before_each = suites.get('beforeEach', [])
            result_cypress_code = f"{generate_test_cases(test_cases,before_each)}"
            # result_cypress_code = format_javascript(cypress_code)
            cypress_code.append(result_cypress_code)
         
            with open(
                    f"{volume_path}/e2e/cypress/e2e/{suites['name']}.cy.js", "w"
                ) as cypress_test_file:
                    cypress_test_file.write(result_cypress_code)
        

        instance.cypress_code = "\n".join(cypress_code)
        instance.save()       
        
       
        
        print("STARTING CONTAINER")
        start_test_inside_conatinerV2(container_run.container_name,volume_path,container_run)

        container_run_serilzer = TestContainersRunsSerializer(container_run)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
           **self.get_serializer(instance).data
        })
        
    @extend_schema(methods=['post'], request=TestSuiteSerializer)
    @action(methods=['post'],detail=False)
    def execute3(self,request,*args, **kwargs):
        data = request.data
        request_json = data.get('request_json', None)
        print("Data from the request body : ",data)
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
        try: # TODO we don't need this any more. Need to confirm from Diljot regarding this.
            # Use request_json directly
            tests = instance.request_json
        except Exception as e:
            return JsonResponse({
                "Status": "Unable to parse JSON or yaml file",
                "json": f"{e}",
                "yaml": None
            }, status=400)
        
        BASE_DIR  = settings.BASE_DIR
        CYPRESS_CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR,"cypress","cypress"))
        name = container_run.container_name
        
        volume_path = f"/automation-tests/{name}/cypress"
        volume_path = get_full_path(volume_path)
        volume_path = convert_to_unix_path(volume_path)
        if settings.SHARED_PATH:
                volume_path = f"{settings.SHARED_PATH}/{name}/cypress"
        print(f"{__name__}: volume_path: {volume_path}")
        
        create_directory(f"{volume_path}")
        copy_files_and_folders(CYPRESS_CONFIG_PATH,volume_path)       
        create_directory(f"{volume_path}/e2e/cypress/e2e/")
        cypress_code = []
   
        for suites in instance.request_json: # using converted json
            test_cases = suites.get('testCases', [])
            before_each = suites.get('beforeEach', [])
            result_cypress_code = """
            // Prevent Cypress from failing the test on uncaught errors
            Cypress.on('uncaught:exception', (err, runnable) => {
            // Log the error (optional)
            console.error('Uncaught Exception:', err.message);
            
            // Return false to prevent Cypress from failing the test
            return false;
            }); \n\n\n""" + f"{generate_test_cases(test_cases,before_each)}"
            # result_cypress_code = format_javascript(cypress_code)
            cypress_code.append(result_cypress_code)
         
            with open(
                    f"{volume_path}/e2e/cypress/e2e/{suites['name']}.cy.js", "w"
                ) as cypress_test_file:

                    cypress_test_file.write(result_cypress_code)
        

        instance.cypress_code = "\n".join(cypress_code)
        instance.save()       
        
       
        
        print("STARTING CONTAINER")
        start_test_inside_conatinerV2(container_run.container_name,volume_path,container_run)

        container_run_serilzer = TestContainersRunsSerializer(container_run)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
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
        
        if artifacts.type == "result":
            # Open the image using PIL
            file_data = artifacts.files.read().decode('utf-8')
            
            data = json.loads(file_data)
            return JsonResponse(data)
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
        return Response({
            "error":"error"
        },status=400) 
        
             
    @action(methods=['get'],detail=True)
    def monitor_container_run(self,request,*args, **kwargs):
        container_run = get_object_or_404(TestContainersRuns,**kwargs)
        
        
        return Response({
            **TestContainersRunsSerializer(container_run).data
        })
        
class TestContainersRunsViewset(viewsets.ModelViewSet):
    queryset = TestContainersRuns.objects.all()
    serializer_class = TestContainersRunsSerializer