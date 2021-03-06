from django.db import models
import apps.common.functions as commonfunctions
from apps.objects.models import Node, Taxonomy
import apps.taxonomy.help_text as apphelp


class Location(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/locations/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        db_column='location',
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )
    street_address = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
    )
    location_city = models.ForeignKey(
        'City',
        db_column='city',
        to_field='city_taxonomy_node',
        on_delete=models.PROTECT,
        related_name='taxonomy_location_city',
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
    )
    location_state = models.ForeignKey(
        'State',
        db_column='state',
        to_field='state_taxonomy_node',
        on_delete=models.PROTECT,
        related_name='taxonomy_location_state',
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
    )
    location_zipcode = models.ForeignKey(
        'Zipcode',
        db_column='zipcode',
        to_field='zipcode_taxonomy_node',
        on_delete=models.PROTECT,
        related_name='taxonomy_location_zipcode',
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
    )
    google_place = models.URLField(
        max_length=2048,
        blank=True,
        null=True,
        help_text='',
    )

    location_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='location_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_location'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_location', 'Can soft delete location'),
            ('restore_location', 'Can restore location'),
        )
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class City(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/cities/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        db_column='city',
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )

    city_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='city_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_city'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_city', 'Can soft delete city'),
            ('restore_city', 'Can restore city'),
        )
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class State(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/states/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        db_column='state',
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )

    state_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='state_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_state'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_state', 'Can soft delete state'),
            ('restore_state', 'Can restore state'),
        )
        verbose_name = 'State'
        verbose_name_plural = 'States'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Zipcode(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/zipcodes/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        db_column='zipcode',
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )

    zipcode_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='zipcode_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_zipcode'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_zipcode', 'Can soft delete zipcode'),
            ('restore_zipcode', 'Can restore zipcode'),
        )
        verbose_name = 'ZIP Code'
        verbose_name_plural = 'ZIP Codes'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Language(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/languages/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        db_column='language',
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='Language',
        db_index=True,
    )
    native_language = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='Native Language Spelling',
    )
    language_code = models.CharField(
        max_length=5,
        unique=True,
        help_text='',
        verbose_name='Google Language Code',
    )
    iso_639_1_language_code = models.CharField(
        null=True,
        blank=True,
        max_length=7,
        unique=True,
        help_text='',
        verbose_name='ISO 639-1 Language Code',
    )
    language_translationtype = models.ForeignKey(
        'TranslationType',
        db_column='translationtype',
        to_field='translationtype_taxonomy_node',
        on_delete=models.PROTECT,
        limit_choices_to={
            'deleted': False,
        },
        related_name='taxonomy_language_translationtype',
        verbose_name='Translation Type',
    )

    language_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='language_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_language'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_language', 'Can soft delete language'),
            ('restore_language', 'Can restore language'),
        )
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class TranslationType(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/translation-types/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        db_column='translationtype',
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='Translation Link Type',
        db_index=True,
    )

    translationtype_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='translationtype_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_translationtype'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_translationtype', 'Can soft delete translation type'),
            ('restore_translationtype', 'Can restore translation type'),
        )
        verbose_name = 'Translation Type'
        verbose_name_plural = 'Translation Types'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolType(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/school-types/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )

    schooltype_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='schooltype_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_schooltype'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_schooltype', 'Can soft delete school type'),
            ('restore_schooltype', 'Can restore school type'),
        )
        verbose_name = 'School Type'
        verbose_name_plural = 'School Types'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class OpenEnrollmentStatus(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/open-enrollment-statuses/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )

    openenrollmentstatus_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='openenrollmentstatus_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_openenrollmentstatus'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_openenrollmentstatus',
                'Can soft delete school open enrollment status'),
            ('restore_openenrollmentstatus',
                'Can restore school open enrollment status'))
        verbose_name = 'Open Enrollment Status'
        verbose_name_plural = 'Open Enrollment Statuses'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolAdministratorType(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/school-administrator-types/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        db_index=True,
    )

    schooladministratortype_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='schooladministratortype_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_schooladministratortype'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_schooladministratortype',
                'Can soft delete school administrator type'),
            ('restore_schooladministratortype',
                'Can restore school administrator type'))
        verbose_name = 'School Administrator Type'
        verbose_name_plural = 'School Administrator Types'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardPrecinct(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/board-precinct/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
    )

    boardprecinct_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='boardprecinct_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_boardprecinct'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardprecinct', 'Can soft delete board precinct'),
            ('restore_boardprecinct', 'Can restore board precinct'),
        )
        verbose_name = 'Board Precinct'
        verbose_name_plural = 'Board Precincts'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMeetingType(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/board-meeting-type/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
    )

    boardmeetingtype_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='boardmeetingtype_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_boardmeetingtype'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardmeetingtype', 'Can soft delete board meeting type'),
            ('restore_boardprecinct', 'Can restore board meeting type'),
        )
        verbose_name = 'Board Meeting Type'
        verbose_name_plural = 'Board Meeting Types'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardPolicySection(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/board-policy-section/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        verbose_name="Policy Section Name",
    )
    description = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Policy Section Description',
    )
    section_prefix = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )

    boardpolicysection_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='boardpolicysection_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_boardpolicysection'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_boardpolicysection',
                'Can soft delete board policy section'),
            ('restore_boardpolicysection', 'Can restore board policy section'),
        )
        verbose_name = 'Board Policy Section'
        verbose_name_plural = 'Board Policy Sections'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictCalendarEventCategory(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/district-calendar-event-categories/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='District Calendar Event Category',
    )
    css_class = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='CSS Class used on events of this type',
    )

    districtcalendareventcategory_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='districtcalendareventcategory_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_districtcalendareventcategory'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtcalendareventcategory',
                'Can soft delete district calendar event category'),
            ('restore_districtcalendareventcategory',
                'Can restore district calendar event category'))
        verbose_name = 'District Calendar Event Category'
        verbose_name_plural = 'District Calendar Event Categories'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogoGroup(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/district-logo-groups/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='District Logo Group',
    )

    districtlogogroup_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='districtlogogroup_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_districtlogogroup'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogogroup', 'Can soft delete district logo group'),
            ('restore_districtlogogroup', 'Can restore district logo group'),
        )
        verbose_name = 'District Logo Group'
        verbose_name_plural = 'District Logo Groups'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class DistrictLogoStyleVariation(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/district-logo-style-variations/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='District Logo Style Variation',
    )

    districtlogostylevariation_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='districtlogostylevariation_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_districtlogostylevariation'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_districtlogostylevariation',
                'Can soft delete district logo style variation'),
            ('restore_districtlogostylevariation',
                'Can restore district logo style variation'))
        verbose_name = 'District Logo Style Variation'
        verbose_name_plural = 'District Logo Style Variations'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolOption(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = '/taxonomy/school-options/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        unique=True,
        help_text='',
        verbose_name='School Option',
    )

    schooloption_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='schooloption_taxonomy_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'taxonomy_schooloption'
        get_latest_by = 'update_date'
        permissions = (
            ('trash_schooloption', 'Can soft delete school option'),
            ('restore_schooloption', 'Can restore school option'),
        )
        verbose_name = 'School Option'
        verbose_name_plural = 'School Options'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SubjectGradeLevel(Taxonomy):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/subjects-grade-levels/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
        db_index=True,
    )

    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='taxonomy_subjectgradelevel_node',
        editable=False,
        on_delete=models.CASCADE
    )

    subjectgradelevel_taxonomy_node = models.OneToOneField(
        Taxonomy,
        db_column='subjectgradelevel_taxonomy_node',
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
        db_table = 'taxonomy_subjectgradelevel'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'update_date'
        permissions = (
            ('trash_subjectgradelevel', 'Can soft delete Subject or Grade Level'),
            ('restore_subjectgradelevel', 'Can restore Subject or Grade Level'),
        )
        verbose_name = 'Subject or Grade Level'
        verbose_name_plural = 'Subjects and Grade Levels'
        default_manager_name = 'base_manager'

    def __str__(self):
        return self.title

    def force_title(self):
        return self.title if self.title else ''

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
