from rest_framework import serializers

from ..models import PerformaceTestSuite,TestContainersRuns,TestArtifacts, CSVData

from django.urls import reverse



class TestArtifactsSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    
    def get_files(self,instance):
        from crum import get_current_request
        request = get_current_request()
        
        get_file_url = reverse( 'performacetestsuite-get-file', kwargs={'pk': instance.pk})
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
            'test_file',
            'container_labels',
            'container_name',
            'container_short_id',
            'ref',
            'runs_artifacts',
            'json',
            'suite',
            'container_logs_str',
            'client_reference_id'
            ]
        
class PerformaceTestSuiteSerializer(serializers.ModelSerializer):
    
    def validate(self, attrs):
        data =  super().validate(attrs)
        test_file = data.get('test_file', None)

        if test_file:
            # Extract information from the uploaded file, for example, file extension
            file_extension = test_file.name.split('.')[-1].lower()

            # You can perform additional checks or extract other information as needed
            # For example, check if the file extension is allowed
            allowed_extensions = ['jmx']  # Add the extensions you want to allow

            if file_extension not in allowed_extensions:
                raise serializers.ValidationError("Invalid file extension. Allowed extensions are: {}".format(allowed_extensions))

            if file_extension ==    'jmx':
                data['type'] = "jmeter"

        return data
    class Meta:
        model = PerformaceTestSuite
        fields = ["id","name", "jrampup_time","jthreads_total_user", "jrampup_steps", "durations" ,"test_file", "client_reference_id", "container_runs","type"]
        read_only_fields = ["id","type","container_runs"]


class CSVDataserializer(serializers.ModelSerializer):
    suite_data = serializers.SerializerMethodField()
    csv_file = serializers.FileField()
    # csv_file = serializers.ListField(child=serializers.FileField())
    
    class Meta:
        model = CSVData
        fields = ['id', 'suite', 'name', 'csv_file', 'suite_data']
        
    def get_suite_data(self, obj):
        suite = obj.suite
        if suite:
            serializer = PerformaceTestSuiteSerializer(suite)
            return serializer.data
        return None
        
    def validate(self, data):
        if 'csv_file' not in data:
            raise serializers.ValidationError('CSV file is required')
        return data
    
    # def create(self, validated_data):
    #     csv_files = validated_data.pop('csv_file', [])
    #     instance = super().create(validated_data)

    #     for csv_file in csv_files:
    #         instance.csv_file.create(csv_file=csv_file)

    #     return instance