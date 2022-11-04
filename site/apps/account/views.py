from django.views.generic import CreateView
from apps.account.forms import AccountCreationForm
from django.shortcuts import reverse


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = AccountCreationForm

    def get_success_url(self):
        return reverse("login")
