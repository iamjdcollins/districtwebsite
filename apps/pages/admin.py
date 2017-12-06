from django.conf import settings
from django import forms
from django.db.models import Q
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import get_permission_codename
from guardian.admin import GuardedModelAdmin
from mptt.admin import MPTTModelAdmin
from ajax_select import make_ajax_form, make_ajax_field
from apps.common.classes import DeletedListFilter, EditLinkToInlineObject
from apps.common.actions import trash_selected, restore_selected, publish_selected, unpublish_selected
from django.contrib.admin.actions import delete_selected
from .models import Page, School, Department, Board, BoardSubPage, News, NewsYear, SubPage
from apps.images.models import Thumbnail, NewsThumbnail, ContentBanner, ProfilePicture
from apps.directoryentries.models import SchoolAdministrator, Staff, BoardMember, StudentBoardMember, BoardPolicyAdmin
from apps.links.models import ResourceLink
from apps.documents.models import Document, BoardPolicy, Policy, AdministrativeProcedure, SupportingDocument
from apps.files.models import File
from apps.objects.models import Node
import apps.common.functions

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class ProfilePictureInline(admin.StackedInline):
    model = ProfilePicture
    fk_name = 'parent'
    fields = ['title','image_file','alttext',]
    extra = 0
    min_num = 1
    max_num = 1

class ThumbnailInline(admin.TabularInline):
  model = Thumbnail
  fk_name = 'parent'
  fields = ['title','image_file','alttext',]
  readonly_fields = []
  extra = 0 
  min_num = 0
  max_num = 1
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class NewsThumbnailInline(admin.TabularInline):
  model = NewsThumbnail
  fk_name = 'parent'
  fields = ['title','image_file','alttext',]
  readonly_fields = []
  extra = 0
  min_num = 0
  max_num = 1
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class ContentBannerInline(admin.TabularInline):
  model = ContentBanner
  fk_name = 'parent'
  fields = ['title','image_file','alttext',]
  readonly_fields = []
  extra = 0 
  min_num = 0
  max_num = 5
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class SchoolAdministratorInline(admin.TabularInline):
  model = SchoolAdministrator
  fk_name = 'parent'
  fields = ['employee', 'schooladministratortype',]
  readonly_fields = []
  extra = 0 
  min_num = 0
  max_num = 5
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

  form = make_ajax_form(SchoolAdministrator, {'employee': 'employee'})

class StaffInline(admin.TabularInline):
  model = Staff
  fk_name = 'parent'
  fields = ['employee','job_title',]
  readonly_fields = []
  ordering = ['title',]
  extra = 0
  min_num = 0
  max_num = 50
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

  form = make_ajax_form(Staff, {'employee': 'employee'})

class StudentBoardMemberInlineForm(forms.ModelForm):
    class Meta:
        model = StudentBoardMember
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(StudentBoardMemberInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class StudentBoardMemberInline(EditLinkToInlineObject, admin.TabularInline):
  model = StudentBoardMember
  form = StudentBoardMemberInlineForm
  fk_name = 'parent'
  fields = ['title','edit_link']
  readonly_fields = ['edit_link']
  ordering = ['title',]
  extra = 0
  min_num = 0
  max_num = 1
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class BoardMemberInline(admin.TabularInline):
  model = BoardMember
  fk_name = 'parent'
  fields = ['employee','precinct','phone','street_address','city','state','zipcode']
  readonly_fields = []
  ordering = ['precinct__title',]
  extra = 0
  min_num = 0
  max_num = 7
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

  form = make_ajax_form(BoardMember, {'employee': 'employee'})

class BoardPolicyAdminInline(admin.TabularInline):
  model = BoardPolicyAdmin
  fk_name = 'parent'
  fields = ['employee',]
  readonly_fields = []
  ordering = ['title',]
  extra = 0
  min_num = 0
  max_num = 5
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

  form = make_ajax_form(BoardPolicyAdmin, {'employee': 'employee'})


class ResourceLinkInline(admin.TabularInline):
  model = ResourceLink.related_nodes.through
  fk_name = 'node'
  fields = []
  readonly_fields = []
  ordering = ['resourcelink__title',]
  extra = 0 
  min_num = 0
  max_num = 50
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

class DocumentInlineForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title'] 

    def __init__(self, *args, **kwargs):
        super(DocumentInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class DocumentInline(EditLinkToInlineObject, admin.TabularInline):
  model = Document
  form = DocumentInlineForm
  fk_name = 'parent'
  readonly_fields = ['edit_link',]
  fields = ['title', 'edit_link', ]
  ordering = ['title',]
  extra = 0 
  min_num = 0
  max_num = 50
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class BoardPolicyInlineForm(forms.ModelForm):
    class Meta:
        model = BoardPolicy
        fields = ['policy_title','section','index',]

    def __init__(self, *args, **kwargs):
        super(BoardPolicyInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['policy_title'].disabled = True
            self.fields['section'].disabled = True
            self.fields['index'].disabled = True

class BoardPolicyInline(EditLinkToInlineObject, admin.TabularInline):
  model = BoardPolicy
  form = BoardPolicyInlineForm
  fk_name = 'parent'
  readonly_fields = ['edit_link',]
  fields = ['policy_title', 'section', 'index', 'edit_link', ]
  ordering = ['title',]
  extra = 0
  min_num = 0
  max_num = 100
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class PolicyInlineForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(PolicyInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class PolicyInline(EditLinkToInlineObject, admin.TabularInline):
    model = Policy
    form = PolicyInlineForm
    fk_name = 'parent'
    readonly_fields = ['edit_link',]
    fields = ['title', 'edit_link', ]
    ordering = ['title',]
    extra = 0
    min_num = 0
    max_num = 1
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
            return qs
        return qs.filter(deleted=0)

class AdministrativeProcedureInlineForm(forms.ModelForm):
    class Meta:
        model = AdministrativeProcedure
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(AdministrativeProcedureInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class AdministrativeProcedureInline(EditLinkToInlineObject, admin.TabularInline):
    model = AdministrativeProcedure
    form = AdministrativeProcedureInlineForm
    fk_name = 'parent'
    readonly_fields = ['edit_link',]
    fields = ['title', 'edit_link', ]
    ordering = ['title',]
    extra = 0
    min_num = 0
    max_num = 1
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
            return qs
        return qs.filter(deleted=0)

class SupportingDocumentInlineForm(forms.ModelForm):
    class Meta:
        model = SupportingDocument
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(SupportingDocumentInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class SupportingDocumentInline(EditLinkToInlineObject, admin.TabularInline):
    model = SupportingDocument
    form = SupportingDocumentInlineForm
    fk_name = 'parent'
    readonly_fields = ['edit_link',]
    fields = ['title', 'edit_link', ]
    ordering = ['title',]
    extra = 0
    min_num = 0
    max_num = 10
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
            return qs
        return qs.filter(deleted=0)

class FileInline(admin.TabularInline):
  model = File
  fk_name = 'parent'
  fields = ['file_file', 'file_language']
  readonly_fields = []
  extra = 0 
  min_num = 0
  max_num = 50
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

  def get_queryset(self, request):
      qs = super().get_queryset(request)
      if request.user.is_superuser:
          return qs
      if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
          return qs
      return qs.filter(deleted=0)

class SubPageInlineForm(forms.ModelForm):
    class Meta:
        model = SubPage
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(SubPageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class SubPageInline(EditLinkToInlineObject, admin.TabularInline):
    model = SubPage
    form = SubPageInlineForm
    fk_name = 'parent'
    readonly_fields = ['edit_link',]
    fields = ['title', 'edit_link', ]
    ordering = ['title',]
    extra = 0
    min_num = 0
    max_num = 50
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
            return qs
        return qs.filter(deleted=0)

class BoardSubPageInlineForm(forms.ModelForm):
    class Meta:
        model = BoardSubPage
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardSubPageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardSubPageInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardSubPage
    form = BoardSubPageInlineForm
    fk_name = 'parent'
    readonly_fields = ['edit_link',]
    fields = ['title', 'edit_link', ]
    ordering = ['title',]
    extra = 0
    min_num = 0
    max_num = 50
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore',self.model._meta)):
            return qs
        return qs.filter(deleted=0)

class PageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            if 'parent' in self.fields:
                self.fields['parent'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(node_type='pages'))

    class Meta:
        model = Page
        fields = ['title', 'body','primary_contact','parent','url']

class PageAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(Page, {'primary_contact': 'employee'},PageAdminForm)

  def get_fields(self, request, obj=None):
      return ['title', 'body','primary_contact','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = []

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  def get_list_display(self,request):
    if request.user.has_perm('pages.restore_page'):
      return ['title','update_date','update_user','published','deleted']
    else:
      return ['title','update_date','update_user','published']

  #ordering = ('url',)
  
  def get_queryset(self, request):
   qs = super().get_queryset(request)
   if request.user.is_superuser:
     return qs
   if request.user.has_perm('pages.restore_page'):
     return qs
   return qs.filter(deleted=0)

  def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
          del actions['delete_selected']
        if request.user.has_perm('pages.trash_page'):    
          actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('pages.restore_page'):
          actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('pages.change_page'):
          actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
          actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions
  

  def get_list_filter(self, request):
    if request.user.has_perm('pages.restore_page'):
      return (DeletedListFilter,'published')
    else:
      return ['published',]

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class SchoolAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchoolAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            if 'parent' in self.fields:
                self.fields['parent'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='page', node_title='Elementary Schools') | Q(content_type='page', node_title='K-8 Schools') | Q(content_type='page', node_title='Middle Schools') | Q(content_type='page', node_title='High Schools') | Q(content_type='page', node_title='Charter Schools') | Q(content_type='page',node_title='Community Learning Centers'))

    class Meta:
        model = School
        fields = ['title', 'body','building_location','main_phone','main_fax','enrollment','openenrollmentstatus','schooltype','website_url','scc_url','boundary_map','primary_contact','parent','url']

class SchoolAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(School,{'primary_contact': 'employee'},SchoolAdminForm)

  def get_fields(self, request, obj=None):
      return ['title', 'body','building_location','main_phone','main_fax','enrollment','openenrollmentstatus','schooltype','website_url','scc_url','boundary_map','primary_contact','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = [ThumbnailInline, ContentBannerInline,SchoolAdministratorInline,ResourceLinkInline,DocumentInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class DepartmentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepartmentAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            if 'parent' in self.fields:
                self.fields['parent'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='page', node_title='Departments') | Q(content_type='department'))

    class Meta:
        model = Department
        fields = ['title','short_description','body','building_location','main_phone','main_fax','primary_contact','parent','url']

class DepartmentAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(Department,{'primary_contact': 'employee'}, DepartmentAdminForm)

  def get_fields(self, request, obj=None):
      return ['title','short_description','body','building_location','main_phone','main_fax','primary_contact','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = [ContentBannerInline,StaffInline,ResourceLinkInline,DocumentInline,SubPageInline]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class BoardAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoardAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            if 'parent' in self.fields:
                self.fields['parent'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='none'))

    class Meta:
        model = Board 
        fields = ['title','body','building_location','main_phone','main_fax','mission_statement','vision_statement','primary_contact','parent','url']

class BoardAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(Board,{'primary_contact': 'employee'}, BoardAdminForm)

  def get_fields(self, request, obj=None):
      return ['title','body','building_location','main_phone','main_fax','mission_statement','vision_statement','primary_contact','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = [ContentBannerInline,BoardMemberInline,StudentBoardMemberInline,BoardSubPageInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class BoardSubPageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoardSubPageAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            if 'parent' in self.fields:
                self.fields['parent'].queryset = Node.objects.filter(deleted=0).filter(published=1).filter(Q(content_type='board'))

    class Meta:
        model = BoardSubPage
        fields = ['title','body','building_location','main_phone','main_fax','primary_contact','parent','url']

class BoardSubPageAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(BoardSubPage,{'primary_contact': 'employee'}, BoardSubPageAdminForm)

  def get_fields(self, request, obj=None):
      return ['title','body','building_location','main_phone','main_fax','primary_contact','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = [ContentBannerInline,StaffInline,ResourceLinkInline,DocumentInline,BoardPolicyInline,SubPageInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          if obj.url == '/board-of-education/policies/':
              if isinstance(inline,ContentBannerInline):
                  continue
              if isinstance(inline,StaffInline):
                  continue
              if isinstance(inline,ResourceLinkInline):
                  continue
              if isinstance(inline,DocumentInline):
                  continue
              if isinstance(inline,SubPageInline):
                  continue
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class NewsAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      return ['title','pinned','summary','body','author_date']

  inlines = [NewsThumbnailInline,ContentBannerInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class NewsYearAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      return ['title',]

  inlines = []

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class ResourceLinkAdmin(MPTTModelAdmin,GuardedModelAdmin):
  def get_fields(self, request, obj=None):
    if obj:
      return ['title', 'link_url','url']
    else:
      return ['title', 'link_url','url']

  def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['url']
        else:
            return ['url']

  inlines = []

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  def get_list_display(self,request):
    if request.user.has_perm('links.restore_resourcelink'):
      return ['title','update_date','update_user','published','deleted']
    else:
      return ['title','update_date','update_user','published']

  #ordering = ('url',)
  
  def get_queryset(self, request):
   qs = super().get_queryset(request)
   if request.user.is_superuser:
     return qs
   if request.user.has_perm('links.restore_resourcelink'):
     return qs
   return qs.filter(deleted=0)

  def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
          del actions['delete_selected']
        if request.user.has_perm('links.trash_resourcelink'):    
          actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('links.restore_resourcelink'):
          actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('links.change_resourcelink'):
          actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
          actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions
  

  def get_list_filter(self, request):
    if request.user.has_perm('links.restore_resourcelink'):
      return (DeletedListFilter,'published')
    else:
      return ['published',]

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)


  response_change = apps.common.functions.response_change

class DocumentAdmin(MPTTModelAdmin,GuardedModelAdmin):
  
  inlines = [FileInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  def get_fields(self, request, obj=None):
    if obj:
      return ['title','url']
    else:
      return ['title', 'url']

  def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['url']
        else:
            return ['url']

  def get_list_display(self,request):
    if request.user.has_perm('documents.restore_document'):
      return ['title','update_date','update_user','published','deleted']
    else:
      return ['title','update_date','update_user','published']

  #ordering = ('url',)
  
  def get_queryset(self, request):
   qs = super().get_queryset(request)
   if request.user.is_superuser:
     return qs
   if request.user.has_perm('documents.restore_document'):
     return qs
   return qs.filter(deleted=0)

  def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
          del actions['delete_selected']
        if request.user.has_perm('documents.trash_document'):
          actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('documents.restore_document'):
          actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('documents.change_document'):
          actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
          actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions
  

  def get_list_filter(self, request):
    if request.user.has_perm('documents.restore_document'):
      return (DeletedListFilter,'published')
    else:
      return ['published',]

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class BoardPolicyAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [BoardPolicyAdminInline,PolicyInline,AdministrativeProcedureInline,SupportingDocumentInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if not isinstance(inline,ResourceLinkInline):
                # Remove delete fields is not superuser
                if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                    if not 'deleted' in inline.fields:
                        inline.fields.append('deleted')
                else:
                    while 'deleted' in inline.fields:
                        inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        return ['title','section','index','parent','url']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','section','index','parent','url']
            else:
                return ['url']

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['title','update_date','update_user','published','deleted']
        else:
            return ['title','update_date','update_user','published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('documents.restore_document'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('documents.trash_document'):
            actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('documents.restore_document'):
            actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('documents.change_document'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions


    def get_list_filter(self, request):
        if request.user.has_perm('documents.restore_document'):
            return (DeletedListFilter,'published')
        else:
            return ['published',]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in formset.new_objects:
            obj.create_user = request.user
            obj.update_user = request.user
            obj.save()
        for obj in formset.changed_objects:
            obj[0].update_user = request.user
            obj[0].save()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.update_user = request.user
        super().save_model(request, obj, form, change)

    response_change = apps.common.functions.response_change

class PolicyAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if not isinstance(inline,ResourceLinkInline):
                # Remove delete fields is not superuser
                if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                    if not 'deleted' in inline.fields:
                        inline.fields.append('deleted')
                else:
                    while 'deleted' in inline.fields:
                        inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        return ['title','parent','url']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['title','update_date','update_user','published','deleted']
        else:
            return ['title','update_date','update_user','published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('documents.restore_document'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('documents.trash_document'):
            actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('documents.restore_document'):
            actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('documents.change_document'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions


    def get_list_filter(self, request):
        if request.user.has_perm('documents.restore_document'):
            return (DeletedListFilter,'published')
        else:
            return ['published',]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in formset.new_objects:
            obj.create_user = request.user
            obj.update_user = request.user
            obj.save()
        for obj in formset.changed_objects:
            obj[0].update_user = request.user
            obj[0].save()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.update_user = request.user
        super().save_model(request, obj, form, change)

    response_change = apps.common.functions.response_change

class AdministrativeProcedureAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if not isinstance(inline,ResourceLinkInline):
                # Remove delete fields is not superuser
                if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                    if not 'deleted' in inline.fields:
                        inline.fields.append('deleted')
                else:
                    while 'deleted' in inline.fields:
                        inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        return ['title','parent','url']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['title','update_date','update_user','published','deleted']
        else:
            return ['title','update_date','update_user','published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('documents.restore_document'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('documents.trash_document'):
            actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('documents.restore_document'):
            actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('documents.change_document'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions


    def get_list_filter(self, request):
        if request.user.has_perm('documents.restore_document'):
            return (DeletedListFilter,'published')
        else:
            return ['published',]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in formset.new_objects:
            obj.create_user = request.user
            obj.update_user = request.user
            obj.save()
        for obj in formset.changed_objects:
            obj[0].update_user = request.user
            obj[0].save()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.update_user = request.user
        super().save_model(request, obj, form, change)

    response_change = apps.common.functions.response_change

class SupportingDocumentAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if not isinstance(inline,ResourceLinkInline):
                # Remove delete fields is not superuser
                if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                    if not 'deleted' in inline.fields:
                        inline.fields.append('deleted')
                else:
                    while 'deleted' in inline.fields:
                        inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        return ['title','parent','url']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['title','update_date','update_user','published','deleted']
        else:
            return ['title','update_date','update_user','published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('documents.restore_document'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('documents.trash_document'):
            actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('documents.restore_document'):
            actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('documents.change_document'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions


    def get_list_filter(self, request):
        if request.user.has_perm('documents.restore_document'):
            return (DeletedListFilter,'published')
        else:
            return ['published',]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in formset.new_objects:
            obj.create_user = request.user
            obj.update_user = request.user
            obj.save()
        for obj in formset.changed_objects:
            obj[0].update_user = request.user
            obj[0].save()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.update_user = request.user
        super().save_model(request, obj, form, change)

    response_change = apps.common.functions.response_change

class SubPageAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(Department,{'primary_contact': 'employee'})

  def get_fields(self, request, obj=None):
      return ['title','body','primary_contact','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = [ContentBannerInline,StaffInline,ResourceLinkInline,DocumentInline]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

class StudentBoardMemberAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      return ['title','first_name','last_name','phone','building_location','parent','url']

  def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['url']
        else:
            if obj:
                return ['title','parent','url']
            else:
                return ['url']

  inlines = [ProfilePictureInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          if not isinstance(inline,ResourceLinkInline):
              # Remove delete fields is not superuser
              if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
              else:
                while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission

  def save_formset(self, request, form, formset, change):
    instances = formset.save(commit=False)
    for obj in formset.deleted_objects:
      obj.delete()
    for obj in formset.new_objects:
      obj.create_user = request.user
      obj.update_user = request.user
      obj.save()
    for obj in formset.changed_objects:
      obj[0].update_user = request.user
      obj[0].save()

  def save_model(self, request, obj, form, change):
    if getattr(obj, 'create_user', None) is None:
      obj.create_user = request.user
    obj.update_user = request.user
    super().save_model(request, obj, form, change)

  response_change = apps.common.functions.response_change

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsYear, NewsYearAdmin)
admin.site.register(ResourceLink,ResourceLinkAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(BoardPolicy,BoardPolicyAdmin)
admin.site.register(Policy,PolicyAdmin)
admin.site.register(AdministrativeProcedure,AdministrativeProcedureAdmin)
admin.site.register(SupportingDocument,SupportingDocumentAdmin)
admin.site.register(SubPage,SubPageAdmin)
admin.site.register(StudentBoardMember, StudentBoardMemberAdmin)
admin.site.register(BoardSubPage, BoardSubPageAdmin)
