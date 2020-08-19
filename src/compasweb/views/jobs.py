# import logging
# logger = logging.getLogger(__name__)
# from django.http import Http404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# from django.shortcuts import redirect, get_object_or_404
# from django.core.paginator import Paginator

from django.shortcuts import render
from ..models import COMPASJob

def job_table(request):
    """
    Collects all public jobs and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    current_jobs = COMPASJob.objects.order_by('creation_time')

    return render(
        request,
        "compasweb/job_table.html",
        {
            'jobs': current_jobs
        }
    )