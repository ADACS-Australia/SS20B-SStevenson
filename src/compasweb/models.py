from django.db import models

# Create your models here.
class COMPASJob(models.Model):
    author = models.CharField(max_length=255, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField()
    public = models.BooleanField(default=False)
    download_link = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("name", "version")
