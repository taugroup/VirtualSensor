from django.db import models
from django.core.validators import MaxValueValidator
from apps.core.models import CommonInfo

# Create your models here.
class Server(CommonInfo):
    address = models.CharField(max_length=256, null=True, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(65535)])
    bridge_port = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(65535)])
    username = models.CharField(max_length=256, null=True, blank=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    connection = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name
