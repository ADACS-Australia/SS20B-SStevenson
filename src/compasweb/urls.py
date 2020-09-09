from django.conf.urls import url
from django.urls import path, re_path
from .views.job.jobs import KeywordView, JobDetailView

urlpatterns = [
    url(r"^$", KeywordView.as_view(), name="jobtable"),
    path("<str:keyword_filter>/", KeywordView.as_view(), name="jobtable"),
    path(r"<int:pk>", JobDetailView.as_view(), name="job_detail"),
]
