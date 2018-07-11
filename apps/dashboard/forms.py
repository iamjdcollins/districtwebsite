from django import forms
from ajax_select.fields import AutoCompleteSelectField
from apps.dashboard.models import GeneralSettings, SiteType, Template, PageLayout, SiteTypeRequiredPage


class GeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = (
            'title',
            'primary_contact',
            'main_phone',
            'main_fax',
            'location',
            'template',
            'nd_statement',
            'ada_statement',
            'global_facebook',
            'global_twitter',
            'global_instagram',
            'global_youtube',
        )

    primary_contact = AutoCompleteSelectField('employee', help_text='')

    def __init__(self, *args, **kwargs):
        super(GeneralSettingsForm, self).__init__(*args, **kwargs)
        self.fields['template'].empty_label = 'Select Template'
        if kwargs['instance'].primary_domain != 'websites.slcschools.org':
            self.fields['nd_statement'].widget = forms.Textarea()
            self.fields['nd_statement'].disabled = True
            self.fields['ada_statement'].widget = forms.Textarea()
            self.fields['ada_statement'].disabled = True


class SitesAddForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = (
            'title',
            'primary_domain',
            'namespace',
            'sitetype',
            'gatrackingid',
            'monsido_domaintoken',
        )

    def __init__(self, *args, **kwargs):
        super(SitesAddForm, self).__init__(*args, **kwargs)


class SitesChangeForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = (
            'title',
            'primary_domain',
            'namespace',
            'sitetype',
            'gatrackingid',
            'monsido_domaintoken',
        )

    def __init__(self, *args, **kwargs):
        super(SitesChangeForm, self).__init__(*args, **kwargs)


class SiteTypesAddForm(forms.ModelForm):
    class Meta:
        model = SiteType
        fields = (
            'title',
        )

    def __init__(self, *args, **kwargs):
        super(SiteTypesAddForm, self).__init__(*args, **kwargs)


class SiteTypesChangeForm(forms.ModelForm):

    class Meta:
        model = SiteType
        fields = (
            'title',
        )

    def __init__(self, *args, **kwargs):
        super(SiteTypesChangeForm, self).__init__(*args, **kwargs)


class SiteTypesRequiredPagesForm(forms.ModelForm):

    class Meta:
        model = SiteTypeRequiredPage
        fields = (
            'title',
            'menu_item',
            'menu_title',
            'pagelayout',
            'parent',
        )

    def __init__(self, *args, **kwargs):
        super(SiteTypesRequiredPagesForm, self).__init__(*args, **kwargs)


class TemplatesAddForm(forms.ModelForm):

    class Meta:
        model = Template
        fields = (
            'title',
            'namespace',
        )

    def __init__(self, *args, **kwargs):
        super(TemplatesAddForm, self).__init__(*args, **kwargs)


class PageLayoutsAddForm(forms.ModelForm):
    class Meta:
        model = PageLayout
        fields = (
            'title',
            'namespace',
        )

    def __init__(self, *args, **kwargs):
        super(PageLayoutsAddForm, self).__init__(*args, **kwargs)


class PageLayoutsChangeForm(forms.ModelForm):

    class Meta:
        model = PageLayout
        fields = (
            'title',
            'namespace',
            'allowed_sitetypes',
        )

    def __init__(self, *args, **kwargs):
        super(PageLayoutsChangeForm, self).__init__(*args, **kwargs)
