from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

class SAMLLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/?next=/'

class BaseURL(SAMLLoginRequiredMixin, RedirectView):

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:dashboard')

class Dashboard(SAMLLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Welcome to ' + request.site.name + '\'s Dashboard')
