from django.db import models

# Create your models here.
from apps.account.models import User
from django.contrib.auth.models import Group
from apps.core.system import mkdir_p, rmdir
from settings.settings import MEDIA_ROOT


class CommonInfo(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)
    folder = models.CharField(max_length=200, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def get_absolute_path(self):
        if self.folder:
            return MEDIA_ROOT / self.folder

    def mkdir(self):
        if self.folder:
            mkdir_p(self.get_absolute_path())

    def rmdir(self):
        if self.folder:
            rmdir(self.get_absolute_path())

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
        # return self._meta.get_fields(include_hidden=False)
        # return [(field.name, field.value(self)) for field in self._meta.fields]
        # return self._meta.get_fields()