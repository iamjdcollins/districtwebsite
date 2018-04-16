from django import forms
from apps.dashboard.models import GeneralSettings, Template, PageLayout


class GeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = (
            'title',
            'template',
            'nd_statement',
            'ada_statement',
        )

    def __init__(self, *args, **kwargs):
        super(GeneralSettingsForm, self).__init__(*args, **kwargs)
        self.fields['template'].empty_label = 'Select Template'
        if kwargs['instance'].primary_domain != 'schools.slcschools.org':
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
        )

    def __init__(self, *args, **kwargs):
        super(SitesAddForm, self).__init__(*args, **kwargs)


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
