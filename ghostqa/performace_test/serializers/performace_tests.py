from rest_framework import serializers

from ..models import PerformaceTestSuite,TestContainersRuns,TestArtifacts

from django.urls import reverse
from collections import defaultdict


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


def group_data(raw_data):
    success_grouped_data = defaultdict(list)
    error_grouped_data = defaultdict(list)
    
    for raw_data_item in raw_data:
        if raw_data_item.get('success, False'):
            response_code = raw_data_item.get('responseCode', 'Unknown')
            success_grouped_data[response_code].append(raw_data_item)
        else:
            response_code = raw_data_item.get('responseCode', 'Unknown')
            error_grouped_data[response_code].append(raw_data_item)
    return success_grouped_data, error_grouped_data

def group_data_with_transaction(raw_data):
    success_data_with_transaction = defaultdict(list)
    error_data_with_transaction = defaultdict(list)
    
    for raw_data_item in raw_data:
        thread_name = raw_data_item.get('threadName', 'Unknown')
        if raw_data_item.get('success', False):
            success_data_with_transaction[thread_name].append(raw_data_item)
        else:
            error_data_with_transaction[thread_name].append(raw_data_item)
    
    return success_data_with_transaction, error_data_with_transaction
    


# def format_data(grouped_data):
#     formatted_data = [{'code': code, 'description': data[0]['responseMessage'], 'count': len(data)} for code, data in grouped_data.items()]
#     return formatted_data
def format_data(grouped_data):
    success_data, error_data = grouped_data
    formatted_data = [{'code': code, 'description': data[0]['responseMessage'], 'count': len(data)} for code, data in success_data.items()]
    # formatted_error_data = [{'code': code, 'description': data[0]['responseMessage'], 'count': len(data)} for code, data in error_data.items()]
    return formatted_data


def calculate_total_count(formatted_data):
    total_count = sum(item['count'] for item in formatted_data)
    return total_count
        
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
            'suite','raw_data',
            'container_logs_str',
            'client_reference_id'
            ]
        
    # def get_success_group_data(self, instance):
    #     # raw_data = instance.get('raw_data')
    #     raw_data = instance.raw_data
    #     grouped_data = group_data(raw_data)
    #     formatted_data = format_data(grouped_data)
    #     return formatted_data

    # def get_error_group_data(self, instance):
    #     raw_data = instance.raw_data
    #     grouped_data = group_data(raw_data)
    #     formatted_data = format_data(grouped_data)
    #     return formatted_data
    
    
    #######main below
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        raw_data = representation.get('raw_data')
        if raw_data is None or not raw_data:
            representation['success_group_data'] = None
            representation['error_group_data'] = None
            representation['error_group_data_with_transaction'] = None
            representation['success_group_data_with_transaction'] = None
            return representation

        # Group raw_data by responseCode
        success_grouped_data = defaultdict(list)
        error_grouped_data = defaultdict(list)
        success_thread_grouped_data = defaultdict(list)
        error_thread_grouped_data = defaultdict(list)
        for raw_data_item in raw_data:
            if raw_data_item.get('success', False):
                response_code = raw_data_item.get('responseCode', 'Unknown')
                success_grouped_data[response_code].append(raw_data_item)
                
                thread_name = raw_data_item.get('threadName', 'Unknown')
                success_thread_grouped_data[thread_name].append(raw_data_item)
            else:
                response_code = raw_data_item.get('responseCode', 'Unknown')
                error_grouped_data[response_code].append(raw_data_item)
                
                thread_name = raw_data_item.get('threadName', 'Unknown')
                error_thread_grouped_data[thread_name].append(raw_data_item)
        
        # Convert the grouped data to the desired format
        success_data = [{'code': code, 'description': data[0]['responseMessage'], 'count': len(data)} for code, data in success_grouped_data.items()]
        error_data = [{'code': code, 'description': data[0]['responseMessage'], 'count': len(data)} for code, data in error_grouped_data.items()]
        success_thread_data = [{'Thread Name': thread_name, 'data': data, 'count': len(data)} for thread_name, data in success_thread_grouped_data.items()]
        error_thread_data = [{'Thread Name': thread_name, 'data': data, 'count': len(data)} for thread_name, data in error_thread_grouped_data.items()]
        
        total_success_thread_count = sum(item['count'] for item in success_thread_data)
        total_error_thread_count = sum(item['count'] for item in error_thread_data)
        
        representation['success_group_data'] = success_data
        representation['error_group_data'] = error_data
        representation['success_group_data_with_transaction'] = success_thread_data
        representation['total_success_thread_count'] = total_success_thread_count
        representation['error_group_data_with_transaction'] = error_thread_data
        representation['total_error_thread_count'] = total_error_thread_count
        return representation

        
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

