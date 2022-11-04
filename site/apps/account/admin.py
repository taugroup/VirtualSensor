from django.contrib import admin
from apps.account.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
