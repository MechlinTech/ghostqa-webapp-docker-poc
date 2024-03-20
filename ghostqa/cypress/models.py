from django.db import models
import uuid
# Create your models here.



class TestSuite(models.Model):
    scenarios_file = models.FileField(upload_to='uploads/scenarios_file/', blank=True, null=True)  # You may want to specify a custom upload_to path
    name = models.CharField(max_length=1000)
    client_reference_id = models.CharField(max_length=250, null=True, blank=True)
    cypress_code = models.TextField(null=True, blank=True)
    request_json = models.JSONField(null=True, blank=True)

class TestContainersRuns(models.Model):
    suite = models.ForeignKey(TestSuite,on_delete=models.CASCADE,related_name='container_runs')
    container_id  = models.CharField(max_length=255, null=True)
    container_status  = models.CharField(max_length=255, null=True)
    container_labels  = models.CharField(max_length=255, null=True)
    container_name  = models.CharField(max_length=255, null=True)
    container_short_id  = models.CharField(max_length=255, null=True)
    container_logs_str = models.TextField(null=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    json = models.JSONField(null = True)
    
    

    
class TestArtifacts(models.Model):
    container_runs = models.ForeignKey(TestContainersRuns,on_delete=models.CASCADE,related_name='runs_artifacts')
    suite = models.ForeignKey(TestSuite,on_delete=models.CASCADE,related_name='suite_artifacts')
    type =models.CharField(max_length=255, null=True)
    files = models.FileField(upload_to='uploads/artifacts/')
    