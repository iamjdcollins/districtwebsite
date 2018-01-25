from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.apps import apps

class SAMLLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/?next=/'

class BaseURL(SAMLLoginRequiredMixin, RedirectView):

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:dashboard')

class Dashboard(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Alias = apps.get_model('multisite','alias')
        context['host'] = self.request.META['HTTP_HOST']
        env = context['host'].split('.')[0]
        if '-test' in env:
            context['sites'] = Alias.objects.filter(domain__icontains='-test')
        elif '-dev' in env:
            context['sites'] = Alias.objects.filter(domain__icontains='-dev')
        else:
            context['sites'] = Alias.objects.filter(is_canonical=True)
        return context
