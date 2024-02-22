
from rest_framework import serializers



class ExecuteSerializers(serializers.Serializer):
    upload_file = serializers.FileField()
    name = serializers.CharField(max_length=1000)