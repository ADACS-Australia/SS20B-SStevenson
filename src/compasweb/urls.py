from django.conf.urls import url
from django.urls import path, re_path
from .views.published_job.published_job import KeywordView, DatasetDetailView, ModelDetailView
from .views.common import index, about
from .views.compas_model_run.compas_model_run import run_compas_model, compas_model_output

urlpatterns = [
    url(r"^$", index, name="homepage"),
    url(r"^about/", about, name="about"),
    path("published/", KeywordView.as_view(), name="published_job"),
    path("published/<str:keyword_filter>/", KeywordView.as_view(), name="published_job"),
    path("dataset/<int:pk>/", DatasetDetailView.as_view(), name="dataset_detail",),
    path("model/<int:pk>/", ModelDetailView.as_view(), name="model_detail"),
    path("model/new/", run_compas_model, name="run_compas_model"),
    path("model/output/<int:job_id>/", compas_model_output, name="compas_model_output"),
]
