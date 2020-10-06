from django.conf.urls import url
from django.urls import path, re_path
from .views.published_job.published_job import KeywordView, JobDetailView
from .views.common import index

urlpatterns = [
    url(r"^$", index, name="homepage"),
    url(r"^/published/", KeywordView.as_view(), name="published_job"),
    path("<str:keyword_filter>/", KeywordView.as_view(), name="published_job"),
    path(r"<int:pk>", JobDetailView.as_view(), name="job_detail"),
]
