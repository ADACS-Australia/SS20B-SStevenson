from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.conf import settings
import os
import subprocess

from compas.demo_single_sys_plotter import main


@shared_task
def run_compas(parameterfilepath, outputfilepath):
    result = None

    command = settings.RUN_COMPAS_COMMAND

    command.append(parameterfilepath)

    subprocess.call(command)


@shared_task
def run_plotting():

    main()
