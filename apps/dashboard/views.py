from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.urls import reverse
from django.apps import apps
from apps.objects.models import User
from apps.dashboard.forms import (
    GeneralSettingsForm,
    SitesAddForm,
    SitesChangeForm,
    SiteTypesAddForm,
    SiteTypesChangeForm,
    SiteTypesRequiredPagesForm,
    TemplatesAddForm,
    PageLayoutsAddForm,
    PageLayoutsChangeForm,
    SitePublishersAddForm,
    SitePublishersChangeForm,
)
from apps.dashboard.models import (
    GeneralSettings as GeneralSettingsModel,
    SiteType as SiteTypeModel,
    SiteTypeRequiredPage as SiteTypeRequiredPageModel,
    Template as TemplateModel,
    PageLayout as PageLayoutsModel,
    SitePublisher as SitePublisherModel,
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


def add_sitetypes_context(self, context):
    context['sitetypes'] = SiteTypeModel.objects.all().order_by('title')
    return context


def add_templates_context(self, context):
    context['templates'] = TemplateModel.objects.all().order_by('title')
    return context


def add_pagelayouts_context(self, context):
    context['pagelayouts'] = PageLayoutsModel.objects.all().order_by('title')
    return context


def add_sitepublishers_context(self, context):
    context['sitepublishers'] = SitePublisherModel.objects.filter(site=self.request.site).order_by('account')
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


def add_siteschange_form(self, context):
    try:
        instance = GeneralSettingsModel.objects.get(pk=self.kwargs['sitepk'])
    except GeneralSettingsModel.DoesNotExist:
        raise Exception('Site Does Not Exist')
    if self.request.POST:
        context['siteschangeform'] = SitesChangeForm(
            instance=instance,
            data=self.request.POST,
        )
    else:
        context['siteschangeform'] = SitesChangeForm(
            instance=instance,
        )
    return context


def add_sitetypesadd_form(self, context):
    if self.request.POST:
        context['sitetypesaddform'] = SiteTypesAddForm(
            data=self.request.POST,
        )
    else:
        context['sitetypesaddform'] = SiteTypesAddForm()
    return context


def add_sitetypeschange_form(self, context):
    try:
        instance = SiteTypeModel.objects.get(pk=self.kwargs['sitetypepk'])
    except SiteTypeModel.DoesNotExist:
        raise Exception('Site Type Does Not Exist')
    RequiredPagesFormSet = modelformset_factory(
        SiteTypeRequiredPageModel,
        form=SiteTypesRequiredPagesForm,
    )
    if self.request.POST:
        context['sitetypeschangeform'] = SiteTypesChangeForm(
            instance=instance,
            data=self.request.POST,
        )
        context['requiredpagesformset'] = RequiredPagesFormSet(data=self.request.POST)
    else:
        context['sitetypeschangeform'] = SiteTypesChangeForm(
            instance=instance,
        )
        context['requiredpagesformset'] = RequiredPagesFormSet(queryset=SiteTypeRequiredPageModel.objects.filter(sitetype=instance))
        for form in context['requiredpagesformset']:
            form.fields['pagelayout'].queryset = instance.dashboard_pagelayout_allowed_sitetypes.all().order_by('title')
            form.fields['parent'].queryset = instance.dashboard_sitetyperequiredpage_sitetype.all().order_by('title')
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


def add_pagelayoutschange_form(self, context):
    try:
        instance = PageLayoutsModel.objects.get(pk=self.kwargs['pagelayoutpk'])
    except PageLayoutsModel.DoesNotExist:
        raise Exception('Page Layout Does Not Exist')
    if self.request.POST:
        context['pagelayoutschangeform'] = PageLayoutsChangeForm(
            instance=instance,
            data=self.request.POST,
        )
    else:
        context['pagelayoutschangeform'] = PageLayoutsChangeForm(
            instance=instance,
        )
    return context


def add_sitepublishersadd_form(self, context):
    if self.request.POST:
        context['sitepublishersaddform'] = SitePublishersAddForm(
            data=self.request.POST,
        )
    else:
        context['sitepublishersaddform'] = SitePublishersAddForm()
    return context


def add_sitepublisherschange_form(self, context):
    try:
        instance = SitePublisherModel.objects.get(pk=self.kwargs['sitepublisherpk'])
    except SitePublisherModel.DoesNotExist:
        raise Exception('Site Publisher Does Not Exist')
    if self.request.POST:
        context['sitepublisherschangeform'] = SitePublishersChangeForm(
            instance=instance,
            data=self.request.POST,
        )
    else:
        context['sitepublisherschangeform'] = SitePublishersChangeForm(
            instance=instance,
        )
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
        if request.site.domain != 'websites.slcschools.org':
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
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitesadd_form(self, context)
        return context


class SitesChange(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/siteschange.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['siteschangeform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['siteschangeform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Site updated successfully')
        return redirect('dashboard:sites')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_siteschange_form(self, context)
        return context


class SiteTypes(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitetypes.html'

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitetypes_context(self, context)
        return context


class SiteTypesAdd(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitetypesadd.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['sitetypesaddform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['sitetypesaddform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Site Type added successfully')
        return redirect('dashboard:sitetypes')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitetypes_context(self, context)
        context = add_sitetypesadd_form(self, context)
        return context


class SiteTypesChange(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitetypeschange.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['sitetypeschangeform'].is_valid() and context['requiredpagesformset'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['sitetypeschangeform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Site Type updated successfully')
            context['requiredpagesformset'].save(commit=False)
            for obj in context['requiredpagesformset'].deleted_objects:
                obj.delete()
            for obj in context['requiredpagesformset'].new_objects:
                obj.create_user = request.user
                obj.update_user = request.user
                obj.sitetype = post
                obj.save()
            for obj in context['requiredpagesformset'].changed_objects:
                obj[0].update_user = request.user
                obj[0].save()
            context['requiredpagesformset'].save_m2m()
        return redirect('dashboard:sitetypes')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitetypes_context(self, context)
        context = add_sitetypeschange_form(self, context)
        return context


class Templates(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/templates.html'

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'websites.slcschools.org':
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
        if request.site.domain != 'websites.slcschools.org':
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
        if request.site.domain != 'websites.slcschools.org':
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
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_pagelayoutsadd_form(self, context)
        return context


class PageLayoutsChange(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/pagelayoutschange.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['pagelayoutschangeform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['pagelayoutschangeform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Page layout updated successfully')
            context['pagelayoutschangeform'].save_m2m()
        return redirect('dashboard:pagelayouts')

    def get(self, request, *args, **kwargs):
        if request.site.domain != 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        # raise Exception('Error')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_pagelayoutschange_form(self, context)
        return context


class SitePublishers(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitepublishers.html'

    def get(self, request, *args, **kwargs):
        if request.site.domain == 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitepublishers_context(self, context)
        return context


class SitePublishersAdd(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitepublishersadd.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['sitepublishersaddform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['sitepublishersaddform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            post.site = request.site
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Site Publisher added successfully')
        return redirect('dashboard:sitepublishers')

    def get(self, request, *args, **kwargs):
        if request.site.domain == 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitepublishersadd_form(self, context)
        return context


class SitePublishersChange(SAMLLoginRequiredMixin, TemplateView):

    template_name = 'cmstemplates/dashboard/sitepublisherschange.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['sitepublisherschangeform'].is_valid():
            user = User.objects.get(pk=request.user.pk)
            post = context['sitepublisherschangeform'].save(commit=False)
            if not post.create_user:
                post.create_user = user
            if not post.site:
                post.site = request.site
            post.update_user = user
            post.save()
            messages.success(
                request,
                'Site Publisher updated successfully')
            context['sitepublisherschangeform'].save_m2m()
        return redirect('dashboard:sitepublishers')

    def get(self, request, *args, **kwargs):
        if request.site.domain == 'websites.slcschools.org':
            return BaseURL.as_view()(self.request)
        context = self.get_context_data()
        # raise Exception('Error')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_sites_context(self, context)
        context = add_sitepublisherschange_form(self, context)
        return context

