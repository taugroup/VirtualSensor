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
from django_q.tasks import async_task
from django.conf import settings

from apps.task.models import Task
from apps.project.models import Project
from apps.input.models import Input
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TaskList(LoginRequiredMixin, ListView):
    model = Task

    def get_queryset(self):
        qs = super(TaskList, self).get_queryset().order_by('-time_created')
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.INFO, "You have not created any tasks yet!")
        return qs


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task

    def get_queryset(self):
        qs = super(TaskDetail, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.ERROR, "Failed to find the requested task!")
        return qs


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['project', 'input', 'description']
    success_url = reverse_lazy('project_list')

    def get_initial(self, *args, **kwargs):
        initial = super(TaskCreate, self).get_initial()
        try:
            project = get_object_or_404(Project, pk=self.kwargs['pk'])
            initial["user"] = self.request.user
            initial["project"] = project
            initial["input"] = project.input_set.first()
        except:
            initial["user"] = self.request.user
            initial["project"] = None
        return initial

    def form_valid(self, form):
        t = form.save(commit=False)
        if t.project.task_set.count() >= settings.PORTAL_MAX_NUMBER_TASKS:
            messages.add_message(self.request, messages.ERROR,
                                 "One project can only have up to one task. You already have %s tasks." % t.project.task_set.count())
            return self.form_invalid(form)

        if t.input.project != t.project:
            messages.error(self.request,
                           "Please select the input from the same project! The name of the input starts with the project name.")
            return self.form_invalid(form)

        if t.input.file_set.all():
            try:
                t.user = self.request.user
                t.name = "%s-TASK-%d" % (t.project.name, t.project.task_set.count() + 1)
                t.folder = os.path.normpath("%s/TASK/%s" % (t.project.folder, t.name))
                t.save()
                t.mkdir()
                logger.info("created symbolic links for application input files")
                t.symlink()
                async_task(t.process)
                return super(TaskCreate, self).form_valid(form)

            except IntegrityError:
                t.delete()
                messages.error(self.request, "Task with this name already exists.")
                logger.error("Task with this name already exists.")
                return self.form_invalid(form)
        else:
            messages.error(self.request, "The application input is empty. Please upload input files first.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        try:
            project = get_object_or_404(Project, pk=kwargs['pk'])
            context['form'].fields['project'].queryset = Project.objects.filter(project=project)
            context['form'].fields['input'].queryset = project.input_set.filter(project=project)
        except:
            context['form'].fields['project'].queryset = Project.objects.filter(user=self.request.user)
            context['form'].fields['input'].queryset = Input.objects.filter(user=self.request.user)
        return context


class TaskUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['description']
    success_url = reverse_lazy('project_list')
    success_message = "Task %(name)s was updated successfully."

    def get_queryset(self):
        qs = super(TaskUpdate, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('project_list')

    def get_queryset(self):
        qs = super(TaskDelete, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        p = get_object_or_none(self)

        if p:
            p.rmdir()
            success_message = "Task %s was deleted successfully." % p.name
            messages.success(self.request, success_message)
            logger.info("Task %s was deleted." % p.name)
        return super(TaskDelete, self).delete(request, *args, **kwargs)
