from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from ...models import COMPASModelRun
from ...forms.model_parameters import COMPASModelRunForm


def run_compas_model(request):

    if request.method == "POST":
        form = COMPASModelRunForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            job_id = form.instance.id

            return redirect(reverse("compas_model_output", args=(job_id,)))
        else:
            messages.error(request, 'Please fix errors before proceeding')
            return render(request, "compasweb/run_model/model_parameters.html", {'run_model_form': form})

    form = COMPASModelRunForm()
    return render(request, "compasweb/run_model/model_parameters.html", {'run_model_form': form})


def compas_model_output(request, job_id):
    return HttpResponse(f'You run job with id {job_id}')
