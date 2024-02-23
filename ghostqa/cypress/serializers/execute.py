
from rest_framework import serializers
from cypress.models import TestSuite,TestContainersRuns,TestArtifacts

from django.urls import reverse
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
        fields = '__all__'
        
class TestSuiteSerializer(serializers.ModelSerializer):
    scenarios_file = serializers.FileField()  # You may want to specify a custom upload_to path
    name = serializers.CharField(max_length=1000)
    client_reference_id = serializers.CharField(required=False)
    container_runs = TestContainersRunsSerializer(many=True,read_only=True)
    
    class Meta:
        model = TestSuite
        fields = ["id", "client_reference_id", "scenarios_file", "name","container_runs"]