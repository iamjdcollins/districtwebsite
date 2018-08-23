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

class ProfilePictureInline(admin.StackedInline):
    model = ProfilePicture
    fk_name = 'parent'
    fields = ['title','site','image_file','alttext',]
    extra = 0
    min_num = 1
    max_num = 1

class EmployeeAdminChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeAdminChangeForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['department'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='school') | Q(content_type='department')).order_by('node_title')

    class Meta(UserChangeForm.Meta):
        model = Employee

class EmployeeAdminAdmin(UserAdmin):
    form = EmployeeAdminChangeForm

    inlines = [ProfilePictureInline,]

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('department','job_title')}),
        )

class SystemAdminAdmin(UserAdmin):
  pass

admin.site.register(Employee, EmployeeAdminAdmin)
admin.site.register(System, SystemAdminAdmin)
