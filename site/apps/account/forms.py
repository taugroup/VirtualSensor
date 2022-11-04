from apps.account.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
