from django.db import models
import uuid
# Create your models here.

class PerformaceTestSuite(models.Model):
    test_file = models.FileField(upload_to='uploads/performace_tests/')  # You may want to specify a custom upload_to path
    name = models.CharField(max_length=1000)
    client_reference_id = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    jthreads_total_user = models.CharField(max_length=250, null=True, blank=True, default='1') 
    jrampup_time = models.IntegerField(null=True, blank=True, default=1)  # in seconds
    jrampup_steps = models.IntegerField(null=True, blank=True, default=1)
    durations = models.IntegerField(null=True, blank=True, default=1)  # in seconds
    
class JmeterTestConfig(models.Model):
    duration = models.FileField(upload_to='uploads/performace_tests/')  # You may want to specify a custom upload_to path
    total_number_of_users = models.CharField(max_length=1000)
    ramp_up_time = models.CharField(max_length=250, null=True, blank=True)
    ramp_up_steps = models.CharField(max_length=250, null=True, blank=True)
    jthreads = models.CharField(max_length=250, null=True, blank=True)
    jrampup = models.CharField(max_length=250, null=True, blank=True)
    
    

class TestContainersRuns(models.Model):
    suite = models.ForeignKey(PerformaceTestSuite,on_delete=models.CASCADE,related_name='container_runs')
    container_id  = models.CharField(max_length=255, null=True)
    container_status  = models.CharField(max_length=255, null=True)
    container_labels  = models.CharField(max_length=255, null=True)
    container_name  = models.CharField(max_length=255, null=True)
    container_short_id  = models.CharField(max_length=255, null=True)
    container_logs_str = models.TextField(null=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    json = models.JSONField(null = True)
    raw_data = models.JSONField(null = True)
    test_file = models.FileField(upload_to='uploads/performace_tests/TestContainersRuns/',null=True)  # You may want to specify a custom upload_to path
    client_reference_id = models.CharField(max_length=250, null=True, blank=True)

   
class TestArtifacts(models.Model):
    container_runs = models.ForeignKey(TestContainersRuns,on_delete=models.CASCADE,related_name='runs_artifacts')
    suite = models.ForeignKey(PerformaceTestSuite,on_delete=models.CASCADE,related_name='suite_artifacts')
    type =models.CharField(max_length=255, null=True)
    files = models.FileField(upload_to='uploads/performace_tests/')
    