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

def index(request):
    """
    Render the index view.
    :param request: Django request object.
    :return: Rendered template
    """
    return render(
        request,
        "compasweb/common/index.html",
    )

def about(request):
    """
    Render the about view.
    :param request: Django request object.
    :return: Rendered template
    """
    return render(
        request,
        "compasweb/common/about.html",
    )

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
