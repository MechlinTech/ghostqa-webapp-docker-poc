
from rest_framework import serializers
from cypress.models import TestSuite,TestContainersRuns,TestArtifacts
from io import BytesIO
from django.urls import reverse
from django.core.files import File
import json
from django.core.files.base import ContentFile
from .request import TestSuiteSerializer as RequestTestSuiteSerializer
class ExecuteSerializers(serializers.Serializer):
    upload_file = serializers.FileField()
    name = serializers.CharField(max_length=1000)
    

class TestArtifactsSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    
    def get_files(self,instance):
        from crum import get_current_request
        request = get_current_request()
        
        get_file_url = reverse( 'testsuite-get-file', kwargs={'pk': instance.pk})
        get_file_url = request.build_absolute_uri(get_file_url)
        return get_file_url
    class Meta:
        model = TestArtifacts
        fields = ["id", "type", "files", "container_runs", "suite"]
class TestContainersRunsSerializer(serializers.ModelSerializer):
    runs_artifacts = TestArtifactsSerializer(many=True)
    class Meta:
        model = TestContainersRuns
        fields = [
            'id',
            'container_id',
            'container_status',
            'container_labels',
            'container_name',
            'container_short_id',
            'ref',
            'runs_artifacts',
            'json',
            'suite',
            'container_logs_str',
            ]
        
class TestSuiteSerializer(serializers.ModelSerializer):
    scenarios_file = serializers.FileField(required=False)  
    name = serializers.CharField(max_length=1000)
    client_reference_id = serializers.CharField(required=False)
    container_runs = TestContainersRunsSerializer(many=True,read_only=True)
    request_json = RequestTestSuiteSerializer(many=True)
    
    class Meta:
        model = TestSuite
        fields = ["id", "client_reference_id", "name","container_runs","cypress_code","scenarios_file", "request_json"]
        
    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        
        # if 'request_json' in validated_data:
        #     json_data = json.dumps(validated_data.get('request_json'))
        
        #     # Create an in-memory byte stream
        #     byte_stream = BytesIO()
            
        #     # Write the JSON data into the byte stream
        #     byte_stream.write(json_data.encode())
            
        #     # Set the file pointer to the beginning of the byte stream
        #     byte_stream.seek(0)
            
        #     # Create a content file from the byte stream
        #     content_file = ContentFile(byte_stream.read())
        #     validated_data['scenarios_file'] = content_file
        return validated_data