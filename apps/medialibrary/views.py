from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class SAMLLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/?next=/'


class BaseURL(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'medialibrary/browser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['node'] = self.request.META['HTTP_REFERER']
        return context
