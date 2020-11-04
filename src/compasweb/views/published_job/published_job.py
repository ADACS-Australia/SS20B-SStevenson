# import logging
# logger = logging.getLogger(__name__)
# from django.http import Http404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.shortcuts import redirect, get_object_or_404
# from django.core.paginator import Paginator
# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from ...models import COMPASJob, Keyword, COMPASDatasetModel


class KeywordView(generic.ListView):
    """
    Display published dataset based on chosen keyword.
    """

    context_object_name = "jobs"
    ordering = "year"
    template_name = "compasweb/published_job/job_datasets.html"

    def get_queryset(self):
        return COMPASJob.filter_by_keyword(keyword=self.request.GET.get("keyword_filter")).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keyword_list"] = Keyword.objects.order_by("tag")
        context["keyword"] = self.request.GET.get("keyword_filter")
        return context


class DatasetDetailView(generic.DetailView):
    """
    Display details of a job. Currently largely a placeholder.
    """

    context_object_name = "job"
    model = COMPASJob
    template_name = "compasweb/published_job/dataset_detail.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["job"] = get_object_or_404(COMPASJob, id=self.kwargs["pk"])
            return context
        except Exception as e:
            print(e)
            return context


class ModelDetailView(generic.DetailView):
    """
    Display details of a chosen model. Currently it's a placeholder only.
    """

    context_object_name = "datasetmodel"
    model = COMPASDatasetModel
    template_name = "compasweb/published_job/model_detail.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context["datasetmodel"] = get_object_or_404(COMPASDatasetModel, id=self.kwargs["pk"])
            context["qs"] = context["datasetmodel"].get_rundetails().get()
            context["compas_setting"] = context["qs"].get_content()
            context["bokeh_autoload"] = context["qs"].get_plots()
            context["download_files"] = context["datasetmodel"].upload_set.all()
            context["data"] = context["datasetmodel"].get_data().get()
            context["stats"] = context["data"].read_stats()
            return context
        except Exception as e:
            print(e)
            return context

    # def job_table(request):


#
#     current_jobs = COMPASJob.objects.order_by('year')
#     keyword_list = Keyword.objects.order_by('tag')
#
#     return render(
#         request,
#         "compasweb/job/job_table.html",
#         {
#             'jobs': current_jobs,
#             'keywords': keyword_list
#         }
#     )
