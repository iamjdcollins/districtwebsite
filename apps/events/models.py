from django.db import models
from django.utils import timezone
import apps.common.functions as commonfunctions
from apps.objects.models import Node, Event as BaseEvent
from apps.taxonomy.models import Location, BoardMeetingType, \
    DistrictCalendarEventCategory
from apps.pages.models import BoardMeetingYear, DistrictCalendarYear


class BoardMeeting(BaseEvent):

    PARENT_TYPE = BoardMeetingYear
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    startdate = models.DateTimeField(
        default=commonfunctions.next_tuesday_sixthrity,
        unique=False,
        verbose_name="Start Date and Time",
    )
    originaldate = models.DateTimeField(
        unique=False,
        verbose_name="Original Start Date and Time",
    )
    originalinstance = models.PositiveIntegerField(
        unique=False,
        blank=True,
        null=True,
    )
    schoolyear = models.CharField(
        max_length=7,
        help_text='',
    )
    yearend = models.CharField(
        max_length=4,
        help_text='',
    )
    building_location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        default=commonfunctions.get_district_office,
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='events_boardmeeting_build_location',
    )
    non_district_location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
        verbose_name='Name of Non-District Location',
    )
    non_district_location_google_place = models.URLField(
        max_length=2048,
        blank=True,
        null=True,
        help_text='',
        verbose_name='Name of Non-District Location Google Place',
    )
    cancelled = models.BooleanField(
        default=False,
    )
    meeting_type = models.ManyToManyField(
        BoardMeetingType,
        blank=True,
        related_name='events_boardmeeting_meeting_type',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='events_boardmeeting_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    event_boardmeeting_node = models.OneToOneField(
        BaseEvent,
        db_column='event_boardmeeting_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'events_boardmeeting'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeeting', 'Can soft delete board meeting'),
            ('restore_boardmeeting', 'Can restore board meeting'),
        )
        verbose_name = 'Board Meeting'
        verbose_name_plural = 'Board Meetings'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return timezone.localtime(
            self.originaldate).strftime(
            '%Y%m%d-%H%M') + '-' + str(self.originalinstance)

    def create_parent(self, creator):
        currentyear = commonfunctions.currentyear(self.startdate)
        parent = Node.objects.get(url=self.PARENT_TYPE.PARENT_URL, site=self.site)
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


class DistrictCalendarEvent(BaseEvent):

    PARENT_TYPE = DistrictCalendarYear
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    originaldate = models.DateTimeField(
        unique=False,
        verbose_name="Original Start Date and Time",
        db_index=True,
    )
    originalinstance = models.PositiveIntegerField(
        unique=False,
        blank=True,
        null=True,
    )
    event_name = models.CharField(
        max_length=400,
        blank=True,
        null=True,
        help_text='',
    )
    event_category = models.ForeignKey(
        DistrictCalendarEventCategory,
        blank=True,
        related_name='events_districtcalendarevent_event_type',
        default=commonfunctions.get_districtcalendareventcategory_general,
        on_delete=models.PROTECT,
    )
    startdate = models.DateTimeField(
        default=commonfunctions.tomorrow_midnight,
        unique=False,
        verbose_name="Start Date and Time",
        db_index=True,
    )
    enddate = models.DateTimeField(
        blank=True,
        null=True,
        unique=False,
        verbose_name="End Date and Time",
    )
    schoolyear = models.CharField(
        max_length=7,
        help_text='',
    )
    yearend = models.CharField(
        max_length=4,
        help_text='',
    )
    building_location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        default='',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
        related_name='events_districtcalendarevent_build_location',
    )
    non_district_location = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
        verbose_name='Name of Non-District Location',
    )
    non_district_location_google_place = models.URLField(
        max_length=2048,
        blank=True,
        null=True,
        help_text='',
        verbose_name='Name of Non-District Location Google Place',
    )
    cancelled = models.BooleanField(
        default=False,
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='events_districtcalendarevent_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    districtcalendarevent_event_node = models.OneToOneField(
        BaseEvent,
        db_column='districtcalendarevent_event_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'events_districtcalendarevent'
        ordering = ['startdate', ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtcalendarevent',
                'Can soft delete district calendar event'),
            ('restore_districtcalendarevent',
                'Can restore district calendar event'),
        )
        verbose_name = 'District Calendar Event'
        verbose_name_plural = 'District Calendar Events'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return timezone.localtime(
            self.originaldate).strftime(
            '%Y%m%d-%H%M') + '-' + str(self.originalinstance)

    def create_parent(self, creator):
        currentyear = commonfunctions.currentyear(self.startdate)
        parent = Node.objects.get(url=self.PARENT_TYPE.PARENT_URL, site=self.site)
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
