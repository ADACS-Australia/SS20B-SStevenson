from django.shortcuts import render, get_object_or_404
from django.views import generic
from ...models import COMPASJob, Keyword, COMPASDatasetModel

import user_agents


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
            datafile = context["datasetmodel"].get_data().get()
            user_agent_str = self.request.META.get("HTTP_USER_AGENT", None)
            if user_agent_str:
                user_agent = user_agents.parse(user_agent_str)
                is_mobile = user_agent.is_mobile
            else:
                is_mobile = False
            context["bokeh_autoload"] = context["qs"].get_plots(datafile.file.path, is_mobile=is_mobile)
            context["download_files"] = context["datasetmodel"].upload_set.all()
            context["stats"] = datafile.read_stats()
            return context
        except Exception as e:
            print(e)
            return context
