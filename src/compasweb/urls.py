from django.conf.urls import url
from .views.jobs import job_table
urlpatterns = [
    url(r'^$', job_table, name='jobtable'),
]