from django.conf import settings
from django import forms
from django.db.models import Q
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import get_permission_codename
from guardian.admin import GuardedModelAdmin
from mptt.admin import MPTTModelAdmin
from ajax_select import make_ajax_form, make_ajax_field
from adminsortable2.admin import SortableInlineAdminMixin
from apps.common.classes import DeletedListFilter, EditLinkToInlineObject
from apps.common.actions import trash_selected, restore_selected, publish_selected, unpublish_selected
from django.contrib.admin.actions import delete_selected
from .models import Page, School, Department, Board, BoardSubPage, News, NewsYear, SubPage, BoardMeetingYear, DistrictCalendarYear, SuperintendentMessage,SuperintendentMessageYear
from apps.images.models import Thumbnail, NewsThumbnail, ContentBanner, ProfilePicture, DistrictLogo, DistrictLogoGIF, DistrictLogoJPG, DistrictLogoPNG, DistrictLogoTIF, PhotoGallery, PhotoGalleryImage
from apps.directoryentries.models import SchoolAdministrator, Administrator, Staff, BoardMember, StudentBoardMember, BoardPolicyAdmin
from apps.links.models import ResourceLink, ActionButton
from apps.documents.models import Document, BoardPolicy, Policy, AdministrativeProcedure, SupportingDocument, BoardMeetingAgenda, BoardMeetingMinutes, BoardMeetingAudio, BoardMeetingVideo, BoardMeetingExhibit, BoardMeetingAgendaItem
from apps.events.models import BoardMeeting, DistrictCalendarEvent
from apps.files.models import File, AudioFile, VideoFile
from apps.objects.models import Node
from apps.faqs.models import FAQ
import apps.common.functions

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


class ProfilePictureInline(admin.StackedInline):
    model = ProfilePicture
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
    ]
    extra = 0
    min_num = 1
    max_num = 1


class ThumbnailInline(admin.TabularInline):
  model = Thumbnail
  fk_name = 'parent'
  fields = ['title','image_file','alttext','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class DistrictLogoGIFInline(admin.TabularInline):
  model = DistrictLogoGIF
  fk_name = 'parent'
  fields = ['title','image_file','alttext','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class DistrictLogoJPGInline(admin.TabularInline):
  model = DistrictLogoJPG
  fk_name = 'parent'
  fields = ['title','image_file','alttext','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class DistrictLogoPNGInline(admin.TabularInline):
  model = DistrictLogoPNG
  fk_name = 'parent'
  fields = ['title','image_file','alttext','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class DistrictLogoTIFInline(admin.TabularInline):
  model = DistrictLogoTIF
  fk_name = 'parent'
  fields = ['title','image_file','alttext','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class DistrictLogoInlineForm(forms.ModelForm):
    class Meta:
        model = DistrictLogo
        fields = ['district_logo_group','district_logo_style_variation',]

    def __init__(self, *args, **kwargs):
        super(DistrictLogoInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['district_logo_group'].disabled = True
            self.fields['district_logo_style_variation'].disabled = True

class DistrictLogoInline(EditLinkToInlineObject, admin.TabularInline):
  model = DistrictLogo
  form = DistrictLogoInlineForm
  ordering = ['district_logo_group__lft','district_logo_style_variation__lft',]
  fk_name = 'parent'
  fields = ['district_logo_group','district_logo_style_variation','update_user','update_date','edit_link',]
  readonly_fields = ['update_user','update_date','edit_link',]
  extra = 0
  min_num = 0
  max_num = 14 
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


class NewsInlineForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'pinned', 'author_date', ]

    def __init__(self, *args, **kwargs):
        super(NewsInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class NewsInline(EditLinkToInlineObject, admin.TabularInline):
    model = News
    form = NewsInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'pinned',
        'author_date',
        'update_user',
        'update_date',
        'edit_link',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        ]
    ordering = ['author_date', ]
    extra = 0
    min_num = 0
    max_num = 300
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('{0}.{1}'.format(
                self.model._meta.model_name,
                get_permission_codename('restore', self.model._meta))):
            return qs
        return qs.filter(deleted=0)


class PhotoGalleryInlineForm(forms.ModelForm):
    class Meta:
        model = PhotoGallery
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        super(PhotoGalleryInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class PhotoGalleryInline(EditLinkToInlineObject,
                         SortableInlineAdminMixin, admin.TabularInline):
    model = PhotoGallery
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        ]
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
        if request.user.has_perm('{0}.{1}'.format(
                self.model._meta.model_name,
                get_permission_codename('restore', self.model._meta))):
            return qs
        return qs.filter(deleted=0)


class PhotoGalleryImageInlineForm(forms.ModelForm):
    class Meta:
        model = PhotoGalleryImage
        fields = ['title', 'image_file', 'alttext', ]

    def __init__(self, *args, **kwargs):
        super(PhotoGalleryImageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class PhotoGalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PhotoGalleryImage
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        ]
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
        if request.user.has_perm('{0}.{1}'.format(
                self.model._meta.model_name,
                get_permission_codename('restore', self.model._meta))):
            return qs
        return qs.filter(deleted=0)


class NewsThumbnailInline(admin.TabularInline):
    model = NewsThumbnail
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        ]
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
        if request.user.has_perm('{0}.{1}'.format(
                self.model._meta.model_name,
                get_permission_codename('restore', self.model._meta))):
            return qs
        return qs.filter(deleted=0)


class ContentBannerInline(SortableInlineAdminMixin, admin.TabularInline):
  model = ContentBanner
  fk_name = 'parent'
  fields = ['title','image_file','alttext','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class SchoolAdministratorInlineForm(forms.ModelForm):
    class Meta:
        model = SchoolAdministrator
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super(SchoolAdministratorInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].disabled = True

class SchoolAdministratorInline(SortableInlineAdminMixin, admin.TabularInline):
  model = SchoolAdministrator
  fk_name = 'parent'
  fields = ['employee', 'schooladministratortype','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

  form = make_ajax_form(SchoolAdministrator, {'employee': 'employee'},SchoolAdministratorInlineForm)

class AdministratorInlineForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super(AdministratorInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].disabled = True

class AdministratorInline(SortableInlineAdminMixin, admin.TabularInline):
  model = Administrator
  fk_name = 'parent'
  fields = ['employee','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
  extra = 0
  min_inum = 0
  max_num = 15
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

  form = make_ajax_form(Administrator, {'employee': 'employee'},AdministratorInlineForm)

class StaffInlineForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super(StaffInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].disabled = True

class StaffInline(SortableInlineAdminMixin, admin.TabularInline):
  model = Staff
  fk_name = 'parent'
  fields = ['employee','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
  extra = 0
  min_inum = 0
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

  form = make_ajax_form(Staff, {'employee': 'employee'},StaffInlineForm)

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
  fields = ['title','update_user','update_date','edit_link']
  readonly_fields = ['update_user','update_date','edit_link']
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

class BoardMemberInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMember
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super(BoardMemberInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].disabled = True

class BoardMemberInline(admin.TabularInline):
  model = BoardMember
  fk_name = 'parent'
  fields = ['employee','is_president','is_vicepresident','precinct','phone','street_address','city','state','zipcode','term_ends','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

  form = make_ajax_form(BoardMember, {'employee': 'employee'},BoardMemberInlineForm)

class BoardPolicyAdminInline(admin.TabularInline):
  model = BoardPolicyAdmin
  fk_name = 'parent'
  fields = ['employee','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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


class ResourceLinkInline(SortableInlineAdminMixin, admin.TabularInline):
  model = ResourceLink
  fk_name = 'parent'
  fields = ['title','link_url','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
  extra = 0 
  min_num = 0
  max_num = 50
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline

class ActionButtonInlineForm(forms.ModelForm):
    class Meta:
        model = ActionButton
        fields = ['title','link_url',]

    def __init__(self, *args, **kwargs):
        super(ActionButtonInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass

class ActionButtonInline(SortableInlineAdminMixin, admin.TabularInline):
  model = ActionButton
  form = ActionButtonInlineForm
  fk_name = 'parent'
  fields = ['title', 'link_url','update_user','update_date','published',]
  readonly_fields = ['update_user','update_date',]
  extra = 0
  min_num = 0
  max_num = 4
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

class DocumentInlineForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(DocumentInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class DocumentInline(EditLinkToInlineObject, SortableInlineAdminMixin, admin.TabularInline):
  model = Document
  form = DocumentInlineForm
  fk_name = 'parent'
  fields = ['title','update_user','update_date','edit_link','published',]
  readonly_fields = ['update_user','update_date','edit_link',]
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
  fields = ['policy_title','section','index','update_user','update_date','edit_link',]
  readonly_fields = ['update_user','update_date','edit_link',]
  ordering = ['section__lft','index',]
  extra = 0
  min_num = 0
  max_num = 100
  has_add_permission = apps.common.functions.has_add_permission_inline
  has_change_permission = apps.common.functions.has_change_permission_inline
  has_delete_permission = apps.common.functions.has_delete_permission_inline


class BoardPolicyReviewInlineForm(forms.ModelForm):
    class Meta:
        model = BoardPolicy
        fields = ['title','subcommittee_review','boardmeeting_review','last_approved',]

    def __init__(self, *args, **kwargs):
        super(BoardPolicyReviewInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass

class BoardPolicyReviewInline(EditLinkToInlineObject, admin.TabularInline):
  model = BoardPolicy
  form = BoardPolicyReviewInlineForm
  verbose_name = 'Board Policy Review Schedule'
  verbose_name_plural = 'Board Policy Review Schedule'
  fk_name = 'parent'
  fields = ['title','subcommittee_review','boardmeeting_review','last_approved','update_user','update_date','edit_link',]
  readonly_fields = ['title','update_user','update_date','edit_link',]
  ordering = ['subcommittee_review','section__lft','index',]
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
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingAgendaInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeetingAgenda
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardMeetingAgendaInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardMeetingAgendaInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardMeetingAgenda
    form = BoardMeetingAgendaInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingMinutesInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeetingMinutes
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardMeetingMinutesInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardMeetingMinutesInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardMeetingMinutes
    form = BoardMeetingMinutesInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingAudioInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeetingAudio
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardMeetingAudioInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardMeetingAudioInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardMeetingAudio
    form = BoardMeetingAudioInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingVideoInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeetingVideo
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardMeetingVideoInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardMeetingVideoInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardMeetingVideo
    form = BoardMeetingVideoInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingExhibitInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeetingExhibit
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardMeetingExhibitInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardMeetingExhibitInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardMeetingExhibit
    form = BoardMeetingExhibitInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingAgendaItemInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeetingAgendaItem
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(BoardMeetingAgendaItemInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class BoardMeetingAgendaItemInline(EditLinkToInlineObject, admin.TabularInline):
    model = BoardMeetingAgendaItem
    form = BoardMeetingAgendaItemInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class FileInlineForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_file', 'file_language']

    def __init__(self, *args, **kwargs):
        super(FileInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['file_language'].disabled = True

class FileInline(admin.TabularInline):
  model = File
  form = FileInlineForm
  fk_name = 'parent'
  fields = ['file_file','file_language','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class AudioFileInlineForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['file_file',]

    def __init__(self, *args, **kwargs):
        super(AudioFileInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass

class AudioFileInline(admin.TabularInline):
  model = AudioFile
  form = AudioFileInlineForm
  fk_name = 'parent'
  fields = ['file_file','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class VideoFileInlineForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['file_file',]

    def __init__(self, *args, **kwargs):
        super(VideoFileInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass

class VideoFileInline(admin.TabularInline):
  model = VideoFile
  form = VideoFileInlineForm
  fk_name = 'parent'
  fields = ['file_file','update_user','update_date',]
  readonly_fields = ['update_user','update_date',]
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

class SubPageInlineForm(forms.ModelForm):
    class Meta:
        model = SubPage
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        super(SubPageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True

class SubPageInline(EditLinkToInlineObject, SortableInlineAdminMixin, admin.TabularInline):
    model = SubPage
    form = SubPageInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link','published',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardSubPageInline(SortableInlineAdminMixin, EditLinkToInlineObject, admin.TabularInline):
    model = BoardSubPage
    form = BoardSubPageInlineForm
    fk_name = 'parent'
    fields = ['title','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
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

class BoardMeetingInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeeting
        fields = ['startdate', 'meeting_type',]

    def __init__(self, *args, **kwargs):
        super(BoardMeetingInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass
            #raise Exception(dir(self))
            #self.fields['startdate'].data = self.instance.startdate
            #self.fields['startdate'].disabled = True
            #self.fields['startdate'].widget = forms.DateTimeInput
            #self.fields['meeting_type'].disabled = True

class BoardMeetingInline(EditLinkToInlineObject, admin.TabularInline):
  model = BoardMeeting
  form = BoardMeetingInlineForm
  fk_name = 'parent'
  fields = ['startdate', 'meeting_type','update_user','update_date','edit_link',]
  readonly_fields = ['update_user','update_date','edit_link',]
  ordering = ['-startdate',]
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

class SuperintendentMessageInlineForm(forms.ModelForm):
    class Meta:
        model = SuperintendentMessage
        fields = ['author_date',]

    def __init__(self, *args, **kwargs):
        super(SuperintendentMessageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass

class SuperintendentMessageInline(EditLinkToInlineObject, admin.TabularInline):
  model = SuperintendentMessage
  form = SuperintendentMessageInlineForm
  fk_name = 'parent'
  fields = ['author_date','update_user','update_date','edit_link',]
  readonly_fields = ['update_user','update_date','edit_link',]
  ordering = ['-author_date',]
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

class DistrictCalendarEventInlineForm(forms.ModelForm):
    class Meta:
        model = DistrictCalendarEvent
        fields = ['event_name','event_category','startdate','enddate',]

    def __init__(self, *args, **kwargs):
        super(DistrictCalendarEventInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass

class DistrictCalendarEventInline(EditLinkToInlineObject, admin.TabularInline):
  model = DistrictCalendarEvent
  form = DistrictCalendarEventInlineForm
  fk_name = 'parent'
  fields = ['event_name','event_category','startdate','enddate','update_user','update_date','edit_link',]
  readonly_fields = ['update_user','update_date','edit_link',]
  ordering = ['startdate',]
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

class FAQInlineForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question',]

    def __init__(self, *args, **kwargs):
        super(FAQInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
          pass

class FAQInline(EditLinkToInlineObject, SortableInlineAdminMixin, admin.TabularInline):
    model = FAQ
    fk_name = 'parent'
    fields = ['question','update_user','update_date','edit_link',]
    readonly_fields = ['update_user','update_date','edit_link',]
    extra = 0
    min_num = 0
    max_num = 25
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
      fields = ['title', 'body','primary_contact',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ActionButtonInline,FAQInline,ResourceLinkInline,DocumentInline,SubPageInline]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          # Remove delete fields is not superuser
          if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
              if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
          else:
              while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          if obj:
              if obj.url == '/search/':
                  if not isinstance(inline,FAQInline):
                      continue
              else:
                  if isinstance(inline,FAQInline):
                      continue
          yield inline.get_formset(request, obj), inline

  def get_list_display(self,request):
    if request.user.has_perm('pages.restore_page'):
      return ['title','update_date','update_user','published','deleted']
    else:
      return ['title','update_date','update_user','published']

  #ordering = ('url',)
  
  def get_queryset(self, request):
   qs = super().get_queryset(request)
   qs = qs.filter(site=request.site.pk)
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
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
      fields = ['title', 'body','building_location','main_phone','main_fax','enrollment','openenrollmentstatus','schooltype','schooloptions','website_url','scc_url','calendar_url','donate_url','boundary_map','primary_contact',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ThumbnailInline, ContentBannerInline, SchoolAdministratorInline, ResourceLinkInline, DocumentInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
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
      fields = ['title','short_description','body','building_location','main_phone','main_fax','primary_contact',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ContentBannerInline,ActionButtonInline,AdministratorInline,StaffInline,ResourceLinkInline,DocumentInline,SubPageInline]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
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
      fields = ['title','body','building_location','main_phone','main_fax','mission_statement','vision_statement','primary_contact',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ContentBannerInline,BoardMemberInline,StudentBoardMemberInline,ResourceLinkInline,DocumentInline,BoardSubPageInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
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
      fields = ['title','body','building_location','main_phone','main_fax','primary_contact',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ContentBannerInline,ActionButtonInline,AdministratorInline,StaffInline,ResourceLinkInline,DocumentInline,BoardPolicyInline,BoardPolicyReviewInline,BoardMeetingInline,SubPageInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          # Remove delete fields is not superuser
          if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
              if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
          else:
              while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          if isinstance(inline,ContentBannerInline):
              if obj.url == '/board-of-education/policies/':
                  continue
              if obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,ActionButtonInline):
              if obj.url == '/board-of-education/policies/':
                  continue
              if obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,AdministratorInline):
              if obj.url == '/board-of-education/policies/':
                  continue
              if obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,StaffInline):
              if obj.url == '/board-of-education/policies/':
                  continue
              if obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,ResourceLinkInline):
              if obj.url == '/board-of-education/policies/':
                  continue
              if obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,DocumentInline):
              if obj.url == '/board-of-education/policies/':
                  continue
              if obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,BoardPolicyInline):
              if not obj.url == '/board-of-education/policies/':
                  continue
          if isinstance(inline, BoardPolicyReviewInline):
              if not obj.url == '/board-of-education/policies/':
                  continue
          if isinstance(inline,BoardMeetingInline):
              if not obj.url == '/board-of-education/board-meetings/':
                  continue
          if isinstance(inline,SubPageInline):
              pass
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class NewsAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      fields = ['title','pinned','summary','body','author_date',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields
  
  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [NewsThumbnailInline, ContentBannerInline, PhotoGalleryInline, ]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class NewsYearAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      fields = ['title',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [NewsInline, ]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class SuperintendentMessageAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      fields = ['author_date','summary','body',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['author_date','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          if obj:
           fields += ['url']
      return fields

  inlines = [NewsThumbnailInline,ContentBannerInline,ResourceLinkInline,DocumentInline]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class SuperintendentMessageYearAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      fields = ['title',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [SuperintendentMessageInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class DocumentAdmin(MPTTModelAdmin,GuardedModelAdmin):
  
  inlines = [FileInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          # Remove delete fields is not superuser
          if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
              if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
          else:
              while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          yield inline.get_formset(request, obj), inline

  def get_fields(self, request, obj=None):
      fields = ['title',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class BoardPolicyAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [BoardPolicyAdminInline,PolicyInline,AdministrativeProcedureInline,SupportingDocumentInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title','section','index','subcommittee_review','boardmeeting_review','last_approved',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent',]
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','section','index','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            fields.remove('section')
            fields.remove('index')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class PolicyAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent',]
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class AdministrativeProcedureAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent',]
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class SupportingDocumentAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent',]
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class SubPageAdmin(MPTTModelAdmin,GuardedModelAdmin):

  form = make_ajax_form(Department,{'primary_contact': 'employee'})

  def get_fields(self, request, obj=None):
      fields = ['title','body','building_location','main_phone','main_fax','primary_contact',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ContentBannerInline,ActionButtonInline,AdministratorInline,StaffInline,ResourceLinkInline,DocumentInline,DistrictLogoInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
          # Remove delete fields is not superuser
          if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
              if not 'deleted' in inline.fields:
                  inline.fields.append('deleted')
          else:
              while 'deleted' in inline.fields:
                  inline.fields.remove('deleted')
          if obj:
              if not obj.url == '/departments/communications-and-community-relations/district-logo/':
                  if isinstance(inline,DistrictLogoInline):
                      continue
          yield inline.get_formset(request, obj), inline

  has_change_permission = apps.common.functions.has_change_permission
  has_add_permission = apps.common.functions.has_add_permission
  has_delete_permission = apps.common.functions.has_delete_permission
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class StudentBoardMemberAdmin(MPTTModelAdmin,GuardedModelAdmin):

  def get_fields(self, request, obj=None):
      fields = ['title','first_name','last_name','phone','building_location',['update_user','update_date',],['create_user','create_date',],]
      if request.user.is_superuser:
          fields += ['published','searchable','parent',]
          if obj:
              fields += ['url']
      return fields

  def get_readonly_fields(self, request, obj=None):
      fields = ['title','update_user','update_date','create_user','create_date',]
      if request.user.is_superuser:
          fields.remove('title')
          if obj:
           fields += ['url']
      return fields

  inlines = [ProfilePictureInline,]

  def get_formsets_with_inlines(self, request, obj=None):
      for inline in self.get_inline_instances(request, obj):
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
  save_formset = apps.common.functions.save_formset
  save_model = apps.common.functions.save_model
  response_change = apps.common.functions.response_change

class BoardMeetingAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [BoardMeetingAgendaInline,BoardMeetingMinutesInline,BoardMeetingAudioInline,BoardMeetingVideoInline,BoardMeetingExhibitInline,BoardMeetingAgendaItemInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title','originaldate', 'startdate','cancelled','meeting_type','building_location','non_district_location','non_district_location_google_place',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','originaldate','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            fields.remove('originaldate')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class BoardMeetingYearAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [BoardMeetingInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class BoardMeetingAgendaAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class BoardMeetingMinutesAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class BoardMeetingAudioAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [AudioFileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class BoardMeetingVideoAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [VideoFileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change


class BoardMeetingExhibitAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class BoardMeetingAgendaItemAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [FileInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class FAQAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [ActionButtonInline,ResourceLinkInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['question','answer',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            if obj:
             fields += ['url']
        return fields

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['question','update_date','update_user','published','deleted']
        else:
            return ['question','update_date','update_user','published']

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class DistrictCalendarYearAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [DistrictCalendarEventInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            if obj:
             fields += ['url']
        return fields

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class DistrictCalendarEventAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = []

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['event_name','event_category','startdate','enddate','building_location','non_district_location','non_district_location_google_place','cancelled',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            if obj:
             fields += ['url']
        return fields

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['event_name','event_category','startdate','enddate','update_date','update_user','published','deleted']
        else:
            return ['event_name','event_category','startdate','enddate','update_date','update_user','published']

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
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change

class DistrictLogoAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [ThumbnailInline,DistrictLogoGIFInline,DistrictLogoJPGInline,DistrictLogoPNGInline,DistrictLogoTIFInline,]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['district_logo_group','district_logo_style_variation',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published','searchable','parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['district_logo_group','district_logo_style_variation','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            if obj:
             fields += ['url']
        return fields

    def get_list_display(self,request):
        if request.user.has_perm('documents.restore_document'):
            return ['event_name','event_category','startdate','enddate','update_date','update_user','published','deleted']
        else:
            return ['event_name','event_category','startdate','enddate','update_date','update_user','published']

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
            return (DeletedListFilter, 'published')
        else:
            return ['published', ]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change


class PhotoGalleryAdmin(MPTTModelAdmin,GuardedModelAdmin):

    inlines = [PhotoGalleryImageInline, ]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline


    def get_fields(self, request, obj=None):
        fields = ['title',['update_user','update_date',],['create_user','create_date',],]
        if request.user.is_superuser:
            fields += ['published', 'searchable', 'parent']
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title','update_user','update_date','create_user','create_date',]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
             fields += ['url']
        return fields

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
            return (DeletedListFilter, 'published')
        else:
            return ['published', ]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change


admin.site.register(Page, PageAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsYear, NewsYearAdmin)
admin.site.register(SuperintendentMessage, SuperintendentMessageAdmin)
admin.site.register(SuperintendentMessageYear, SuperintendentMessageYearAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(BoardPolicy, BoardPolicyAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(AdministrativeProcedure, AdministrativeProcedureAdmin)
admin.site.register(SupportingDocument, SupportingDocumentAdmin)
admin.site.register(BoardMeetingAgenda, BoardMeetingAgendaAdmin)
admin.site.register(BoardMeetingMinutes, BoardMeetingMinutesAdmin)
admin.site.register(BoardMeetingAudio, BoardMeetingAudioAdmin)
admin.site.register(BoardMeetingVideo, BoardMeetingVideoAdmin)
admin.site.register(BoardMeetingExhibit, BoardMeetingExhibitAdmin)
admin.site.register(BoardMeetingAgendaItem, BoardMeetingAgendaItemAdmin)
admin.site.register(SubPage, SubPageAdmin)
admin.site.register(StudentBoardMember, StudentBoardMemberAdmin)
admin.site.register(BoardSubPage, BoardSubPageAdmin)
admin.site.register(BoardMeeting, BoardMeetingAdmin)
admin.site.register(BoardMeetingYear, BoardMeetingYearAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(DistrictCalendarYear, DistrictCalendarYearAdmin)
admin.site.register(DistrictCalendarEvent, DistrictCalendarEventAdmin)
admin.site.register(DistrictLogo, DistrictLogoAdmin)
admin.site.register(PhotoGallery, PhotoGalleryAdmin)
