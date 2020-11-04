from django.urls import reverse
from django.test import TestCase, Client


class PublishedDatasetsViewsTest(TestCase):
    # Use this fixture to populate test database
    fixtures = ["test_data.json"]
    client = Client()

    def test_published_job_view(self):
        response = self.client.get(reverse("published_job"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "compasweb/published_job/job_datasets.html")

    def test_published_job_view_with_keyword_filter(self):
        response = self.client.get(reverse("published_job", kwargs={"keyword_filter": "BBH"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "compasweb/published_job/job_datasets.html")

    def test_dataset_detail_view(self):
        response = self.client.get(reverse("dataset_detail", kwargs={"pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "compasweb/published_job/dataset_detail.html")

    def test_dataset_detail_view_non_existing_dataset(self):
        response = self.client.get(reverse("dataset_detail", kwargs={"pk": "5"}))
        self.assertEqual(response.status_code, 404)

    # def test_dataset_detail_view_no_dataset_id(self):
    #     response = self.client.get(reverse("dataset_detail"))
    #     self.assertEqual(response.status_code, 200)
