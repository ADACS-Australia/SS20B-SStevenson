from django.db import models


class Keyword(models.Model):
    tag = models.CharField(max_length=255, blank=False, null=False)


class COMPASJob(models.Model):
    author = models.CharField(max_length=255, blank=False, null=False)
    # published defines if the job was published in a journal/arxiv
    published = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    year = models.IntegerField(null=True)
    journal = models.CharField(max_length=255, null=True)
    journal_DOI = models.CharField(max_length=255, null=True)
    dataset_DOI = models.CharField(max_length=255, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    # public defines if the job is publicly accessible
    public = models.BooleanField(default=False)
    download_link = models.TextField(blank=True, null=True)
    arxiv_id = models.CharField(max_length=255, blank=False)
    keywords = models.ManyToManyField(Keyword)

