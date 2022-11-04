from django.contrib import admin
from apps.input.models import Input


# Register your models here.

@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    model = Input
