from django.conf.urls import url
from django.urls import path
from .views.job.jobs import KeywordView

urlpatterns = [
    url(r"^$", KeywordView.as_view(), name="jobtable"),
    path("<str:keyword_filter>/", KeywordView.as_view(), name="jobtable"),
]
