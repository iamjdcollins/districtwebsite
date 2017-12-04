from django.conf import settings
from django.db import models
from guardian.shortcuts import assign_perm
from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group
import apps.common.functions
from apps.objects.models import Node, Page as BasePage
from apps.pages.help import PageHelp
from django.contrib.auth import get_permission_codename
from apps.taxonomy.models import Location, SchoolType, OpenEnrollmentStatus
from apps.images.models import Thumbnail, PageBanner, ContentBanner
from apps.directoryentries.models import SchoolAdministrator
from django.utils import timezone

# Create your models here.

class Page(BasePage):

  HAS_PERMISSIONS = True

  title = models.CharField(max_length=200, help_text='',db_index=True)
  body = RichTextField(null=True, blank=True, help_text=PageHelp.body)

  page_page_node = models.OneToOneField(BasePage, db_column='page_page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'pages_page'
    get_latest_by = 'update_date'
    permissions = (('trash_page', 'Can soft delete page'),('restore_page', 'Can restore page'))
    verbose_name = 'Page'
    verbose_name_plural = 'Pages'

  def __str__(self):
    return self.title

  save = apps.common.functions.pagesave
  delete = apps.common.functions.modeltrash

class School(BasePage):

  HAS_PERMISSIONS = True
  
  THUMBNAILS = True
  CONTENTBANNERS = True
  SCHOOLADMINISTRATORS = True

  title = models.CharField(max_length=200, unique=True, help_text='',db_index=True)
  body = RichTextField(null=True, blank=True, help_text='')
  building_location = models.ForeignKey(Location, to_field='location_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='pages_school_building_location')
  main_phone = models.CharField(max_length=11, null=True, blank=True, help_text='')
  main_fax = models.CharField(max_length=11, null=True, blank=True, help_text='')
  enrollment = models.PositiveIntegerField(help_text='', null=True, blank=True)
  schooltype = models.ForeignKey(SchoolType, to_field='schooltype_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='pages_school_schooltype')
  website_url = models.URLField(max_length=2048, null=True, blank=True, help_text='')
  scc_url = models.URLField(max_length=2048, help_text="", null=True, blank=True)
  boundary_map = models.URLField(max_length=2048, help_text='', null=True, blank=True)
  openenrollmentstatus = models.ForeignKey(OpenEnrollmentStatus, null=True, blank=True, to_field='openenrollmentstatus_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='pages_school_openenrollmentstatus')

  school_page_node = models.OneToOneField(BasePage, db_column='school_page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  def thumbnails(self):
    return Thumbnail.objects.filter(parent=self.pk)

  def contentbanners(self):
    return ContentBanner.objects.filter(parent=self.pk)

  def schooladministrators(self):
    return SchoolAdministrator.objects.filter(parent=self.pk)

  def resourcelinks(self):
    return self.links_resourcelink_node.all()

  class Meta:
    db_table = 'pages_school'
    get_latest_by = 'update_date'
    permissions = (('trash_school', 'Can soft delete school'),('restore_school', 'Can restore school'))
    verbose_name = 'School'
    verbose_name_plural = 'Schools'

  def __str__(self):
    return self.title

  save = apps.common.functions.pagesave
  delete = apps.common.functions.modeltrash

class Department(BasePage):

    HAS_PERMISSIONS = True

    CONTENTBANNER = True
    STAFF = True
    RESOURCELINK = True
    DOCUMENT = True
    SUBPAGE = True

    title = models.CharField(max_length=200, unique=True, help_text='',db_index=True)
    body = RichTextField(null=True, blank=True, help_text='')
    short_description = models.TextField(max_length=2000, verbose_name='Short Description', null=True, blank=True,)
    building_location = models.ForeignKey(Location, to_field='location_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='pages_department_building_location')
    main_phone = models.CharField(max_length=11, null=True, blank=True, help_text='')
    main_fax = models.CharField(max_length=11, null=True, blank=True, help_text='')

    department_page_node = models.OneToOneField(BasePage, db_column='department_page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'pages_department'
        get_latest_by = 'update_date'
        permissions = (('trash_department', 'Can soft delete department'),('restore_department', 'Can restore department'))
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.title

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash

class Board(BasePage):

    HAS_PERMISSIONS = True

    CONTENTBANNER = True

    title = models.CharField(max_length=200, unique=True, help_text='',db_index=True)
    body = RichTextField(null=True, blank=True, help_text='',)
    building_location = models.ForeignKey(Location, to_field='location_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='pages_board_building_location')
    main_phone = models.CharField(max_length=11, null=True, blank=True,help_text='',)
    main_fax = models.CharField(max_length=11, null=True, blank=True,help_text='',)
    mission_statement = models.TextField(max_length=2000, help_text='', verbose_name='Mission Statement', null=True, blank=True,)
    vision_statement = models.TextField(max_length=2000, help_text='', verbose_name='Vision Statement', null=True, blank=True,)

    class Meta:
        db_table = 'pages_board'
        get_latest_by = 'update_date'
        permissions = (('trash_board', 'Can soft delete board'),('restore_board', 'Can restore board'))
        verbose_name = 'Board'
        verbose_name_plural = 'Board'

    def __str__(self):
        return self.title

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash

class BoardSubPage(BasePage):

    HAS_PERMISSIONS = True

    CONTENTBANNER = True
    STAFF = True
    RESOURCELINK = True
    DOCUMENT = True
    SUBPAGE = True

    title = models.CharField(max_length=200, unique=True, help_text='',db_index=True)
    body = RichTextField(null=True, blank=True, help_text='',)
    building_location = models.ForeignKey(Location, to_field='location_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='pages_boardsubpage_building_location')
    main_phone = models.CharField(max_length=11, null=True, blank=True,help_text='',)
    main_fax = models.CharField(max_length=11, null=True, blank=True,help_text='',)

    class Meta:
        db_table = 'pages_boardsubpage'
        get_latest_by = 'update_date'
        permissions = (('trash_boardsubpage', 'Can soft delete board subpage'),('restore_boardsubpage', 'Can restore board subpage'))
        verbose_name = 'Board Subpage'
        verbose_name_plural = 'Board Subpages'

    def __str__(self):
        return self.title

class NewsYear(BasePage):
    title = models.CharField(max_length=200, unique=True, help_text="",)
    yearend = models.CharField(max_length=4, unique=True, help_text="", blank=True)

    newsyear_page_node = models.OneToOneField(BasePage, db_column='newsyear_page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'pages_newsyear'
        get_latest_by = 'update_date'
        permissions = (('trash_newsyear', 'Can soft delete newsyear'),('restore_newsyear', 'Can restore newsyear'))
        verbose_name = 'News Year'
        verbose_name_plural = 'News Years'

    def __str__(self):
        return self.title

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash

class News(BasePage):

    PARENT_TYPE = NewsYear

    title = models.CharField(max_length=200, unique=False, help_text="",)
    body = RichTextField(null=True, blank=True, help_text="",)
    summary = RichTextField(max_length=400, null=True, blank=True, help_text="",)
    pinned = models.BooleanField(default=False,)
    author_date = models.DateTimeField(default=timezone.now,)

    news_page_node = models.OneToOneField(BasePage, db_column='news_page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'pages_news'
        get_latest_by = 'update_date'
        permissions = (('trash_news', 'Can soft delete news'),('restore_news', 'Can restore news'))
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-author_date',]

    def __str__(self):
        return self.title

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash

class SubPage(BasePage):

    CONTENTBANNER = True
    STAFF = True
    RESOURCELINK = True
    DOCUMENT = True

    title = models.CharField(max_length=200, help_text='',db_index=True)
    body = RichTextField(null=True, blank=True, help_text=PageHelp.body)
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='pages_subpage_node', editable=False)

    subpage_page_node = models.OneToOneField(BasePage, db_column='subpage_page_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'pages_subpage'
        get_latest_by = 'update_date'
        permissions = (('trash_subpage', 'Can soft delete subpage'),('restore_subpage', 'Can restore subpage'))
        verbose_name = 'Subpage'
        verbose_name_plural = 'Subpages'

    def __str__(self):
        return self.title

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash
