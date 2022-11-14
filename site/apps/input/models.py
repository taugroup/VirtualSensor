from django.db import models
from django.shortcuts import reverse
from apps.core.models import CommonInfo
from apps.sensor.models import Sensor


class Input(CommonInfo):
    project = models.ForeignKey(Sensor, null=True, blank=False,
                                help_text="Required.", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("name", "user")
        verbose_name = "Input Files"

    def __str__(self):
        return self.name.strip()

    def get_absolute_url(self):
        return reverse('input_detail', args=[str(self.id)])

    def delete(self, *args, **kwargs):
        self.rmdir()
        super(Input, self).delete(*args, **kwargs)
