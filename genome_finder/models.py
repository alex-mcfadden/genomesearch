from django.db import models

# Create your models here.

class Job(models.Model):
    sequence = models.CharField(max_length=1000)
    genome_name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    startbp = models.IntegerField()
    endbp = models.IntegerField()

