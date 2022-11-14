from django.shortcuts import render, get_object_or_404, redirect

from settings.settings import MEDIA_ROOT
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.sensor.models import Sensor
from apps.file.models import File

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def post(request, sensor, file_list):
    file_names = []
    succeed = False
    file_names = [_f._name for _f in file_list]
    file_name = file_names[0]
    #
    # num_files = len(file_list)

    # only allowed to upload once
    # if input.file_set.count() >= settings.PORTAL_MAX_NUMBER_FILES_PER_INPUT:
    #     messages.add_message(request, messages.ERROR, "No more files are allowed for this input!")
    #     return

    # only allow two files
    # if num_files > settings.PORTAL_MAX_NUMBER_FILES_PER_INPUT or num_files == 0:
    #     messages.add_message(request, messages.ERROR, "Please upload up to 5 files.")
    #     succeed = False
    # else:
    #     for fn in file_names:
    if file_name.endswith('.csv') or file_name.endswith('.json'):
        succeed = True
    else:
        messages.add_message(request, messages.ERROR, "Only CSV and JSON files are supported!")
        succeed = False

    if succeed:
        # for f in file_list:
        try:
            File(
                user=request.user,
                name=file_name,
                file=file_list[0],
                folder=sensor.folder,
                sensor=sensor,
            ).save()
        except:
            messages.add_message(request, messages.ERROR, "Failed to upload files!")

        messages.add_message(request, messages.SUCCESS, "Upload files successfully!")
    return


@login_required
def file_create(request, *args, **kwargs):
    sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
    context = {
        'file': File.objects.filter(sensor=sensor),
        'sensor': sensor
    }
    if request.method == 'POST':
        if request.FILES.get("file_list"):
            file_list = request.FILES
            post(request, input, file_list)

    return render(request, 'file/file_form.html', context)


@login_required
def file_delete(request, *args, **kwargs):
    p = get_object_or_404(File, pk=kwargs['pk'])
    sensor = p.sensor
    try:
        if p:
            success_message = "File %s was deleted successfully!" % p.name
            messages.success(request, success_message)
            logger.info("File %s was deleted." % p.name)
            p.delete()
    except:
        messages.error(request, "Failed to delete %s!" % p.name)
        pass
    return redirect('file_create', sensor.id)
