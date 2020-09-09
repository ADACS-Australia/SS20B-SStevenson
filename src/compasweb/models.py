import os
from django.conf import settings
from django.db import models

import tarfile

class Keyword(models.Model):
    tag = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.tag


def job_directory_path(instance, filename):
    """
    a callable to generate a custom directory path to upload file to
    instance: an instance of the model to which the file belongs
    filename: name of the file to be uploaded
    """
    # change file name if it has spaces
    fname = filename.replace(" ", "_")
    # Use Dataset DOI as directory name for dataset files, replace any slashes with dots
    dir_name = instance.dataset_DOI.replace("/", ".")
    # dataset files will be saved in MEDIA_ROOT/datasets/dataset.doi/
    return "{0}/{1}".format(f"datasets/{dir_name}", fname)


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
    # filefield to upload dataset files compressed in a tarball
    files = models.FileField(upload_to=job_directory_path, blank=True, null=True)

    @classmethod
    def filter_by_keyword(cls, keyword=None):
        return (
            cls.objects.all().filter(keywords__tag=keyword)
            if keyword
            else cls.objects.all()
        )

    def save(self, *args, **kwargs):
        """
        overwrites default save behavior
        """
        super().save(*args, **kwargs)
        # Check file name is not empty after saving the model and uploading file
        if self.files.name:
            self.decompress_tar_file()
        

    def decompress_tar_file(self):
        # Get the actual path for uploaded file
        dataset_tar_path = os.path.join(settings.MEDIA_ROOT, self.files.name)
        # Get the parent directory to compress the tarball into
        dataset_dir = os.path.dirname(dataset_tar_path)
        # Check the uploaded file could be decompressed using tarfile
        if tarfile.is_tarfile(dataset_tar_path):
            dataset_tar = tarfile.open(dataset_tar_path)
            dataset_tar.extractall(dataset_dir)
            dataset_tar.close()
            # remove the tar file after decompression
            os.remove(dataset_tar_path)

    def get_available_files(self):
        listing = []
        if self.files.name:
            dataset_tar_path = os.path.join(settings.MEDIA_ROOT, self.files.name)
            dataset_dir = os.path.dirname(dataset_tar_path)
            listing = os.listdir(dataset_dir)
        return listing

