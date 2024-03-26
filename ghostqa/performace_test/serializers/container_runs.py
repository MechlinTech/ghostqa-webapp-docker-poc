from rest_framework import serializers
from ..models import TestContainersRuns



class ContainersRunsSerializers(serializers.Serializer):
    
    
    class Meta:
        model = TestContainersRuns
        fields = "__all__"
        