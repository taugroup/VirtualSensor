from apps.core.system import get_object_or_none
from django.db import IntegrityError
from django.utils.text import slugify
import os

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin

from apps.project.models import Project

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProjectList(LoginRequiredMixin, ListView):
    model = Project

    def get_queryset(self):
        qs = super(ProjectList, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.INFO, "You have not created any projects yet!")
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        context["max_number_inputs"] = settings.PORTAL_MAX_NUMBER_INPUTS
        return context


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project

    def get_queryset(self):
        qs = super(ProjectDetail, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.ERROR, "Failed to find the requested project!")
        return qs

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context["max_number_inputs"] = settings.PORTAL_MAX_NUMBER_INPUTS
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description']
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        p = form.save(commit=False)
        if not p.name.isalnum():
            messages.add_message(self.request, messages.ERROR, "Project name must be alphanumeric.")
            return self.form_invalid(form)
        try:
            p.user = self.request.user
            p.folder = os.path.normpath("users/%s/%s" % (slugify(p.user.username), p.name))
            p.mkdir()
            p.save()
            messages.add_message(self.request, messages.SUCCESS, "Project %s was created successfully." % p.name)
            logger.info("Project %s was created successfully." % p.name)
            return redirect(self.success_url)

        except IntegrityError:
            messages.add_message(self.request, messages.ERROR, "Project with this name already exists.")
            return self.form_invalid(form)


class ProjectUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    fields = ['description']
    success_url = reverse_lazy('project_list')
    success_message = "Project %(name)s was updated successfully."

    def get_queryset(self):
        qs = super(ProjectUpdate, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')

    def get_queryset(self):
        qs = super(ProjectDelete, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        p = get_object_or_none(self)

        if p:
            p.rmdir()
            success_message = "Project %s was deleted successfully." % p.name
            messages.success(self.request, success_message)
            logger.info("Project %s was deleted." % p.name)
        return super(ProjectDelete, self).delete(request, *args, **kwargs)
