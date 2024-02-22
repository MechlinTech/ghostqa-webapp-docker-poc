from django.db import models

# Create your models here.


class TestSuite(models.Model):
    name = models.CharField(max_length=1000)