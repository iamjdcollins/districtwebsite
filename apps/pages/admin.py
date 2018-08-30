import sys
from django.conf import settings
from django import forms
from django.db.models import Q
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import get_permission_codename
from guardian.admin import GuardedModelAdmin
from mptt.admin import MPTTModelAdmin
from ajax_select import make_ajax_form, make_ajax_field
from ajax_select.fields import AutoCompleteSelectField
from adminsortable2.admin import SortableInlineAdminMixin
from apps.common.classes import (
    DeletedListFilter,
    EditLinkToInlineObject,
    LinkToInlineObject,
    MyDraggableMPTTAdmin,
)
from apps.common.actions import (
    trash_selected,
    restore_selected,
    publish_selected,
    unpublish_selected,
)
from django.contrib.admin.actions import delete_selected
from .models import (
    Page,
    Announcement,
    School,
    Department,
    Board,
    BoardSubPage,
    News,
    NewsYear,
    SubPage,
    BoardMeetingYear,
    DistrictCalendarYear,
    SuperintendentMessage,
    SuperintendentMessageYear,
)
from apps.images.models import (
    Thumbnail,
    NewsThumbnail,
    ContentBanner,
    ProfilePicture,
    DistrictLogo,
    DistrictLogoGIF,
    DistrictLogoJPG,
    DistrictLogoPNG,
    DistrictLogoTIF,
    PhotoGallery,
    PhotoGalleryImage,
)
from apps.directoryentries.models import (
    SchoolAdministrator,
    Administrator,
    Staff,
    BoardMember,
    StudentBoardMember,
    BoardPolicyAdmin,
    SchoolAdministration,
    SchoolStaff,
    SchoolFaculty,
)
from apps.links.models import (
    ResourceLink,
    ActionButton,
    ClassWebsite,
)
from apps.documents.models import (
    Document,
    DisclosureDocument,
    BoardPolicy,
    Policy,
    AdministrativeProcedure,
    SupportingDocument,
    BoardMeetingAgenda,
    BoardMeetingMinutes,
    BoardMeetingAudio,
    BoardMeetingVideo,
    BoardMeetingExhibit,
    BoardMeetingAgendaItem,
)
from apps.events.models import (
    BoardMeeting,
    DistrictCalendarEvent,
)
from apps.files.models import (
    File,
    AudioFile,
    VideoFile,
    PrecinctMap,
)
from apps.taxonomy.models import (
    SubjectGradeLevel,
)
from apps.objects.models import Node
from apps.faqs.models import FAQ
import apps.common.functions
from ckeditor.widgets import CKEditorWidget

from django.utils.safestring import mark_safe
from django.urls import reverse
from apps.dashboard.models import PageLayout


class ProfilePictureInline(
    LinkToInlineObject,
    admin.StackedInline,
):
    model = ProfilePicture
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
    extra = 0
    min_num = 1
    max_num = 1


class ThumbnailInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = Thumbnail
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DistrictLogoGIFInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = DistrictLogoGIF
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DistrictLogoJPGInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = DistrictLogoJPG
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DistrictLogoPNGInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = DistrictLogoPNG
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DistrictLogoTIFInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = DistrictLogoTIF
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DistrictLogoInlineForm(forms.ModelForm):
    class Meta:
        model = DistrictLogo
        fields = [
            'district_logo_group',
            'district_logo_style_variation',
        ]

    def __init__(self, *args, **kwargs):
        super(DistrictLogoInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['district_logo_group'].disabled = True
            self.fields['district_logo_style_variation'].disabled = True


class DistrictLogoInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = DistrictLogo
    form = DistrictLogoInlineForm
    ordering = [
        'district_logo_group__lft',
        'district_logo_style_variation__lft',
    ]
    fk_name = 'parent'
    fields = [
        'district_logo_group',
        'district_logo_style_variation',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class NewsInlineForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'pinned',
            'author_date',
        ]

    def __init__(self, *args, **kwargs):
        super(NewsInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class NewsInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
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
        'published',
        'copy_link',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
        ]
    ordering = ['-author_date', ]
    extra = 0
    min_num = 0
    max_num = 500
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


class PhotoGalleryInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    SortableInlineAdminMixin,
    admin.TabularInline
):
    model = PhotoGallery
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
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


class PhotoGalleryImageInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = PhotoGalleryImage
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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


class NewsThumbnailInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = NewsThumbnail
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
        ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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


class ContentBannerInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline
):
    model = ContentBanner
    fk_name = 'parent'
    fields = [
        'title',
        'image_file',
        'alttext',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class SchoolAdministratorInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = SchoolAdministrator
    fk_name = 'parent'
    fields = [
        'employee',
        'schooladministratortype',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)

    form = make_ajax_form(SchoolAdministrator, {
                          'employee': 'employee'}, SchoolAdministratorInlineForm)


class AdministratorInlineForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super(AdministratorInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].disabled = True


class AdministratorInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = Administrator
    fk_name = 'parent'
    fields = [
        'employee',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)

    form = make_ajax_form(
        Administrator, {'employee': 'employee'}, AdministratorInlineForm)


class StaffInlineForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['employee']

    def __init__(self, *args, **kwargs):
        super(StaffInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['employee'].disabled = True


class StaffInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = Staff
    fk_name = 'parent'
    fields = [
        'employee',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)

    form = make_ajax_form(Staff, {'employee': 'employee'}, StaffInlineForm)


class StudentBoardMemberInlineForm(forms.ModelForm):
    class Meta:
        model = StudentBoardMember
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(StudentBoardMemberInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class StudentBoardMemberInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = StudentBoardMember
    form = StudentBoardMemberInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = ['title', ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMemberInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMember
    fk_name = 'parent'
    fields = [
        'employee',
        'is_president',
        'is_vicepresident',
        'precinct',
        'phone',
        'street_address',
        'city',
        'state',
        'zipcode',
        'term_ends',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
    ordering = ['precinct__title', ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)

    form = make_ajax_form(
        BoardMember, {'employee': 'employee'}, BoardMemberInlineForm)


class BoardPolicyAdminInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = BoardPolicyAdmin
    fk_name = 'parent'
    fields = [
        'employee',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
    ordering = ['title', ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)

    form = make_ajax_form(BoardPolicyAdmin, {'employee': 'employee'})


class ResourceLinkInlineForm(forms.ModelForm):
    class Meta:
        model = ResourceLink
        fields = ['title', 'link_url', 'published']

    def __init__(self, *args, **kwargs):
        super(ResourceLinkInlineForm, self).__init__(*args, **kwargs)
        if self.instance.related_locked:
            self.fields['title'].disabled = True
            self.fields['title'].widget.attrs['class'] = '{0} related_locked'.format(
                self.fields['title'].widget.attrs['class']
            )
            self.fields['title'].widget.attrs['data-relatedtype'] = '{0}'.format(
                self.instance.related_type
            )
            self.fields['link_url'].disabled = True
            self.fields['published'].disabled = True
            if 'deleted' in self.fields:
                self.fields['deleted'].disabled = True


class ResourceLinkInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline
):
    model = ResourceLink
    form = ResourceLinkInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'link_url',
        'update_user',
        'update_date',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class ClassWebsiteInlineForm(forms.ModelForm):
    class Meta:
        model = ClassWebsite
        fields = ['title', 'link_url', 'published']

    def __init__(self, *args, **kwargs):
        super(ClassWebsiteInlineForm, self).__init__(*args, **kwargs)


class ClassWebsiteInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline
):
    model = ClassWebsite
    form = ClassWebsiteInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'link_url',
        'update_user',
        'update_date',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class ActionButtonInlineForm(forms.ModelForm):
    class Meta:
        model = ActionButton
        fields = ['title', 'link_url', ]

    def __init__(self, *args, **kwargs):
        super(ActionButtonInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class ActionButtonInline(
    SortableInlineAdminMixin,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = ActionButton
    form = ActionButtonInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'link_url',
        'update_user',
        'update_date',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DocumentInlineForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'pagelayout']

    def __init__(self, *args, **kwargs):
        super(DocumentInlineForm, self).__init__(*args, **kwargs)
        self.fields['pagelayout'].initial = Document.PAGELAYOUT
        self.fields['pagelayout'].widget = forms.HiddenInput()
        if self.instance.pk:
            self.fields['title'].disabled = True


class DocumentInline(
    EditLinkToInlineObject,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = Document
    form = DocumentInlineForm
    classes = {
        'document_inline',
    }
    fk_name = 'parent'
    fields = [
        'title',
        'pagelayout',
        'update_user',
        'update_date',
        'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    extra = 0
    min_num = 0
    max_num = 500
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DisclosureDocumentInlineForm(forms.ModelForm):
    class Meta:
        model = DisclosureDocument
        fields = ['title', 'pagelayout',]

    def __init__(self, *args, **kwargs):
        super(DisclosureDocumentInlineForm, self).__init__(*args, **kwargs)
        self.fields['pagelayout'].initial = DisclosureDocument.PAGELAYOUT
        self.fields['pagelayout'].widget = forms.HiddenInput()
        if self.instance.pk:
            self.fields['title'].disabled = True


class DisclosureDocumentInline(
    EditLinkToInlineObject,
    LinkToInlineObject,
    admin.TabularInline,
):
    model = DisclosureDocument
    form = DisclosureDocumentInlineForm
    verbose_name = 'Disclosure Document'
    verbose_name_plural = 'Disclosure Documents'
    fk_name = 'parent'
    fields = [
        'title',
        'pagelayout',
        'update_user',
        'update_date',
        'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    extra = 0
    min_num = 0
    max_num = 500
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class BoardPolicyInlineForm(forms.ModelForm):
    class Meta:
        model = BoardPolicy
        fields = ['policy_title', 'section', 'index', ]

    def __init__(self, *args, **kwargs):
        super(BoardPolicyInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['section'].disabled = True
            self.fields['index'].disabled = True


class BoardPolicyInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardPolicy
    form = BoardPolicyInlineForm
    fk_name = 'parent'
    fields = [
        'policy_title',
        'section',
        'index',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = ['section__lft', 'index', ]
    extra = 0
    min_num = 0
    max_num = 100
    has_add_permission = apps.common.functions.has_add_permission_inline
    has_change_permission = apps.common.functions.has_change_permission_inline
    has_delete_permission = apps.common.functions.has_delete_permission_inline


class BoardPolicyReviewInlineForm(forms.ModelForm):
    class Meta:
        model = BoardPolicy
        fields = [
            'title',
            'subcommittee_review',
            'boardmeeting_review',
            'last_approved',
        ]

    def __init__(self, *args, **kwargs):
        super(BoardPolicyReviewInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class BoardPolicyReviewInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardPolicy
    form = BoardPolicyReviewInlineForm
    verbose_name = 'Board Policy Review Schedule'
    verbose_name_plural = 'Board Policy Review Schedule'
    fk_name = 'parent'
    fields = [
        'title',
        'subcommittee_review',
        'boardmeeting_review',
        'last_approved',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'subcommittee_review',
        'section__lft',
        'index',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class PolicyInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = Policy
    form = PolicyInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class AdministrativeProcedureInlineForm(forms.ModelForm):
    class Meta:
        model = AdministrativeProcedure
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(AdministrativeProcedureInlineForm,
              self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class AdministrativeProcedureInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = AdministrativeProcedure
    form = AdministrativeProcedureInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class SupportingDocumentInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = SupportingDocument
    form = SupportingDocumentInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMeetingAgendaInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeetingAgenda
    form = BoardMeetingAgendaInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMeetingMinutesInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeetingMinutes
    form = BoardMeetingMinutesInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMeetingAudioInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeetingAudio
    form = BoardMeetingAudioInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMeetingVideoInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeetingVideo
    form = BoardMeetingVideoInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMeetingExhibitInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeetingExhibit
    form = BoardMeetingExhibitInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardMeetingAgendaItemInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeetingAgendaItem
    form = BoardMeetingAgendaItemInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = ['title', ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class FileInlineForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            'file_file',
            'file_language',
        ]

    def __init__(self, *args, **kwargs):
        super(FileInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['file_language'].disabled = True


class FileInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = File
    form = FileInlineForm
    fk_name = 'parent'
    fields = [
        'file_file',
        'file_language',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
    ]
    ordering = [
        'file_language__lft',
        'file_language__title',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class AudioFileInlineForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['file_file', ]

    def __init__(self, *args, **kwargs):
        super(AudioFileInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class AudioFileInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = AudioFile
    form = AudioFileInlineForm
    fk_name = 'parent'
    fields = [
        'file_file',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class VideoFileInlineForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['file_file', ]

    def __init__(self, *args, **kwargs):
        super(VideoFileInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class VideoFileInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = VideoFile
    form = VideoFileInlineForm
    fk_name = 'parent'
    fields = [
        'file_file',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class PrecinctMapInline(
    LinkToInlineObject,
    admin.TabularInline,
):
    model = PrecinctMap
    fk_name = 'parent'
    fields = [
        'file_file',
        'update_user',
        'update_date',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class SubPageInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline
):
    model = SubPage
    form = SubPageInlineForm
    classes = {
        'subpage_inline',
    }
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class SectionPageInlineForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title',
        ]

    def __init__(self, *args, **kwargs):
        super(SectionPageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['title'].disabled = True


class SectionPageInline(
    LinkToInlineObject,
    SortableInlineAdminMixin,
    EditLinkToInlineObject,
    admin.TabularInline
):
    model = Page
    form = SectionPageInlineForm
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    verbose_name = 'Section Page'
    verbose_name_plural = 'Section Pages'
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
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


class BoardSubPageInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline
):
    model = BoardSubPage
    form = BoardSubPageInlineForm
    fk_name = 'parent'
    classes = {
        'boardsubpage_inline',
    }
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class BoardMeetingInlineForm(forms.ModelForm):
    class Meta:
        model = BoardMeeting
        fields = [
            'startdate',
            'meeting_type',
        ]

    def __init__(self, *args, **kwargs):
        super(BoardMeetingInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class BoardMeetingInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = BoardMeeting
    form = BoardMeetingInlineForm
    fk_name = 'parent'
    fields = [
        'startdate',
        'meeting_type',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        '-startdate',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class SuperintendentMessageInlineForm(forms.ModelForm):
    class Meta:
        model = SuperintendentMessage
        fields = ['author_date', ]

    def __init__(self, *args, **kwargs):
        super(SuperintendentMessageInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class SuperintendentMessageInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = SuperintendentMessage
    form = SuperintendentMessageInlineForm
    fk_name = 'parent'
    fields = [
        'author_date',
        'update_user',
        'update_date',
        'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        '-author_date',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class DistrictCalendarEventInlineForm(forms.ModelForm):
    class Meta:
        model = DistrictCalendarEvent
        fields = [
            'event_name',
            'event_category',
            'startdate',
            'enddate',
        ]

    def __init__(self, *args, **kwargs):
        super(DistrictCalendarEventInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class DistrictCalendarEventInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    admin.TabularInline,
):
    model = DistrictCalendarEvent
    form = DistrictCalendarEventInlineForm
    fk_name = 'parent'
    fields = [
        'event_name',
        'event_category',
        'startdate',
        'enddate',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    ordering = [
        'startdate',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class FAQInlineForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', ]

    def __init__(self, *args, **kwargs):
        super(FAQInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class FAQInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    SortableInlineAdminMixin,
    admin.TabularInline,
):
    model = FAQ
    fk_name = 'parent'
    fields = [
        'question',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class AnnouncementInlineForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body', ]

    def __init__(self, *args, **kwargs):
        super(AnnouncementInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class AnnouncementInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    SortableInlineAdminMixin,
    admin.TabularInline,
):
    model = Announcement
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class SchoolAdministrationInlineForm(forms.ModelForm):
    class Meta:
        model = SchoolAdministration
        fields = [
            'employee',
        ]

    def __init__(self, *args, **kwargs):
        super(SchoolAdministrationInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class SchoolAdministrationInline(
    LinkToInlineObject,
    # EditLinkToInlineObject,
    SortableInlineAdminMixin,
    admin.TabularInline,
):
    model = SchoolAdministration
    form = make_ajax_form(SchoolAdministration, {
                          'employee': 'employee'}, SchoolAdministrationInlineForm)
    fk_name = 'parent'
    fields = [
        'employee',
        'update_user',
        'update_date',
        # 'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        # 'edit_link',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class SchoolStaffInlineForm(forms.ModelForm):
    class Meta:
        model = SchoolStaff
        fields = [
            'employee',
        ]

    def __init__(self, *args, **kwargs):
        super(SchoolStaffInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class SchoolStaffInline(
    LinkToInlineObject,
    # EditLinkToInlineObject,
    SortableInlineAdminMixin,
    admin.TabularInline,
):
    model = SchoolStaff
    form = make_ajax_form(SchoolStaff, {
                          'employee': 'employee'}, SchoolStaffInlineForm)
    verbose_name = 'School Staff'
    verbose_name_plural = 'School Staff'
    fk_name = 'parent'
    fields = [
        'employee',
        'update_user',
        'update_date',
        # 'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        # 'edit_link',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class SchoolFacultyInlineForm(forms.ModelForm):
    class Meta:
        model = SchoolFaculty
        fields = [
            'employee',
            'primary_subject',
            'additional_subjects',
            'pagelayout',
        ]

    def __init__(self, *args, **kwargs):
        super(SchoolFacultyInlineForm, self).__init__(*args, **kwargs)
        self.fields['pagelayout'].initial = str(PageLayout.objects.get(namespace='school-faculty-my-page.html').pk)
        self.fields['pagelayout'].widget = forms.HiddenInput()
        if self.instance.pk:
            pass


class SchoolFacultyInline(
    LinkToInlineObject,
    EditLinkToInlineObject,
    #SortableInlineAdminMixin,
    admin.TabularInline,
):
    model = SchoolFaculty
    form = make_ajax_form(SchoolFaculty, {
                          'employee': 'employee'}, SchoolFacultyInlineForm)
    verbose_name = 'School Faculty'
    verbose_name_plural = 'School Faculty'
    fk_name = 'parent'
    ordering = [
        'employee__first_name',
        'employee__last_name',
    ]
    fields = [
        'employee',
        'primary_subject',
        'additional_subjects',
        'primary_contact',
        'pagelayout',
        'update_user',
        'update_date',
        'edit_link',
        'published',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        'edit_link',
        'copy_link',
    ]
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class SubjectGradeLevelInlineForm(forms.ModelForm):
    class Meta:
        model = SubjectGradeLevel
        fields = [
            'title',
        ]

    def __init__(self, *args, **kwargs):
        super(SubjectGradeLevelInlineForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            pass


class SubjectGradeLevelInline(
    LinkToInlineObject,
    # EditLinkToInlineObject,
    SortableInlineAdminMixin,
    admin.TabularInline,
):
    model = SubjectGradeLevel
    form = SubjectGradeLevelInlineForm
    verbose_name = 'Subject or Grade Level'
    verbose_name_plural = 'Subjects and Grade Levels'
    fk_name = 'parent'
    fields = [
        'title',
        'update_user',
        'update_date',
        # 'edit_link',
        'copy_link',
    ]
    readonly_fields = [
        'update_user',
        'update_date',
        # 'edit_link',
        'copy_link',
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
        if request.user.has_perm(self.model._meta.model_name + '.' + get_permission_codename('restore', self.model._meta)):
            return qs
        return qs.filter(deleted=0)


class PageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            if 'parent' in self.fields:
                self.fields['parent'].queryset = Node.objects.filter(deleted=0, published=1, site=self.instance.site).filter(Q(node_type='pages'))

    class Meta:
        model = Page
        fields = ['title', 'body','primary_contact','parent','url']


class PageAdmin(MyDraggableMPTTAdmin, GuardedModelAdmin):

    form = make_ajax_form(Page, {'primary_contact': 'employee'} ,PageAdminForm)

    def get_fields(self, request, obj=None):
        fields = []
        if request.site.domain != 'www.slcschools.org':
            if obj:
                if obj.pagelayout.namespace in obj.TYPES:
                    fields = obj.TYPES[obj.pagelayout.namespace]['fields']
                else:
                    fields = []
            else:
                fields = []
            # When adding fields with append below you should
            # have a matching remove. For some reason if you
            # do not fields appear inconsistently for different
            # users.
            if request.user.is_superuser:
                if 'searchable' not in fields:
                    fields.append('searchable')
                if 'parent' not in fields:
                    fields.append('parent')
                if 'url' not in fields:
                    fields.append('url')
            else:
                if 'searchable' in fields:
                    fields.remove('searchable')
                if 'parent' in fields:
                    fields.remove('parent')
                if 'url' in fields:
                    fields.remove('url')
            return fields
        elif request.site.domain == 'www.slcschools.org':
            fields = ['title', 'pagelayout', 'body','primary_contact',['update_user','update_date',],['create_user','create_date',],]
            if request.user.is_superuser:
                fields += ['published','searchable','parent',]
                if obj:
                    fields += ['url']
            return fields

    def get_readonly_fields(self, request, obj=None):
        if request.site.domain != 'www.slcschools.org':
            if obj:
                if obj.pagelayout.namespace in obj.TYPES:
                    fields = obj.TYPES[obj.pagelayout.namespace]['readonly_fields']
                else:
                    fields = []
            else:
                fields = ['title']
            # When adding fields with append below you should
            # have a matching remove. For some reason if you
            # do not fields appear inconsistently for different
            # users.
            if request.user.is_superuser:
                if 'title' in fields:
                    fields.remove('title')
            else:
                if 'title' not in fields:
                    fields.append('title')
            return fields
        elif request.site.domain == 'www.slcschools.org':
            fields = ['title','update_user','update_date','create_user','create_date',]
            if request.user.is_superuser:
                fields.remove('title')
                if obj:
                    fields += ['url']
            return fields

    inlines = [ActionButtonInline,FAQInline,ResourceLinkInline,DocumentInline,SubPageInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if request.site.domain != 'www.slcschools.org':
            if obj:
                if obj.pagelayout.namespace in obj.TYPES:
                    inlines = obj.TYPES[obj.pagelayout.namespace]['inlines']
                else:
                    inlines = []
            else:
                inlines = []
            inlines = [getattr(sys.modules[__name__], inline) for inline in inlines]
        if request.site.domain == 'www.slcschools.org':
            inlines = self.inlines

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances

    def get_formsets_with_inlines(self, request, obj=None):
        if request.site.domain != 'www.slcschools.org':
            for inline in self.get_inline_instances(request, obj):
                yield inline.get_formset(request, obj), inline
        if request.site.domain == 'www.slcschools.org':
            for inline in self.get_inline_instances(request, obj):
                # Remove delete fields is not superuser
                if request.user.is_superuser or request.user.has_perm(inline.model._meta.model_name + '.' + get_permission_codename('restore',inline.model._meta)):
                    if 'deleted' not in inline.fields:
                        inline.fields.append('deleted')
                else:
                    while 'deleted' in inline.fields:
                        inline.fields.remove('deleted')
                if obj:
                    if obj.url == '/search/':
                        if not isinstance(inline, FAQInline):
                            continue
                    else:
                        if isinstance(inline, FAQInline):
                            continue
                yield inline.get_formset(request, obj), inline

    def get_list_display(self, request):
        if request.user.has_perm('pages.restore_page'):
            return ['tree_actions', 'indented_title','update_date','update_user','published','deleted']
        else:
            return ['tree_actions', 'indented_title','update_date','update_user','published']

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
            return (DeletedListFilter, 'published')
        else:
            return ['published', ]

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
      fields = [['title', 'school_number'], 'body','building_location','main_phone','main_fax','enrollment','openenrollmentstatus','schooltype','schooloptions','website_url','scc_url','calendar_url','donate_url','boundary_map','primary_contact',['update_user','update_date',],['create_user','create_date',],]
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


class AnnouncementAdmin(
    MPTTModelAdmin,
    GuardedModelAdmin,
):

    # inlines = [PhotoGalleryImageInline, ]

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
        fields = ['title', 'body', ['update_user','update_date',],['create_user','create_date',],]
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
            return ['title', 'update_date','update_user','published','deleted']
        else:
            return ['title', 'update_date','update_user','published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('announcement.restore_document'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('announcement.trash_document'):
            actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('announcement.restore_document'):
            actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('announcement.change_document'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions

    def get_list_filter(self, request):
        if request.user.has_perm('announcement.restore_document'):
            return (DeletedListFilter, 'published')
        else:
            return ['published', ]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change


class SchoolFacultyAdmin(
    MPTTModelAdmin,
    GuardedModelAdmin,
):

    inlines = [DisclosureDocumentInline, ClassWebsiteInline, ]

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
        fields = ['title', 'body', ['update_user','update_date',],['create_user','create_date',],]
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
            return ['title', 'update_date','update_user','published','deleted']
        else:
            return ['title', 'update_date','update_user','published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('schoolfaculty.restore_document'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('schoolfaculty.trash_document'):
            actions['trash_selected'] = (trash_selected,'trash_selected',trash_selected.short_description)
        if request.user.has_perm('schoolfaculty.restore_document'):
            actions['restore_selected'] = (restore_selected,'restore_selected',restore_selected.short_description)
        if request.user.has_perm('schoolfaculty.change_document'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions

    def get_list_filter(self, request):
        if request.user.has_perm('schoolfaculty.restore_document'):
            return (DeletedListFilter, 'published')
        else:
            return ['published', ]

    has_change_permission = apps.common.functions.has_change_permission
    has_add_permission = apps.common.functions.has_add_permission
    has_delete_permission = apps.common.functions.has_delete_permission
    save_formset = apps.common.functions.save_formset
    save_model = apps.common.functions.save_model
    response_change = apps.common.functions.response_change


class DisclosureDocumentAdmin(MPTTModelAdmin, GuardedModelAdmin):
    inlines = [FileInline, ]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Remove delete fields is not superuser
            if request.user.is_superuser or request.user.has_perm(
                    inline.model._meta.model_name + '.' + get_permission_codename('restore', inline.model._meta)):
                if not 'deleted' in inline.fields:
                    inline.fields.append('deleted')
            else:
                while 'deleted' in inline.fields:
                    inline.fields.remove('deleted')
            yield inline.get_formset(request, obj), inline

    def get_fields(self, request, obj=None):
        fields = ['title', ['update_user', 'update_date', ], ['create_user', 'create_date', ], ]
        if request.user.is_superuser:
            fields += ['published', 'searchable', 'parent', ]
            if obj:
                fields += ['url']
        return fields

    def get_readonly_fields(self, request, obj=None):
        fields = ['title', 'update_user', 'update_date', 'create_user', 'create_date', ]
        if request.user.is_superuser:
            fields.remove('title')
            if obj:
                fields += ['url']
        return fields

    def get_list_display(self, request):
        if request.user.has_perm('documents.restore_disclosuredocument'):
            return ['title', 'update_date', 'update_user', 'published', 'deleted']
        else:
            return ['title', 'update_date', 'update_user', 'published']

    # ordering = ('url',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.has_perm('documents.restore_disclosuredocument'):
            return qs
        return qs.filter(deleted=0)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.has_perm('documents.trash_disclosuredocument'):
            actions['trash_selected'] = (trash_selected, 'trash_selected', trash_selected.short_description)
        if request.user.has_perm('documents.restore_disclosuredocument'):
            actions['restore_selected'] = (restore_selected, 'restore_selected', restore_selected.short_description)
        if request.user.has_perm('documents.change_disclosuredocument'):
            actions['publish_selected'] = (publish_selected, 'publish_selected', publish_selected.short_description)
            actions['unpublish_selected'] = (
            unpublish_selected, 'unpublish_selected', unpublish_selected.short_description)
        return actions

    def get_list_filter(self, request):
        if request.user.has_perm('documents.restore_disclosuredocument'):
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
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(SchoolFaculty, SchoolFacultyAdmin)
admin.site.register(DisclosureDocument, DisclosureDocumentAdmin)
