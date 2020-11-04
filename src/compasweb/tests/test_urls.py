from django.urls import reverse, resolve

from django.test import TestCase

from ..views.common import about, index
from ..views.published_job.published_job import KeywordView, DatasetDetailView


class TestURLs(TestCase):
    def test_published_datasets_url_resolves(self):
        url = reverse("published_job")
        self.assertEqual(type(resolve(url).func.view_class()), KeywordView)

    def test_published_datasets_with_keyword_url_resolves(self):
        url = reverse("published_job", kwargs={"keyword_filter": "BBH"})
        self.assertEqual(type(resolve(url).func.view_class()), KeywordView)

    def test_dataset_details_url_resolves(self):
        url = reverse("dataset_detail", kwargs={"pk": 1})
        self.assertEqual(type(resolve(url).func.view_class()), DatasetDetailView)

    def test_about_url_resolves(self):
        url = reverse("about")
        self.assertEqual(resolve(url).func, about)

    def test_index_url_resolves(self):
        url = reverse("homepage")
        self.assertEqual(resolve(url).func, index)
