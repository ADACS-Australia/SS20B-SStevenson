import os

from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from celery import chain
from ...models import COMPASModelRun
from ...forms.model_parameters import COMPASModelRunForm
from compasweb.utils.tasks import test_task, run_compas, run_plotting, compress_output
from ...utils.constants import TASK_FAIL, TASK_FAIL_OTHER, TASK_SUCCESS, TASK_RUNNING, TASK_TIMEOUT
from ...utils.handle_tar_files import compress_files_into_tarball


def run_compas_model(request):

    request.session.flush()
    if request.method == "POST":

        form = COMPASModelRunForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            model_id = form.instance.id
            return redirect(reverse("compas_model_output", args=(model_id,)))
        else:
            messages.error(request, 'Please fix errors before proceeding')
            return render(request, "compasweb/run_model/model_parameters.html", {'run_model_form': form})

    form = COMPASModelRunForm()
    return render(request, "compasweb/run_model/model_parameters.html", {'run_model_form': form})


def compas_model_output(request, model_id):

    model = get_object_or_404(COMPASModelRun, id=model_id)
    model_id = str(model.id)

    # form grid file path
    grid_file_path = os.path.join(settings.COMPAS_IO_PATH, model_id, 'BSE_grid.txt')
    output_path = os.path.join(settings.COMPAS_IO_PATH, model_id)
    detailed_output_file_path = os.path.join(
        settings.COMPAS_IO_PATH, model_id, 'COMPAS_Output', 'Detailed_Output', 'BSE_Detailed_Output_0.h5'
    )
    plot_path = os.path.join(settings.COMPAS_IO_PATH, model_id, 'COMPAS_Output', 'Detailed_Output', 'gw151226evol.png')
    tar_file_path = output_path + ".tar.gz"

    run_details_url = None
    plot_url = None
    output_url = None
    grid_file_url = None
    detailed_output_url = None

    result = None
    error_code = 0

    # saves job information to session if it's not there yet
    # this runs when first loading output view

    if model_id not in request.session:
        task = chain(
            run_compas.s(grid_file_path, output_path, detailed_output_file_path),
            run_plotting.s(detailed_output_file_path, plot_path),
            compress_output.s(output_path, tar_file_path),
        )()

        request.session[model_id] = task.id
        request.session['reloads_count'] = 3
    else:
        task = run_compas.AsyncResult(request.session[model_id])
        reloads_count = request.session['reloads_count']
        request.session['reloads_count'] = reloads_count - 1

    # get task result
    result = task.get()

    grid_file_url = f'jobs/{model_id}/BSE_grid.txt'
    run_details_url = f'jobs/{model_id}/COMPAS_Output/Run_Details'

    # set output file url if the job succeeded, otherwise it will be None
    if result == TASK_SUCCESS:
        plot_url = f'jobs/{model_id}/COMPAS_Output/Detailed_Output/gw151226evol.png'
        output_url = f'jobs/{model_id}/COMPAS_Output/COMPAS_Output.h5'
        detailed_output_url = f'jobs/{model_id}/COMPAS_Output/Detailed_Output/BSE_Detailed_Output_0.h5'

        if not os.path.exists(plot_path):
            plot_url = None

    # Updating error codes according to task state to display proper text in template
    elif result == TASK_TIMEOUT:
        error_code = 2
    elif result == TASK_FAIL:
        error_code = 1
    # example of another failure/error type
    elif result == TASK_FAIL_OTHER:
        error_code = 3
    return render(
        request,
        "compasweb/run_model/compas_model_output.html",
        {
            'model': model,
            'error_code': error_code,
            'run_details': run_details_url,
            'output': output_url,
            'grid': grid_file_url,
            'detailed_output': detailed_output_url,
            'plot': plot_url,
        },
    )


def download_compas_output_as_tar(request, model_id):

    model_id = str(model_id)
    # path to compas model directory where all output files exist
    tar_file_path = os.path.join(settings.COMPAS_IO_PATH, (model_id + ".tar.gz"))
    outputtarfile = open(file=tar_file_path, mode="rb")
    response = HttpResponse(outputtarfile, 'application/tar+gzip')
    response['Content-Disposition'] = 'attachment; filename="output.tar.gz"'

    return response
