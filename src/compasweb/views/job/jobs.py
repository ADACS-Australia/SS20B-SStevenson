# import logging
# logger = logging.getLogger(__name__)
# from django.http import Http404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.shortcuts import redirect, get_object_or_404
# from django.core.paginator import Paginator

from django.shortcuts import render
from django.views import generic
from ...models import COMPASJob, Keyword


class KeywordView(generic.ListView):
    """
    Display job based on chosen keyword.
    """

    context_object_name = "jobs"
    ordering = "year"
    template_name = "compasweb/job/job_table.html"

    def get_queryset(self):
        return COMPASJob.filter_by_keyword(
            keyword=self.request.GET.get("keyword_filter")
        ).order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keyword_list"] = Keyword.objects.order_by("tag")
        context["keyword"] = self.request.GET.get("keyword_filter")
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
