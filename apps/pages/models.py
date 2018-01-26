from django.db import models
from ckeditor.fields import RichTextField
import apps.common.functions
from apps.objects.models import Node, Page as BasePage
from apps.pages.help import PageHelp
from apps.taxonomy.models import Location, SchoolType, OpenEnrollmentStatus, \
    SchoolOption
from django.utils import timezone


class Page(BasePage):

    HAS_PERMISSIONS = True

    title = models.CharField(
        max_length=200,
        help_text='',
        db_index=True
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text=PageHelp.body
    )

    page_page_node = models.OneToOneField(
        BasePage,
        db_column='page_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_page'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_page', 'Can soft delete page'),
            ('restore_page', 'Can restore page')
        )
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class School(BasePage):

    HAS_PERMISSIONS = True

    THUMBNAILS = True
    CONTENTBANNERS = True
    SCHOOLADMINISTRATORS = True

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text=''
    )
    building_location = models.ForeignKey(
        Location,
        to_field='location_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_school_building_location'
    )
    main_phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text=''
    )
    main_fax = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text=''
    )
    enrollment = models.PositiveIntegerField(
        help_text='',
        null=True,
        blank=True
    )
    schooltype = models.ForeignKey(
        SchoolType,
        to_field='schooltype_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_school_schooltype'
    )
    website_url = models.URLField(
        max_length=2048,
        null=True,
        blank=True,
        help_text=''
    )
    scc_url = models.URLField(
        max_length=2048,
        help_text="",
        null=True,
        blank=True
    )
    calendar_url = models.URLField(
        max_length=2048,
        help_text="",
        null=True,
        blank=True,
        verbose_name="School Calendar URL"
    )
    donate_url = models.URLField(
        max_length=2048,
        help_text="",
        null=True,
        blank=True,
        verbose_name="School Donation URL"
    )
    boundary_map = models.URLField(
        max_length=2048,
        help_text='',
        null=True,
        blank=True
    )
    openenrollmentstatus = models.ForeignKey(
        OpenEnrollmentStatus,
        null=True,
        blank=True,
        to_field='openenrollmentstatus_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_school_openenrollmentstatus',
    )
    schooloptions = models.ManyToManyField(
        SchoolOption,
        blank=True,
        related_name='pages_school_schooloptions',
        verbose_name='School Options',
    )

    school_page_node = models.OneToOneField(
        BasePage,
        db_column='school_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_school'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_school', 'Can soft delete school'),
            ('restore_school', 'Can restore school'),
        )
        verbose_name = 'School'
        verbose_name_plural = 'Schools'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class Department(BasePage):

    HAS_PERMISSIONS = True

    CONTENTBANNER = True
    STAFF = True
    RESOURCELINK = True
    DOCUMENT = True
    SUBPAGE = True

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text='',
    )
    short_description = models.TextField(
        max_length=2000,
        verbose_name='Short Description',
        null=True,
        blank=True,
    )
    building_location = models.ForeignKey(
        Location,
        to_field='location_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_department_building_location',
    )
    main_phone = models.CharField(
        max_length=11,
        default='18015780000',
        help_text=''
    )
    main_fax = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='',
    )
    is_department = models.BooleanField(
        default=False,
        db_index=True,
    )

    department_page_node = models.OneToOneField(
        BasePage,
        db_column='department_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_department'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_department', 'Can soft delete department'),
            ('restore_department', 'Can restore department')
        )
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class Board(BasePage):

    HAS_PERMISSIONS = True

    CONTENTBANNER = True

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text='',
    )
    building_location = models.ForeignKey(
        Location,
        to_field='location_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_board_building_location',
    )
    main_phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='',
    )
    main_fax = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='',
    )
    mission_statement = models.TextField(
        max_length=2000,
        help_text='',
        verbose_name='Mission Statement',
        null=True,
        blank=True,
    )
    vision_statement = models.TextField(
        max_length=2000,
        help_text='',
        verbose_name='Vision Statement',
        null=True,
        blank=True,
    )

    board_page_node = models.OneToOneField(
        BasePage, db_column='board_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_board'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_board', 'Can soft delete board'),
            ('restore_board', 'Can restore board'),
        )
        verbose_name = 'Board'
        verbose_name_plural = 'Board'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class BoardSubPage(BasePage):

    HAS_PERMISSIONS = True

    CONTENTBANNER = True
    STAFF = True
    RESOURCELINK = True
    DOCUMENT = True
    SUBPAGE = True

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text='',
    )
    building_location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_boardsubpage_building_location',
    )
    main_phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='',
    )
    main_fax = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='pages_boardsubpage_node',
        editable=False,
    )

    boardsubpage_page_node = models.OneToOneField(
        BasePage,
        db_column='boardsubpage_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    inline_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True,
    )

    class Meta:
        db_table = 'pages_boardsubpage'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardsubpage', 'Can soft delete board subpage'),
            ('restore_boardsubpage', 'Can restore board subpage')
        )
        verbose_name = 'Board Subpage'
        verbose_name_plural = 'Board Subpages'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class BoardMeetingYear(BasePage):

    PARENT_URL = '/board-of-education/board-meetings/'

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
    )
    yearend = models.CharField(
        max_length=4,
        unique=True,
        help_text='',
        blank=True,
    )

    boardmeetingyear_page_node = models.OneToOneField(
        BasePage,
        db_column='boardmeetingyear_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_boardmeetingyear'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingyear', 'Can soft delete board meeting year'),
            ('restore_boardmeetingyear', 'Can restore board meeting year')
        )
        verbose_name = 'Board Meeting Year'
        verbose_name_plural = 'Board Meeting Years'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class NewsYear(BasePage):

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="",
    )
    yearend = models.CharField(
        max_length=4,
        unique=True,
        help_text="",
        blank=True,
    )

    newsyear_page_node = models.OneToOneField(
        BasePage,
        db_column='newsyear_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_newsyear'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_newsyear', 'Can soft delete newsyear'),
            ('restore_newsyear', 'Can restore newsyear'),
        )
        verbose_name = 'News Year'
        verbose_name_plural = 'News Years'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class News(BasePage):

    PARENT_TYPE = NewsYear

    title = models.CharField(
        max_length=200,
        unique=False,
        help_text="",
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text="",
    )
    summary = RichTextField(
        max_length=400,
        null=True,
        blank=True,
        help_text="",
    )
    pinned = models.BooleanField(
        default=False,
    )
    author_date = models.DateTimeField(
        default=timezone.now,
    )

    news_page_node = models.OneToOneField(
        BasePage,
        db_column='news_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_news'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_news', 'Can soft delete news'),
            ('restore_news', 'Can restore news')
        )
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = [
            '-author_date',
        ]
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class SuperintendentMessageYear(BasePage):

    PARENT_URL = '/departments/superintendents-office/superintendents-message/'

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="",
    )
    yearend = models.CharField(
        max_length=4,
        unique=True,
        help_text="",
        blank=True,
    )

    superintendentmessageyear_page_node = models.OneToOneField(
        BasePage,
        db_column='superintendentmessage_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_superintendentmessageyear'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_superintendentmessageyear',
                'Can soft delete superintendent message year'),
            ('restore_superintendentmessageyear',
                'Can restore superintendent message year')
        )
        verbose_name = 'Superintendent Message Year'
        verbose_name_plural = 'Superintendent Message Years'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return 'Superintendent\'s Message ' + \
            self.author_date.strftime('%Y-%m-%d')

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class SuperintendentMessage(BasePage):

    PARENT_TYPE = SuperintendentMessageYear

    title = models.CharField(
        max_length=200,
        unique=False,
        help_text="",
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text="",
    )
    summary = RichTextField(
        max_length=400,
        null=True,
        blank=True,
        help_text="",
    )
    author_date = models.DateTimeField(
        default=timezone.now,
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='pages_superintendentmessage_node',
        editable=False,
    )

    superintendentmessage_page_node = models.OneToOneField(
        BasePage,
        db_column='superintendentmessage_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_superintendentmessage'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_superintendentmessage',
                'Can soft delete superintendent message'),
            ('restore_superintendentmessage',
                'Can restore superintendent message'))
        verbose_name = 'Superintendent Message'
        verbose_name_plural = 'Superintendent Messages'
        ordering = [
            '-author_date',
        ]
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class SubPage(BasePage):

    CONTENTBANNER = True
    STAFF = True
    RESOURCELINK = True
    DOCUMENT = True

    title = models.CharField(
        max_length=200,
        help_text='',
        db_index=True,
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text=PageHelp.body,
    )
    building_location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        to_field='location_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='pages_subpage_building_location',
    )
    main_phone = models.CharField(
        max_length=11,
        null=True,
        blank=True, help_text='',
    )
    main_fax = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='pages_subpage_node',
        editable=False,
    )

    subpage_page_node = models.OneToOneField(
        BasePage,
        db_column='subpage_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    inline_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        db_index=True
    )

    class Meta:
        db_table = 'pages_subpage'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_subpage', 'Can soft delete subpage'),
            ('restore_subpage', 'Can restore subpage'),
        )
        verbose_name = 'Subpage'
        verbose_name_plural = 'Subpages'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash


class DistrictCalendarYear(BasePage):

    PARENT_URL = '/calendars/'

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="",
    )
    yearend = models.CharField(
        max_length=4,
        unique=True,
        help_text="",
        blank=True,
    )

    districtcalendaryear_page_node = models.OneToOneField(
        BasePage,
        db_column='districtcalendaryear_page_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'pages_districtcalendaryear'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtcalendaryear',
                'Can soft delete district calendar year'),
            ('restore_districtcalendaryear',
                'Can restore district calendar year')
        )
        verbose_name = 'District Calendar Year'
        verbose_name_plural = 'District Calendar Years'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = apps.common.functions.pagesave
    delete = apps.common.functions.modeltrash
