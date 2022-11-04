from django.shortcuts import render, get_object_or_404, redirect

from settings.settings import MEDIA_ROOT
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.input.models import Input
from apps.file.models import File

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def post(request, input, file_list):
    files = []
    succeed = False

    file_names = [_f._name for _f in file_list]

    num_files = len(file_list)

    # only allowed to upload once
    if input.file_set.count() >= settings.PORTAL_MAX_NUMBER_FILES_PER_INPUT:
        messages.add_message(request, messages.ERROR, "No more files are allowed for this input!")
        return

    # only allow two files
    if num_files > settings.PORTAL_MAX_NUMBER_FILES_PER_INPUT or num_files == 0:
        messages.add_message(request, messages.ERROR, "Please upload up to two files, X1.csv and/or X2.csv!")
        succeed = False
    else:
        if num_files == settings.PORTAL_MAX_NUMBER_FILES_PER_INPUT:
            if 'X1.csv' in file_names and "X2.csv" in file_names:
                succeed = True
            else:
                messages.add_message(request, messages.ERROR,
                                     "When uploading two files, the file names must be X1.csv and X2.csv!")
                succeed = False
        elif num_files == 1:
            if 'X1.csv' in file_names:
                succeed = True
            else:
                messages.add_message(request, messages.ERROR,
                                     "If uploading only one file, the file name must be X1.csv!")
                succeed = False

    if succeed:
        for f in file_list:
            try:
                files.append(File(
                    user=request.user,
                    name=f._name,
                    file=f,
                    folder=input.folder,
                    input=input,
                ))
            except:
                messages.add_message(request, messages.ERROR, "Failed to upload files!")
        File.objects.bulk_create(files)
        messages.add_message(request, messages.SUCCESS, "Upload files successfully!")
    return


@login_required
def file_create(request, *args, **kwargs):
    input = get_object_or_404(Input, pk=kwargs['pk'])
    context = {
        'file_list': File.objects.filter(input=input),
        'input': input
    }
    if request.method == 'POST':
        if request.FILES.get("file_list"):
            file_list = request.FILES.getlist("file_list")
            post(request, input, file_list)

    return render(request, 'file/file_form.html', context)


@login_required
def file_delete(request, *args, **kwargs):
    p = get_object_or_404(File, pk=kwargs['pk'])
    input = p.input
    try:
        if p:
            success_message = "File %s was deleted successfully!" % p.name
            messages.success(request, success_message)
            logger.info("File %s was deleted." % p.name)
            p.delete()
    except:
        messages.error(request, "Failed to delete %s!" % p.name)
        pass
    return redirect('file_create', input.id)
