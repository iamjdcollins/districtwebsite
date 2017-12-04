from django.db import models
from apps.objects.models import Node, DirectoryEntry
from apps.users.models import Employee
from apps.taxonomy.models import SchoolAdministratorType, City, State, Zipcode, BoardPrecinct
import apps.common.functions
from apps.taxonomy.models import Location

class SchoolAdministrator(DirectoryEntry):
  PARENT_URL = ''
  URL_PREFIX = '/directory/schooladministrator/'

  title = models.CharField(max_length=200, help_text='')
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='directoryenties_schooladministrator_employee')
  schooladministratortype = models.ForeignKey(SchoolAdministratorType, on_delete=models.CASCADE, related_name='directoryenties_schooladministrator_schooladministratortype')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='directoryentries_schooladministrator_node', editable=False)


  schooladministrator_directoryentry_node = models.OneToOneField(DirectoryEntry, db_column='schooladministrator_directoryentry_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'directoryenties_schooladministrator'
    get_latest_by = 'create_date'
    verbose_name = 'School Administrator'
    verbose_name_plural = 'School Administrators'
    default_manager_name = 'objects'
 
  save = apps.common.functions.directoryentrysave
  delete = apps.common.functions.modeltrash

class Staff(DirectoryEntry):
  PARENT_URL = ''
  URL_PREFIX = '/directory/staff/'

  title = models.CharField(max_length=200, help_text='')
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='directoryenties_staff_employee')
  job_title =  models.CharField(max_length=200, help_text='')
  related_node = models.ForeignKey(Node, blank=True, null=True, related_name='directoryentries_staff_node', editable=False)


  staff_directoryentry_node = models.OneToOneField(DirectoryEntry, db_column='staff_directoryentry_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

  class Meta:
    db_table = 'directoryenties_staff'
    get_latest_by = 'create_date'
    verbose_name = 'Staff'
    verbose_name_plural = 'Staff'
    default_manager_name = 'objects'

  save = apps.common.functions.directoryentrysave
  delete = apps.common.functions.modeltrash

class BoardMember(DirectoryEntry):
    PARENT_URL = ''
    URL_PREFIX = '/directory/boardmember/'

    title = models.CharField(max_length=200, help_text='')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='directoryenties_boardmember_employee')
    precinct = models.ForeignKey(BoardPrecinct, on_delete=models.PROTECT, related_name='directoryenties_boardmember_precinct')
    phone = models.CharField(max_length=11, help_text='')
    street_address = models.CharField(max_length=200, null=True, blank=True, unique=True, help_text='')
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.PROTECT, related_name='directoryenties_boardmember_city', limit_choices_to={'deleted': False,}, help_text='')
    state = models.ForeignKey(State, null=True, blank=True, on_delete=models.PROTECT, related_name='directoryenties_boardmember_state', limit_choices_to={'deleted': False,}, help_text='')
    zipcode = models.ForeignKey(Zipcode, null=True, blank=True, on_delete=models.PROTECT, related_name='directoryenties_boardmember_zipcode', limit_choices_to={'deleted': False,}, help_text='')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='directoryentries_boardmember_node', editable=False)


    boardmember_directoryentry_node = models.OneToOneField(DirectoryEntry, db_column='boardmember_directoryentry_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'directoryenties_boardmember'
        get_latest_by = 'create_date'
        verbose_name = 'Board Member'
        verbose_name_plural = 'Board Members'
        default_manager_name = 'objects'

    save = apps.common.functions.directoryentrysave
    delete = apps.common.functions.modeltrash

class StudentBoardMember(DirectoryEntry):
    PARENT_URL = ''
    URL_PREFIX = '/directory/studentboardmember/'

    title = models.CharField(max_length=200, help_text='')
    first_name = models.CharField(max_length=30, null=True, blank=True, help_text='', verbose_name='First Name')
    last_name =  models.CharField(max_length=30, null=True, blank=True, help_text='', verbose_name='Last Name')
    phone = models.CharField(max_length=11, null=True, blank=True, help_text='')
    building_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT, limit_choices_to={'deleted': False,}, help_text='', related_name='directoryentries_studentboardmember_building_location')
    related_node = models.ForeignKey(Node, blank=True, null=True, related_name='directoryentries_studentboardmember_node', editable=False)


    studentboardmember_directoryentry_node = models.OneToOneField(DirectoryEntry, db_column='studentboardmember_directoryentry_node', on_delete=models.CASCADE, parent_link=True,editable=False,)

    class Meta:
        db_table = 'directoryenties_studentboardmember'
        get_latest_by = 'create_date'
        verbose_name = 'Student Board Member'
        verbose_name_plural = 'Student Board Members'
        default_manager_name = 'objects'

    save = apps.common.functions.directoryentrysave
    delete = apps.common.functions.modeltrash
