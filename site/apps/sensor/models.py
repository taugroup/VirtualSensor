import os.path

from django.db import models
from django.conf import settings
from settings.settings import MEDIA_ROOT
# Create your models here.
from django.shortcuts import reverse
from apps.core.models import CommonInfo
from apps.server.models import Server
from apps.core.system import get_upload_to

from apps.core.TAUVirtualSensor import VirtualSensor

class Sensor(CommonInfo):
    file = models.FileField(upload_to=get_upload_to, blank=True, max_length=512)
    file_type = models.CharField(max_length=16, null=True, blank=True)
    topic = models.CharField(max_length=200, null=True, blank=True)
    fields = models.CharField(max_length=4096, null=True, blank=True)
    server = models.ForeignKey(Server, blank=True, null=True, on_delete=models.CASCADE)
    published = models.BooleanField(default=False, verbose_name="publish now")

    class Meta:
        unique_together = ("name", "user")

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def get_absolute_url(self):
        return reverse('sensor_detail', args=[str(self.id)])

    def publish(self):
        if not self.published:
            try:
                vs = VirtualSensor()
                if self.file_type == 'csv':
                    vs = self.read_csv()
                elif self.file_type == 'json':
                    vs = self.read_json()
                vs.publish()
                self.published = True
                self.save()
            except:
                pass

    def read_csv(self):
        address = self.server.address
        port = self.server.port
        vs = VirtualSensor(address, port=port, delimiter=';',
                           filepath=str(MEDIA_ROOT)+'/'+self.file.name,
                           interval=5)
        vs.read_csv()
        return vs

    def read_json(self, filepath):
        address = self.server.address
        port = self.server.port
        vs = VirtualSensor(address, port=port, filepath=filepath, interval=5)
        vs.read_json()
        return vs

    def delete(self, *args, **kwargs):
        self.rmdir()
        super(Sensor, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name