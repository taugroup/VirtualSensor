import datetime

from django.db import models
from os import path
import time
from django.urls import reverse_lazy
from django.contrib.sites.models import Site
from django.shortcuts import reverse

from apps.core.models import CommonInfo
from apps.project.models import Project
from apps.input.models import Input
from apps.file.models import File
from apps.core.system import exec, symlink_all, get_upload_to
from settings.settings import MEDIA_ROOT
from django.core.mail import send_mail

TASK_STATUS = [
    ('running', 'Running'),
    ('queued', 'Queued'),
    ('finished', 'Finished'),
]


def deltatime2str(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]

    strings=[]
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value , seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)

class Task(CommonInfo):
    project = models.ForeignKey(Project, null=True, blank=False,
                                help_text="Required.", on_delete=models.CASCADE)
    input = models.ForeignKey(Input, null=True, blank=False,
                              help_text="Required.", on_delete=models.CASCADE)
    output = models.FileField(upload_to=get_upload_to, blank=True, max_length=512)
    exec_time = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(max_length=10, default="queued", choices=TASK_STATUS)

    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return self.name.strip()

    def get_absolute_url(self):
        return reverse('task_detail', args=[str(self.id)])

    def delete(self, *args, **kwargs):
        self.rmdir()
        super(Task, self).delete(*args, **kwargs)

    def process(self):
        cwd = MEDIA_ROOT / self.folder

        output = cwd / "output.txt"

        # cmd = "julia %s %s %s %s" % (jst, infile1, infile2, output)
        # cmd = "julia %s %s %s %s" % (jst, infile1, infile2, output)
        # cmd = "julia %s %s" % (jst, output)
        cmd = "sleep 40; cal > %s" % output
        # cmd = "sleep 10; cal>%s" % output

        self.status = "running"
        self.save()
        start = time.time()
        exec(cmd, cwd, block=True)
        self.exec_time = deltatime2str(datetime.timedelta(seconds=int(time.time() - start)))
        self.status = "finished"
        self.save()

        if path.exists(output):
            self.output = self.folder + "/" + "output.txt"
            self.save()

        current_site = Site.objects.get_current()

        send_mail(
            '[Simulocean Task] %s finished successfully!' % self.name,
            'Hi %s !\n\nYour task is done! Plesae visit %s%s to check your results.\n\nSimulocean Team' % (
                self.user, current_site, reverse_lazy('task_detail', args=[str(self.id)])),
            'simulocean@gmail.com',
            [self.user.email],
            fail_silently=False,
        )

        return

    def symlink(self):
        symlink_all(MEDIA_ROOT / self.input.folder, MEDIA_ROOT / self.folder)
