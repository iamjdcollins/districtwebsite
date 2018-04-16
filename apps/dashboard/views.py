from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.apps import apps
from apps.objects.models import User
from apps.dashboard.forms import (
    GeneralSettingsForm,
    SitesAddForm,
    TemplatesAddForm,
    PageLayoutsAddForm,
)
from apps.dashboard.models import (
    GeneralSettings as GeneralSettingsModel,
    Template as TemplateModel,
    PageLayout as PageLayoutsModel,
)


def add_sites_context(self, context):
    Alias = apps.get_model('multisite', 'alias')
    context['host'] = self.request.META['HTTP_HOST']
    env = context['host'].split('.')[0]
    if '-test' in env:
        context['sites'] = (
            Alias
            .objects
            .filter(domain__icontains='-test')
            .order_by('domain')
        )
    elif '-dev' in env:
        context['sites'] = (
            Alias
            .objects
            .filter(domain__icontains='-dev')
            .order_by('domain')
        )
    else:
        context['sites'] = (
            Alias
            .objects
            .filter(is_canonical=True)
            .order_by('domain')
        )
    return context


def add_templates_context(self, context):
    context['templates'] = TemplateModel.objects.all()
    return context


def add_pagelayouts_context(self, context):
    context['pagelayouts'] = PageLayoutsModel.objects.all()
    return context


def add_general_settings_form(self, context):
    instance = GeneralSettingsModel.objects.get(site=self.request.site)
    if self.request.POST:
        context['generalsettingsform'] = GeneralSettingsForm(
            data=self.request.POST,
            instance=instance,
        )
    else:
        context['generalsettingsform'] = GeneralSettingsForm(instance=instance)
    return context


def add_sitesadd_form(self, context):
    if self.request.POST:
        context['sitesaddform'] = SitesAddForm(
            data=self.request.POST,
        )
    else:
        context['sitesaddform'] = SitesAddForm()
    return context


def add_templatesadd_form(self, context):
    if self.request.POST:
        context['templatesaddform'] = TemplatesAddForm(
            data=self.request.POST,
        )
    else:
        context['templatesaddform'] = TemplatesAddForm()
    return context


def add_pagelayoutsadd_form(self, context):
    if self.request.POST:
        context['pagelayoutsaddform'] = PageLayoutsAddForm(
            data=self.request.POST,
        )
    else:
        context['pagelayoutsaddform'] = PageLayoutsAddForm()
    return context


class SAMLLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/accounts/login/?next=/'


class BaseURL(SAMLLoginRequiredMixin, RedirectView):

    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('dashboard:dashboard')


class Dashboard(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        return context


class GeneralSettings(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/general.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['generalsettingsform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['generalsettingsform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Settings updated successfully')
        return redirect('dashboard:general')

    def get(self, request, *args, **kwargs):
        model, created = GeneralSettingsModel.objects.get_or_create(
            site=request.site
        )
        if created:
            model.create_user = request.user
            model.update_user = request.user
            model.save()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_general_settings_form(self, context)
        return context


class Sites(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sites.html'

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'schools.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        return context


class SitesAdd(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitesadd.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['sitesaddform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['sitesaddform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Site added successfully')
        return redirect('dashboard:sites')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'schools.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitesadd_form(self, context)
        return context


class Templates(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/templates.html'

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'schools.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_templates_context(self, context)
        return context


class TemplatesAdd(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/templatesadd.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['templatesaddform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['templatesaddform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Template added successfully')
        return redirect('dashboard:templates')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'schools.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_templatesadd_form(self, context)
        return context


class PageLayouts(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/pagelayouts.html'

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'schools.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_pagelayouts_context(self, context)
        return context


class PageLayoutsAdd(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/pagelayoutsadd.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['pagelayoutsaddform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['pagelayoutsaddform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Page layout added successfully')
        return redirect('dashboard:pagelayouts')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'schools.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_pagelayoutsadd_form(self, context)
        return context
