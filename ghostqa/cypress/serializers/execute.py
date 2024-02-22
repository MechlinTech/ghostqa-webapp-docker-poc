
from rest_framework import serializers
from cypress.models import TestSuite,TestContainersRuns


class ExecuteSerializers(serializers.Serializer):
    upload_file = serializers.FileField()
    name = serializers.CharField(max_length=1000)
    

class TestContainersRunsSerializer(serializers.ModelSerializer):
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