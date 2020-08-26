from django.conf.urls import url
from .views.job.jobs import KeywordView

urlpatterns = [
    url(r'^$', KeywordView.as_view(), name='jobtable'),
]