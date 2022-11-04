from apps.core.system import get_object_or_none
from django.db import IntegrityError
from django.utils.text import slugify
import os

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from apps.project.models import Project
from apps.input.models import Input

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class InputList(LoginRequiredMixin, ListView):
    model = Input

    def get_queryset(self):
        qs = super(InputList, self).get_queryset().order_by('-time_created')
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.INFO, "You have not created any inputs yet!")
        return qs


class InputDetail(LoginRequiredMixin, DetailView):
    model = Input

    def get_queryset(self):
        qs = super(InputDetail, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.ERROR, "Failed to find the requested input!")
        return qs


class InputCreate(LoginRequiredMixin, CreateView):
    model = Input
    fields = ['project', 'description']
    success_url = reverse_lazy('project_list')
    success_message = "Application input %(name)s was created successfully. Please don't forget to upload " \
                      "the input files before you submit a task."

    def get_initial(self):
        try:
            project = get_object_or_404(Project, pk=self.kwargs['pk'])
            return {
                "user": self.request.user,
                "project": project,
                # "application": self.request.user.profile.applications.all().first()
            }
        except:
            return {
                "user": self.request.user,
                "project": None
            }

    def form_valid(self, form):
        p = form.save(commit=False)
        if p.project.input_set.count() >= settings.PORTAL_MAX_NUMBER_INPUTS:
            messages.add_message(self.request, messages.ERROR, "One project can only have up to 4 inputs!")
            return self.form_invalid(form)
        try:
            p.user = self.request.user
            p.name = "%s-INPUT-%d" % (p.project.name, p.project.input_set.all().count() + 1)
            p.folder = os.path.normpath("%s/INPUT/%s" % (p.project.folder, p.name))
            p.mkdir()
            p.save()
            messages.add_message(self.request, messages.SUCCESS, "Input %s was created successfully." % p.name)
            logger.info("Input %s was created successfully." % p.name)
            return redirect(self.success_url)

        except IntegrityError:
            messages.add_message(self.request, messages.ERROR, "Input with this name already exists.")
            return self.form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )

    def get_context_data(self, **kwargs):
        context = super(InputCreate, self).get_context_data(**kwargs)

        projects = Project.objects.filter(user=self.request.user)
        if projects is not None:
            context['form'].fields['project'].queryset = projects
        else:
            messages.warning(self.request, "You will need to create a project first.")
        return context


class InputUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Input
    fields = ['description']
    success_url = reverse_lazy('input_list')
    success_message = "Input %(name)s was updated successfully."

    def get_queryset(self):
        qs = super(InputUpdate, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class InputDelete(LoginRequiredMixin, DeleteView):
    model = Input
    success_url = reverse_lazy('input_list')

    def get_queryset(self):
        qs = super(InputDelete, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        p = get_object_or_none(self)

        if p is not None:
            p.rmdir()
            success_message = "Input %s was deleted successfully." % p.name
            messages.success(self.request, success_message)
            logger.info("Input %s was deleted." % p.name)
        return super(InputDelete, self).delete(request, *args, **kwargs)
