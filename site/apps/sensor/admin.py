from django.contrib import admin
from apps.sensor.models import Sensor


# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    model = Sensor
