from django.contrib import admin
from apps.server.models import Server


# Register your models here.
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    model = Server