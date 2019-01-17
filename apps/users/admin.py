from django import forms
from django.contrib.auth import get_permission_codename
from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Employee, System
from django.utils import timezone
from guardian.admin import GuardedModelAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from apps.common.classes import DeletedListFilter
from apps.common.actions import trash_selected, restore_selected, publish_selected, unpublish_selected
from django.contrib.admin.actions import delete_selected
from apps.objects.models import Node
from apps.images.models import ProfilePicture
import apps.common.functions
from django.contrib.sites.models import Site

class ProfilePictureInlineForm(forms.ModelForm):
    class Meta:
        model = ProfilePicture
        fields = [
            'title',
            'site',
            'image_file',
            'alttext',
        ]

    def __init__(self, *args, **kwargs):
        super(ProfilePictureInlineForm, self).__init__(*args, **kwargs)
        district = Site.objects.get(domain='www.slcschools.org')
        self.fields['title'].initial = '{0} {1}'.format(self.parent.first_name, self.parent.last_name)
        self.fields['alttext'].initial = '{0} {1}'.format(self.parent.first_name, self.parent.last_name)
        self.fields['site'].initial = district
        self.fields['title'].widget = forms.HiddenInput()
        self.fields['alttext'].widget = forms.HiddenInput()
        self.fields['site'].widget = forms.HiddenInput()


class ProfilePictureInline(admin.StackedInline):
    model = ProfilePicture
    form = ProfilePictureInlineForm
    fk_name = 'parent'
    fields = ['title','site','image_file','alttext',]
    extra = 0
    min_num = 0
    max_num = 1
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_formset(self, request, obj=None, **kwargs):
        self.form.parent = obj
        self.form.request = request
        return super().get_formset(request, obj, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)

class EmployeeAdminChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeAdminChangeForm, self).__init__(*args, **kwargs)
        if self.instance:
            try:
                self.fields['department'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='school') | Q(content_type='department')).order_by('node_title')
            except KeyError:
                pass

    class Meta(UserChangeForm.Meta):
        model = Employee

class EmployeeAdminAdmin(UserAdmin):
    form = EmployeeAdminChangeForm

    inlines = [ProfilePictureInline,]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(EmployeeAdminAdmin, self).get_fieldsets(request, obj)
        if not request.user.is_superuser:
            return []
        fieldsets = fieldsets + (
            ('Department/Job Title', {'fields': ('department','job_title')}),
        )
        return fieldsets

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    #has_delete_permission = apps.common.functions.has_delete_permission
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change


class SystemAdminAdmin(UserAdmin):
  pass

admin.site.register(Employee, EmployeeAdminAdmin)
admin.site.register(System, SystemAdminAdmin)
