from rest_framework import viewsets
from ..models import TestContainersRuns

from ..serializers.performace_tests import TestContainersRunsSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ContainersRunsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TestContainersRuns.objects.all()
    serializer_class = TestContainersRunsSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'container_id','client_reference_id','container_id']
    ordering_fields = ['container_name', 'id']
    ordering = ['id','container_name']