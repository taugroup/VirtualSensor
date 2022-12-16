from apps.core.system import get_object_or_none
from django.db import IntegrityError
from django.utils.text import slugify
import os, json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django_q.tasks import async_task

from apps.sensor.models import Sensor

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SensorList(LoginRequiredMixin, ListView):
    model = Sensor

    def get_queryset(self):
        qs = super(SensorList, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.INFO, "You have not created any sensors yet!")
        return qs

    def get_context_data(self, **kwargs):
        context = super(SensorList, self).get_context_data(**kwargs)
        # context["max_number_inputs"] = settings.PORTAL_MAX_NUMBER_INPUTS
        return context


class SensorDetail(LoginRequiredMixin, DetailView):
    model = Sensor

    def get_queryset(self):
        qs = super(SensorDetail, self).get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        if not qs:
            messages.add_message(self.request, messages.ERROR, "Failed to find the requested sensor!")
        return qs

    def get_context_data(self, **kwargs):
        context = super(SensorDetail, self).get_context_data(**kwargs)
        # context["max_number_inputs"] = settings.PORTAL_MAX_NUMBER_INPUTS
        return context


class SensorCreate(LoginRequiredMixin, CreateView):
    model = Sensor
    fields = ['name', 'file', 'server', 'description', 'published']
    success_url = reverse_lazy('sensor_list')

    def form_valid(self, form):
        p = form.save(commit=False)

        if not p.name.isalnum():
            messages.add_message(self.request, messages.ERROR, "Sensor name must be alphanumeric.")
            return self.form_invalid(form)

        if p.file.name.lower().endswith('.csv'):
            p.file_type = 'csv'
        elif p.file.name.lower().endswith('.json'):
            p.file_type = 'json'
        else:
            messages.add_message(self.request, messages.ERROR, "Only CSV and JSON files are supported!")
            return self.form_invalid(form)

        try:
            p.user = self.request.user
            p.folder = os.path.normpath("users/%s/%s" % (slugify(p.user.username), p.name))
            p.mkdir()
            p.save()
            vs = p.read_csv()
            p.topic = vs.topic
            p.fields = vs.fields
            p.save()
            if p.published:
                async_task(p.publish())

            messages.add_message(self.request, messages.SUCCESS, "Sensor %s was created successfully." % p.name)
            logger.info("Sensor %s was created successfully." % p.name)
            return redirect(self.success_url)

        except IntegrityError:
            messages.add_message(self.request, messages.ERROR, "Sensor with this name already exists.")
            return self.form_invalid(form)

class SensorUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sensor
    fields = ['file','description', 'published']
    success_url = reverse_lazy('sensor_list')
    success_message = "Sensor %(name)s was updated successfully."

    def form_valid(self, form):
        p = form.save(commit=False)

        if not p.name.isalnum():
            messages.add_message(self.request, messages.ERROR, "Sensor name must be alphanumeric.")
            return self.form_invalid(form)

        if p.file.name.endswith('.csv') or p.file.name.endswith('.json'):
            pass
        else:
            messages.add_message(self.request, messages.ERROR, "Only CSV and JSON files are supported!")
            return self.form_invalid(form)

        try:
            p.user = self.request.user
            p.folder = os.path.normpath("users/%s/%s" % (slugify(p.user.username), p.name))
            p.mkdir()
            p.save()
            vs = p.read_csv()
            p.topic = vs.topic
            p.fields = vs.fields
            p.save()

            if p.published:
                async_task(p.publish())

            messages.add_message(self.request, messages.SUCCESS, "Sensor %s was created successfully." % p.name)
            logger.info("Sensor %s was created successfully." % p.name)
            return redirect(self.success_url)

        except IntegrityError:
            messages.add_message(self.request, messages.ERROR, "Sensor with this name already exists.")
            return self.form_invalid(form)

    def get_queryset(self):
        qs = super(SensorUpdate, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )

class SensorDelete(DeleteView):
    model = Sensor
    success_url = reverse_lazy('sensor_list')

    def get_queryset(self):
        qs = super(SensorDelete, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        p = get_object_or_none(self)

        if p:
            p.rmdir()
            success_message = "Sensor %s was deleted successfully." % p.name
            messages.success(self.request, success_message)
            logger.info("Sensor %s was deleted." % p.name)
        return super(SensorDelete, self).delete(request, *args, **kwargs)