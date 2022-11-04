from django.db import models

# Create your models here.
from django.shortcuts import reverse
from apps.core.models import CommonInfo

class Project(CommonInfo):
    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

    def delete(self, *args, **kwargs):
        for t in self.task_set.all():
            t.delete()
        for ai in self.input_set.all():
            ai.delete()
        self.rmdir()
        super(Project, self).delete(*args, **kwargs)
