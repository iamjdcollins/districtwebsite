from django.db import models
from ckeditor.fields import RichTextField
import apps.common.functions as commonfunctions
from apps.objects.models import Node, Page as BasePage
from apps.pages.help import PageHelp
from apps.taxonomy.models import Location, SchoolType, OpenEnrollmentStatus, \
    SchoolOption
from django.utils import timezone


class Page(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = True
    TYPES = {
        'default.html': {
            'fields': [
                'title',
                'body',
                'primary_contact',
                'published',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
                'ResourceLinkInline',
                'DocumentInline',
            ],
        },
        'site-section.html': {
            'fields': [
                'title',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
                'SectionPageInline',
            ],
        },
        'about-our-school.html': {
            'fields': [
                'title',
                'about_our_school',
                'primary_contact',
                'published',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [],
        },
        'administration-staff-directory.html': {
            'fields': [
                'title',
                'primary_contact',
                'published',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
                'SchoolAdministrationInline',
                'SchoolStaffInline',
            ],
        },
        'faculty-directory.html': {
            'fields': [
                'title',
                'primary_contact',
                'published',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
                'SubjectGradeLevelInline',
                'SchoolFacultyInline',
            ],
        },
        'school-home.html': {
            'fields': [
                'title',
                'primary_contact',
                'published',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
                'AnnouncementInline',
                'ActionButtonInline',
            ],
        },
        'school-employees.html': {
            'fields': [
                'title',
                'school_employees',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
            ],
        },
        'school-community-council-scc.html': {
            'fields': [
                'title',
                'body',
                'primary_contact',
                'published',
                ['update_user', 'update_date'],
                ['create_user', 'create_date'],
            ],
            'readonly_fields': [
                'title',
                'update_user',
                'update_date',
                'create_user',
                'create_date',
                'url',
            ],
            'inlines': [
                'SchoolCommunityCouncilMemberInline',
                'SchoolCommunityCouncilMeetingInline',
            ],
        },
    }

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
    about_our_school = models.ForeignKey(
        'School',
        null=True,
        blank=False,
        limit_choices_to={
            'deleted': False,
        },
        related_name='page_about_our_school',
        on_delete=models.SET_NULL,
    )
    school_employees = models.ForeignKey(
        'self',
        null=True,
        blank=False,
        limit_choices_to={
            'url': '/employees/',
            'site__domain': 'www.slcschools.org',
            'published': 1,
            'deleted': 0,
        },
        verbose_name='District Website Employees Page',
        related_name='page_school_employees',
        on_delete=models.CASCADE,
    )

    page_page_node = models.OneToOneField(
        BasePage,
        db_column='page_page_node',
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
        db_table = 'pages_page'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_page', 'Can soft delete page'),
            ('restore_page', 'Can restore page')
        )
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Announcement(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/announcements/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
        db_index=True,
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text=''
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='pages_announcement_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    announcement_page_node = models.OneToOneField(
        BasePage,
        db_column='announcement_page_node',
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
        db_table = 'pages_announcement'
        get_latest_by = 'update_date'
        ordering = [
            'inline_order',
        ]
        permissions = (
            ('trash_announcement', 'Can soft delete announcement'),
            ('restore_announcement', 'Can restore announcement'),
        )
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class School(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = True

    THUMBNAILS = True
    CONTENTBANNERS = True
    SCHOOLADMINISTRATORS = True

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )
    school_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='',
        db_index=True,
        unique=True,
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Department(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Board(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardSubPage(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
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
        on_delete=models.CASCADE,
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingYear(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = '/board-of-education/board-meetings/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class NewsYear(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = '/news/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class News(BasePage):

    PARENT_TYPE = NewsYear
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

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
        max_length=1000,
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    def create_parent(self, creator):
        currentyear = commonfunctions.currentyear(self.author_date)
        parent = Node.objects.get(url=self.PARENT_TYPE.PARENT_URL)
        obj, created = self.PARENT_TYPE.objects.get_or_create(
            title=currentyear['currentyear']['long'],
            yearend=currentyear['currentyear']['short'],
            parent=parent,
            defaults={
                'create_user': creator,
                'update_user': creator,
                'site': self.site,
            },
        )
        return obj

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SuperintendentMessageYear(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = '/departments/superintendents-office/superintendents-message/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SuperintendentMessage(BasePage):

    PARENT_TYPE = SuperintendentMessageYear
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

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
        max_length=1000,
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
        on_delete=models.CASCADE,
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return 'Superintendent\'s Message ' + \
            self.author_date.strftime('%Y-%m-%d')

    def create_parent(self, creator):
        currentyear = commonfunctions.currentyear(self.author_date)
        parent = Node.objects.get(url=self.PARENT_TYPE.PARENT_URL)
        obj, created = self.PARENT_TYPE.objects.get_or_create(
            title=currentyear['currentyear']['long'],
            yearend=currentyear['currentyear']['short'],
            parent=parent,
            defaults={'create_user': creator,
                      'update_user': creator, 'site': self.site},
        )
        return obj

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SubPage(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

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
        on_delete=models.CASCADE,
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictCalendarYear(BasePage):

    PARENT_TYPE = ''
    PARENT_URL = '/calendars/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text="",
    )
    yearend = models.CharField(
        max_length=4,
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
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
