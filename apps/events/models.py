from django.db import models
import apps.common.functions
from apps.objects.models import Node, Event as BaseEvent
from apps.taxonomy.models import Location, BoardMeetingType
from apps.pages.models import BoardMeetingYear, DistrictCalendarYear

class BoardMeeting(BaseEvent):

    PARENT_URL = ''
    URL_PREFIX = ''
    PARENT_TYPE = BoardMeetingYear

    title = models.CharField(max_length=200, help_text='')
    startdate = models.DateTimeField(default=apps.common.functions.next_tuesday_sixthrity, unique=False, verbose_name="Start Date and Time")
    originaldate = models.DateTimeField(unique=False, verbose_name="Original Start Date and Time")
    schoolyear = models.CharField(max_length=7, help_text='')
    yearend = models.CharField(max_length=4, help_text='')
    building_location = models.ForeignKey(Location, null=True, blank=True, default=apps.common.functions.get_district_office, on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='events_boardmeeting_build_location')
    non_district_location = models.CharField(max_length=200, null=True, blank=True, help_text='', verbose_name='Name of Non-District Location')
    non_district_location_google_place = models.URLField(max_length=2048, blank=True,null=True, help_text='', verbose_name='Name of Non-District Location Google Place')
    cancelled = models.BooleanField(default=False)
    meeting_type = models.ManyToManyField(BoardMeetingType, blank=True, related_name='events_boardmeeting_meeting_type')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='events_boardmeeting_node', editable=False)

    event_boardmeeting_node = models.OneToOneField(BaseEvent, db_column='event_boardmeeting_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'events_boardmeeting'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeeting', 'Can soft delete board meeting'),('restore_boardmeeting', 'Can restore board meeting'))
        verbose_name = 'Board Meeting'
        verbose_name_plural = 'Board Meetings'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.eventsave
    delete = apps.common.functions.modeltrash

class DistrictCalendarEvent(BaseEvent):

    PARENT_URL = ''
    URL_PREFIX = ''
    PARENT_TYPE = DistrictCalendarYear

    title = models.CharField(max_length=200, help_text='')
    originaldate = models.DateTimeField(unique=False, verbose_name="Original Start Date and Time")
    startdate = models.DateTimeField(default=apps.common.functions.tomorrow_midnight, unique=False, verbose_name="Start Date and Time")
    enddate = models.DateTimeField(default='', unique=False, verbose_name="Start Date and Time")
    schoolyear = models.CharField(max_length=7, help_text='')
    yearend = models.CharField(max_length=4, help_text='')
    building_location = models.ForeignKey(Location, null=True, blank=True, default='', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='events_districtcalendarevent_build_location')
    non_district_location = models.CharField(max_length=200, null=True, blank=True, help_text='', verbose_name='Name of Non-District Location')
    non_district_location_google_place = models.URLField(max_length=2048, blank=True,null=True, help_text='', verbose_name='Name of Non-District Location Google Place')
    cancelled = models.BooleanField(default=False)
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='events_districtcalendarevent_node', editable=False)

    districtcalendarevent_event_node = models.OneToOneField(BaseEvent, db_column='districtcalendarevent_event_node', on_delete=models.CASCADE, parent_link=True, editable=False)

    class Meta:
        db_table = 'events_districtcalendarevent'
        get_latest_by = 'update_date'
        permissions = (('trash_districtcalendarevent', 'Can soft delete district calendar event'),('restore_districtcalendarevent', 'Can restore district calendar event'))
        verbose_name = 'District Calendar Event'
        verbose_name_plural = 'District Calendar Events'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.eventsave
    delete = apps.common.functions.modeltrash
