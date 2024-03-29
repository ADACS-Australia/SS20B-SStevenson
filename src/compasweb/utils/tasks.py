from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.conf import settings
import os
import subprocess
import traceback

from .celery_single_sys_plotter import main
from .celery_pythonSubmit import run_compas_cmd
from .constants import TASK_SUCCESS, TASK_FAIL, TASK_FAIL_OTHER
from celery.exceptions import TaskRevokedError, SoftTimeLimitExceeded
from .handle_tar_files import compress_files_into_tarball


def check_output_file_generated(outputfilepath):
    """
    Check if the job finished successfully by checking that output file is created
    This will keep running until file is created or timeout otherwise
    :param outputfilepath: full path of output file
    :return:
    """
    created = False
    # keep checking until output file is generated
    while not created:
        created = os.path.exists(outputfilepath)

    return TASK_SUCCESS


@shared_task
def run_compas(grid_file_path, output_path, detailed_output_file_path):

    result = None
    try:
        run_compas_cmd(grid_file_path, output_path)
        result = check_output_file_generated(detailed_output_file_path)

    except SoftTimeLimitExceeded as timeout_err:
        # If job timed out, clean up output directory
        cleanup_timeout_task(outputfilepath)
        print(timeout_err)
        result = TASK_TIMEOUT

    except Exception as e:
        # return fail code if job failed for some other reason
        print(e)
        result = TASK_FAIL
    # An example of adding in another error (would need to go above Exception above)
    except TaskRevokedError as revoked_err:
        print(revoked_err)
        result = TASK_FAIL_OTHER
    finally:
        return result


@shared_task
def run_plotting(jobstate, detailed_output_file_path, plot_path):

    if jobstate == TASK_SUCCESS:
        # sending output file path to generate the plot into
        # TODO: modify it to work with compas running in Docker

        result = None
        try:
            main(detailed_output_file_path, plot_path)
            result = check_output_file_generated(plot_path)
        except Exception as e:
            print(e)
            result = TASK_FAIL
        finally:
            return result

    elif jobstate == TASK_FAIL or jobstate == TASK_TIMEOUT:
        print("COMPAS Model didn't run successfully! Couldn't generate plot")
        return TASK_FAIL


@shared_task
def compress_output(jobstate, output_path, tar_file_path):

    result = None
    if jobstate == TASK_SUCCESS:
        try:
            compress_files_into_tarball(output_path, tar_file_path)
            # result = check_output_file_generated(tar_file_path)
        except Exception as e:
            print(e)
            # result = TASK_FAIL
        finally:
            return TASK_SUCCESS


@shared_task
def test_task(model_id):
    print(f"Task Recieved: {model_id}")
