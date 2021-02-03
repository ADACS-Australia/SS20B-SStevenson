import tempfile
import os
import shutil
import tarfile

from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile

from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.test import TestCase, Client
from django.test import override_settings

from ..models import COMPASJob, Keyword, COMPASModel, COMPASDatasetModel, Upload


class BaseModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        creating two tags and two jobs
        """
        super(BaseModelTestCase, cls).setUpClass()
        cls.keyword1 = Keyword(tag="BBH")
        cls.keyword1.save()
        cls.keyword2 = Keyword(tag="CE")
        cls.keyword2.save()

        cls.job1 = COMPASJob(
            author="Vigna-G\u00f3mez",
            published=True,
            title="On the formation history of Galactic double neutron stars",
            year=2018,
            journal="MNRAS",
            journal_DOI="10.1093/mnras/sty2463",
            dataset_DOI="10.5281/zenodo.3358304",
            creation_time="2020-08-26T20:53:11.702Z",
            description="",
            public=True,
            download_link="zenodo arxiv",
            arxiv_id="1805.07974",
        )
        cls.job1.save()
        cls.job1.keywords.add(cls.keyword1)  # BBH
        cls.job1.save()

        cls.job2 = COMPASJob(
            author="van Son et al.",
            published=True,
            title="Polluting the pair-instability mass gap for binary black holes through super-Eddington accretion in isolated binaries",
            year=2020,
            journal="ApJ",
            journal_DOI="10.3847/1538-4357/ab9809",
            dataset_DOI="10.5281/zenodo.3871801",
            creation_time="2020-08-26T20:53:11.657Z",
            description="",
            public=True,
            download_link="zenodo arxiv",
            arxiv_id="2004.05187",
        )
        cls.job2.save()
        cls.job2.keywords.add(cls.keyword2)  # CE
        cls.job2.keywords.add(cls.keyword1)  # BBH
        cls.job2.save()

        cls.compasmodel1 = COMPASModel(
            name="Feducial",
            summary="Feducial Summary",
            description="Feducial Description",
        )
        cls.compasmodel1.save()

        cls.datasetmodel1 = COMPASDatasetModel(
            compasjob=cls.job1,
            compasmodel=cls.compasmodel1,
        )
        cls.datasetmodel1.save()


class KeywordModelTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEqual(self.keyword1.tag, "BBH")
        self.assertEqual(self.keyword2.tag, "CE")


class COMPASJobModelTestCase(BaseModelTestCase):
    # Use this fixture to populate test database
    # fixtures = ["test_data.json"]

    def test_created_properly(self):
        self.assertEqual(2, len(self.job2.keywords.all()))
        self.assertEqual(len(COMPASJob.objects.filter(keywords__tag="BBH")), 2)

    def test_keyword_filter(self):
        self.assertEqual(len(COMPASJob.filter_by_keyword("CE")), 1)

    # overrides the media root setting for testing purpose
    @override_settings(MEDIA_ROOT="/tmp/django_test")
    def test_upload_file_creates_dataset_media_directory(self):
        """
        Uploading a simple text file on the fly
        """
        filename = "myfile.txt"
        self.datasetmodel1.files = SimpleUploadedFile(filename, b"these are the file contents!")
        self.datasetmodel1.save()

        filepath = f"datasets/{self.job1.id}/{self.compasmodel1.id}/{filename}"

        self.assertEqual(self.datasetmodel1.files, filepath)

        dataset_file_path = os.path.join(settings.MEDIA_ROOT, self.datasetmodel1.files.name)
        self.assertEqual(os.path.exists(dataset_file_path), True)
        self.assertEqual(len(Upload.objects.filter(file__icontains=filepath)), 1)

    @override_settings(MEDIA_ROOT="/tmp/django_test")
    def test_upload_tarball(self):
        """
        Create a tarball on the fly with 2 text files
        Upload them to one of the jobs
        Check the file is uploaded and decompressed successfully then removed
        """
        # coverage reportprint(os.getcwd())
        # filename = tempfile.mkstemp()[1]
        filename = "file1.txt"
        f = open(filename, "w")
        f.write("These are the file contents")
        f.close()
        print()

        # filename1 = tempfile.mkstemp()[1]
        filename1 = "file2.txt"
        f1 = open(filename1, "w")
        f1.write("These are the file contents")
        f1.close()

        # Use absolute path to make sure UploadedFile uses the right directory (MEDIA_ROOT)
        tarfilepath = os.path.join(os.getcwd(), "test.tar.gz")
        tf = tarfile.open(tarfilepath, mode="w:gz")
        tf.add(filename)
        tf.add(filename1)
        tf.close()

        self.datasetmodel1.files = UploadedFile(
            file=open(file=tarfilepath, mode="rb")  # , content_type="application/gzip",
        )
        self.datasetmodel1.save()

        os.remove(filename)
        os.remove(filename1)
        os.remove(tarfilepath)

        dataset_file_path = os.path.join(settings.MEDIA_ROOT, self.datasetmodel1.files.name)
        dir_name = os.path.dirname(dataset_file_path)

        self.assertEqual(
            self.datasetmodel1.files,
            f"datasets/{self.job1.id}/{self.compasmodel1.id}/test.tar.gz",
        )
        self.assertEqual(os.path.exists(os.path.join(dir_name, filename)), True)
        self.assertEqual(os.path.exists(os.path.join(dir_name, filename1)), True)
        self.assertEqual(os.path.exists(dataset_file_path), False)

        file_path = f"datasets/{self.job1.id}/{self.compasmodel1.id}/{filename}"
        file_path1 = f"datasets/{self.job1.id}/{self.compasmodel1.id}/{filename1}"
        self.assertEqual(len(Upload.objects.filter(file__icontains=file_path1)), 1)
        self.assertEqual(len(Upload.objects.filter(file__icontains=file_path)), 1)

    @override_settings(MEDIA_ROOT="/tmp/django_test")
    def test_upload_tarball_with_subdirectory(self):
        """
        Create a tarball on the fly with a text file in a subdirectory
        Upload them to one of the jobs
        Check the file is uploaded and decompressed successfully then removed
        """
        dirname = "testdir"
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        filename = "file1.txt"
        f = open(os.path.join(dirname, filename), "w")
        f.write("These are the file contents")
        f.close()
        print()

        # Use absolute path to make sure UploadedFile uses the right directory (MEDIA_ROOT)
        tarfilepath = os.path.join(os.getcwd(), "test.tar.gz")
        tf = tarfile.open(tarfilepath, mode="w:gz")
        tf.add(dirname)
        tf.close()

        self.datasetmodel1.files = UploadedFile(
            file=open(file=tarfilepath, mode="rb")  # , content_type="application/gzip",
        )
        self.datasetmodel1.save()

        shutil.rmtree(dirname)
        os.remove(tarfilepath)

        dataset_file_path = os.path.join(settings.MEDIA_ROOT, self.datasetmodel1.files.name)
        dir_name = os.path.dirname(dataset_file_path)

        self.assertEqual(
            self.datasetmodel1.files,
            f"datasets/{self.job1.id}/{self.compasmodel1.id}/test.tar.gz",
        )
        self.assertEqual(os.path.exists(os.path.join(dir_name, dirname, filename)), True)
        self.assertEqual(os.path.exists(dataset_file_path), False)

        file_path = f"datasets/{self.job1.id}/{self.compasmodel1.id}/{dirname}/{filename}"
        self.assertEqual(len(Upload.objects.filter(file__icontains=file_path)), 1)

    @classmethod
    @override_settings(MEDIA_ROOT="/tmp/django_test")
    def tearDownClass(cls):
        """
        Removes all media files from temp MEDIA ROOT
        """
        shutil.rmtree(
            os.path.join(settings.MEDIA_ROOT, "datasets"),
            ignore_errors=False,
            onerror=None,
        )
