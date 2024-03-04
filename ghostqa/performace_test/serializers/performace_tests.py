from rest_framework import serializers

from ..models import PerformaceTestSuite


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
        fields = ["id","name", "jrampup","jthreads","test_file", "client_reference_id", "container_runs","type"]
        read_only_fields = ["id","type","container_runs"]

