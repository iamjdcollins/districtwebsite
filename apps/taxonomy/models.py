from django.db import models
from django.conf import settings
import uuid
import apps.common.functions
from apps.objects.models import Taxonomy

# Create your models here.

class Location(Taxonomy):
  
  PARENT_URL = '/taxonomy/locations/'

  title = models.CharField(db_column='location',max_length=200, unique=True, help_text='', db_index=True)
  street_address = models.CharField(max_length=200, unique=True, help_text='')
  location_city = models.ForeignKey('City',db_column='city', to_field='city_taxonomy_node', on_delete=models.PROTECT, related_name='taxonomy_location_city', limit_choices_to={'deleted': False,}, help_text='')
  location_state = models.ForeignKey('State',db_column='state', to_field='state_taxonomy_node', on_delete=models.PROTECT, related_name='taxonomy_location_state', limit_choices_to={'deleted': False,}, help_text='')
  location_zipcode = models.ForeignKey('Zipcode',db_column='zipcode', to_field='zipcode_taxonomy_node', on_delete=models.PROTECT, related_name='taxonomy_location_zipcode', limit_choices_to={'deleted': False,}, help_text='')
  google_place = models.URLField(max_length=2048, blank=True,null=True, help_text='')

  location_taxonomy_node = models.OneToOneField(Taxonomy, db_column='location_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_location'
    get_latest_by = 'update_date'
    permissions = (('trash_location', 'Can soft delete location'),('restore_location', 'Can restore location'))
    verbose_name = 'Location'
    verbose_name_plural = 'Locations'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class City(Taxonomy):

  PARENT_URL = '/taxonomy/cities/'

  title = models.CharField(db_column='city',max_length=200, unique=True, help_text='', db_index=True)

  city_taxonomy_node = models.OneToOneField(Taxonomy, db_column='city_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_city'
    get_latest_by = 'update_date'
    permissions = (('trash_city', 'Can soft delete city'),('restore_city', 'Can restore city'))
    verbose_name = 'City'
    verbose_name_plural = 'Cities'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class State(Taxonomy):

  PARENT_URL = '/taxonomy/states/'

  title = models.CharField(db_column='state',max_length=200, unique=True, help_text='', db_index=True)

  state_taxonomy_node = models.OneToOneField(Taxonomy, db_column='state_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_state'
    get_latest_by = 'update_date'
    permissions = (('trash_state', 'Can soft delete state'),('restore_state', 'Can restore state'))
    verbose_name = 'State'
    verbose_name_plural = 'States'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class Zipcode(Taxonomy):

  PARENT_URL = '/taxonomy/zipcodes/'

  title = models.CharField(db_column='zipcode',max_length=200, unique=True, help_text='', db_index=True)

  zipcode_taxonomy_node = models.OneToOneField(Taxonomy, db_column='zipcode_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_zipcode'
    get_latest_by = 'update_date'
    permissions = (('trash_zipcode', 'Can soft delete zipcode'),('restore_zipcode', 'Can restore zipcode'))
    verbose_name = 'ZIP Code'
    verbose_name_plural = 'ZIP Codes'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class Language(Taxonomy):

  PARENT_URL = '/taxonomy/languages/'

  title = models.CharField(db_column='language',max_length=200, unique=True, help_text='', verbose_name='Language', db_index=True)
  native_language =  models.CharField(max_length=200, unique=True, help_text='', verbose_name='Native Language Spelling')
  language_code = models.CharField(max_length=5, unique=True, help_text='', verbose_name='Language Code')
  language_translationtype = models.ForeignKey('TranslationType',db_column='translationtype',to_field='translationtype_taxonomy_node', on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, related_name='taxonomy_language_translationtype', verbose_name='Translation Type')

  language_taxonomy_node = models.OneToOneField(Taxonomy, db_column='language_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_language'
    get_latest_by = 'update_date'
    permissions = (('trash_language', 'Can soft delete language'),('restore_language', 'Can restore language'))
    verbose_name = 'Language'
    verbose_name_plural = 'Languages'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class TranslationType(Taxonomy):

  PARENT_URL = '/taxonomy/translation-types/'

  title = models.CharField(db_column='translationtype',max_length=200, unique=True, help_text='', verbose_name='Translation Link Type', db_index=True)

  translationtype_taxonomy_node = models.OneToOneField(Taxonomy, db_column='translationtype_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_translationtype'
    get_latest_by = 'update_date'
    permissions = (('trash_translationtype', 'Can soft delete translation type'),('restore_translationtype', 'Can restore translation type'))
    verbose_name = 'Translation Type'
    verbose_name_plural = 'Translation Types'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class SchoolType(Taxonomy):

  PARENT_URL = '/taxonomy/school-types/'

  title = models.CharField(max_length=200, unique=True, help_text='', db_index=True)

  schooltype_taxonomy_node = models.OneToOneField(Taxonomy, db_column='schooltype_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_schooltype'
    get_latest_by = 'update_date'
    permissions = (('trash_schooltype', 'Can soft delete school type'),('restore_schooltype', 'Can restore school type'))
    verbose_name = 'School Type'
    verbose_name_plural = 'School Types'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class OpenEnrollmentStatus(Taxonomy):

  PARENT_URL = '/taxonomy/open-enrollment-statuses/'

  title = models.CharField(max_length=200, unique=True, help_text='', db_index=True)

  openenrollmentstatus_taxonomy_node = models.OneToOneField(Taxonomy, db_column='openenrollmentstatus_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_openenrollmentstatus'
    get_latest_by = 'update_date'
    permissions = (('trash_openenrollmentstatus', 'Can soft delete school open enrollment status'),('restore_openenrollmentstatus', 'Can restore school open enrollment status'))
    verbose_name = 'Open Enrollment Status'
    verbose_name_plural = 'Open Enrollment Statuses'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

class SchoolAdministratorType(Taxonomy):

  PARENT_URL = '/taxonomy/school-administrator-types/'

  title = models.CharField(max_length=200, unique=True, help_text='', db_index=True)

  schooladministratortype_taxonomy_node = models.OneToOneField(Taxonomy, db_column='schooladministratortype_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'taxonomy_schooladministratortype'
    get_latest_by = 'update_date'
    permissions = (('trash_schooladministratortype', 'Can soft delete school administrator type'),('restore_schooladministratortype', 'Can restore school administrator type'))
    verbose_name = 'School Administrator Type'
    verbose_name_plural = 'School Administrator Types'
    default_manager_name = 'objects'

  def __str__(self):
    return self.title

  save = apps.common.functions.taxonomysave
  delete = apps.common.functions.modeltrash

class BoardPrecinct(Taxonomy):

    PARENT_URL = '/taxonomy/board-precinct/'

    title = models.CharField(max_length=200, unique=True, help_text='')

    boardprecinct_taxonomy_node = models.OneToOneField(Taxonomy, db_column='boardprecinct_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'taxonomy_boardprecinct'
        get_latest_by = 'update_date'
        permissions = (('trash_boardprecinct', 'Can soft delete board precinct'),('restore_boardprecinct', 'Can restore board precinct'))
        verbose_name = 'Board Precinct'
        verbose_name_plural = 'Board Precincts'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.taxonomysave
    delete = apps.common.functions.modeltrash

class BoardMeetingType(Taxonomy):

    PARENT_URL = '/taxonomy/board-meeting-type/'

    title = models.CharField(max_length=200, unique=True, help_text='')

    boardmeetingtype_taxonomy_node = models.OneToOneField(Taxonomy, db_column='boardmeetingtype_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'taxonomy_boardmeetingtype'
        get_latest_by = 'update_date'
        permissions = (('trash_boardmeetingtype', 'Can soft delete board meeting type'),('restore_boardprecinct', 'Can restore board meeting type'))
        verbose_name = 'Board Meeting Type'
        verbose_name_plural = 'Board Meeting Types'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.taxonomysave
    delete = apps.common.functions.modeltrash

class BoardPolicySection(Taxonomy):

    PARENT_URL = '/taxonomy/board-policy-section/'

    title = models.CharField(max_length=200, unique=True, help_text='',verbose_name="Policy Section Name")
    description = models.CharField(max_length=500,null=True, blank=True,verbose_name='Policy Section Description')
    section_prefix = models.CharField(max_length=1,null=True, blank=True,)

    boardpolicysection_taxonomy_node = models.OneToOneField(Taxonomy, db_column='boardpolicysection_taxonomy_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'taxonomy_boardpolicysection'
        get_latest_by = 'update_date'
        permissions = (('trash_boardpolicysection', 'Can soft delete board policy section'),('restore_boardpolicysection', 'Can restore board policy section'))
        verbose_name = 'Board Policy Section'
        verbose_name_plural = 'Board Policy Sections'
        default_manager_name = 'objects'

    def __str__(self):
        return self.title

    save = apps.common.functions.taxonomysave
    delete = apps.common.functions.modeltrash
