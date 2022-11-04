from django.contrib import admin
from apps.file.models import File


# Register your models here.

@admin.register(File)
class InputAdmin(admin.ModelAdmin):
    model = File
