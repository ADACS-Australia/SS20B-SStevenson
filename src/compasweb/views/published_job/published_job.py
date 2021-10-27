from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import TemplateResponseMixin
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

def placeholder_functional_view(request, **kwargs):
    print(request, kwargs)

    context = {}
    context["datasetmodel"] = get_object_or_404(COMPASDatasetModel, id=kwargs["pk"])
    datafile = context["datasetmodel"].get_data().get()

    if request.method == "POST":
        print("POST REQ")
        if request.POST.get("main_group"):
            resp = datafile.return_react_subgroup(request)
            return JsonResponse(resp)
        
        if request.POST.get("data_request"):
            resp = datafile.return_react_data(request)
            return JsonResponse(resp)

    if request.method == 'GET':
        print('here')
        try:
            user_agent_str = request.META.get("HTTP_USER_AGENT", None)
            if user_agent_str:
                user_agent = user_agents.parse(user_agent_str)
                is_mobile = user_agent.is_mobile
            else:
                is_mobile = False
            context["react_menu"] = datafile.get_react_keys()
            context["download_files"] = context["datasetmodel"].upload_set.all()
            context["stats"] = datafile.read_stats()
            context["kwargs_id"] = kwargs["pk"]

            return render(request, "compasweb/published_job/model_detail.html", context)
        except Exception as e:
            print(e)
            return render(request, "compasweb/published_job/model_detail.html", context)
    
    return 'Broked'

class ModelCustomView(generic.View):

    def get(self, request, *args, **kwargs):
        print(request, 'getthis')
        try:
            print(kwargs)
            context = {}
            context["datasetmodel"] = get_object_or_404(COMPASDatasetModel, id=kwargs["pk"])
            datafile = context["datasetmodel"].get_data().get()
            user_agent_str = request.META.get("HTTP_USER_AGENT", None)
            if user_agent_str:
                user_agent = user_agents.parse(user_agent_str)
                is_mobile = user_agent.is_mobile
            else:
                is_mobile = False
            context["react_menu"] = datafile.get_react_keys()
            context["download_files"] = context["datasetmodel"].upload_set.all()
            context["stats"] = datafile.read_stats()

            return render(request, "compasweb/published_job/model_detail.html", context)
        except Exception as e:
            print(e)
            return render(request, "compasweb/published_job/model_detail.html", context)

    def post(self, request, *args, **kwargs):
        print('poststhis', request)
        return 0

class ModelDetailView(generic.DetailView):
    """
    Display details of a chosen model. Currently it's a placeholder only.
    """

    context_object_name = "datasetmodel"
    model = COMPASDatasetModel
    template_name = "compasweb/published_job/model_detail.html"

    def get_context_data(self, **kwargs):
        print(self.request)
        try:
            context = super().get_context_data(**kwargs)
            context["datasetmodel"] = get_object_or_404(COMPASDatasetModel, id=self.kwargs["pk"])
            datafile = context["datasetmodel"].get_data().get()
            user_agent_str = self.request.META.get("HTTP_USER_AGENT", None)
            if user_agent_str:
                user_agent = user_agents.parse(user_agent_str)
                is_mobile = user_agent.is_mobile
            else:
                is_mobile = False
            context["react_menu"] = datafile.get_react_keys()
            context["download_files"] = context["datasetmodel"].upload_set.all()
            context["stats"] = datafile.read_stats()

            if self.request.method == "POST":
                print("POST REQ")
                if self.request.POST.get("main_group"):
                    context["subgroup_list"] = datafile.return_react_subgroup(self.request)
                
                if self.request.POST.get("data_request"):
                    context["react_data"] = datafile.return_react_data(self.request)

            return context
        except Exception as e:
            print(e)
            return context
