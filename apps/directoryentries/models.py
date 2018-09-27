from django.db import models
from ckeditor.fields import RichTextField
import apps.common.functions as commonfunctions
from apps.objects.models import Node, DirectoryEntry
from apps.users.models import Employee
from apps.taxonomy.models import (
    SchoolAdministratorType,
    City,
    State,
    Zipcode,
    BoardPrecinct,
    SubjectGradeLevel,
)
from apps.taxonomy.models import Location
from apps.dashboard.models import PageLayout


class SchoolAdministrator(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/schooladministrators/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='directoryenties_schooladministrator_employee',
    )
    schooladministratortype = models.ForeignKey(
        SchoolAdministratorType,
        on_delete=models.CASCADE,
        related_name=('directoryenties_schooladministrator'
                      '_schooladministratortype'),
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='directoryentries_schooladministrator_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schooladministrator_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='schooladministrator_directoryentry_node',
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
        db_table = 'directoryenties_schooladministrator'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'School Administrator'
        verbose_name_plural = 'School Administrators'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.employee.title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Administrator(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/administrators/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='directoryenties_administrator_employee',
    )
    job_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='directoryentries_administrator_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    administrator_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='administrator_directoryentry_node',
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
        db_table = 'directoryenties_administrator'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.employee.title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class Staff(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/staff/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='directoryenties_staff_employee',
    )
    job_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='directoryentries_staff_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    staff_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='staff_directoryentry_node',
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
        db_table = 'directoryenties_staff'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.employee.title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardMember(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/boardmembers/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='directoryenties_boardmember_employee',
    )
    is_president = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='President',
    )
    is_vicepresident = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Vice President',
    )
    precinct = models.ForeignKey(
        BoardPrecinct,
        on_delete=models.PROTECT,
        related_name='directoryenties_boardmember_precinct',
    )
    phone = models.CharField(
        max_length=11,
        help_text='',
    )
    street_address = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        unique=True,
        help_text='',
    )
    city = models.ForeignKey(
        City,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='directoryenties_boardmember_city',
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
    )
    state = models.ForeignKey(
        State,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='directoryenties_boardmember_state',
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
    )
    zipcode = models.ForeignKey(
        Zipcode,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='directoryenties_boardmember_zipcode',
        limit_choices_to={
            'deleted': False,
        },
        help_text='',
    )
    term_ends = models.DateTimeField(
        default=commonfunctions.december_thirty_first,
        unique=False,
        verbose_name="Term Ends",
        null=True,
        blank=True,
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='directoryentries_boardmember_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    boardmember_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='boardmember_directoryentry_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'directoryenties_boardmember'
        get_latest_by = 'create_date'
        verbose_name = 'Board Member'
        verbose_name_plural = 'Board Members'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.employee.title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class StudentBoardMember(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/studentboardmember/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text='',
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text='',
        verbose_name='Last Name',
    )
    phone = models.CharField(
        max_length=11,
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
        related_name='directoryentries_studentboardmember_building_location',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='directoryentries_studentboardmember_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    studentboardmember_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='studentboardmember_directoryentry_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'directoryenties_studentboardmember'
        get_latest_by = 'create_date'
        verbose_name = 'Student Board Member'
        verbose_name_plural = 'Student Board Members'
        default_manager_name = 'base_manager'

    def force_title(self):
        return 'Student Board Member'

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class BoardPolicyAdmin(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/boardpolicyadmins/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='directoryenties_boardpolicyadmin_employee',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='directoryentries_boardpolicyadmin_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    boardpolicyadmin_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='boardpolicyadmin_directoryentry_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'directoryenties_boardpolicyadmin'
        get_latest_by = 'create_date'
        verbose_name = 'Board Policy Administrator'
        verbose_name_plural = 'Board Policy Administrators'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.employee.title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolAdministration(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = '/school-administration/'
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text='',
        verbose_name='About Me',
    )
    employee = models.ForeignKey(
        Employee,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='directoryenties_schooladministration_employee',
    )
    related_node = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        related_name='directoryentries_schooladministration_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schooladministration_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='schooladministration_directoryentry_node',
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
        db_table = 'directoryenties_schooladministration'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'School Administrator'
        verbose_name_plural = 'School Administration'
        default_manager_name = 'base_manager'

    def force_title(self):
        return self.employee.title

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolStaff(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text='',
        verbose_name='About Me',
    )
    employee = models.ForeignKey(
        Employee,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='directoryenties_schoolstaff_employee',
    )
    related_node = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        related_name='directoryentries_schoolstaff_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schoolstaff_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='schoolstaff_directoryentry_node',
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
        db_table = 'directoryenties_schoolstaff'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'School Staff'
        verbose_name_plural = 'School Staff'
        default_manager_name = 'base_manager'

    def force_title(self):
        return 'School Staff: {0} {1}'.format(
            self.employee.first_name,
            self.employee.last_name,
        )

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolFaculty(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False
    PAGELAYOUT = '{0}'.format(
        PageLayout.objects.get_or_create(
            namespace='school-faculty-my-page.html',
            defaults={'title': 'School Faculty My Page'}
        )[0].pk
    )

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text='',
        verbose_name='About Me',
    )
    employee = models.ForeignKey(
        Employee,
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name='directoryenties_schoolfaculty_employee',
    )

    primary_subject = models.ForeignKey(
        SubjectGradeLevel,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='directoryenties_schoolfaculty_primary_subject'
    )

    additional_subjects = models.ManyToManyField(
        SubjectGradeLevel,
        blank=True,
        related_name='directoryenties_schoolfaculty_additional_subjects',
        verbose_name='Additional Subjects',
    )

    related_node = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        related_name='directoryentries_schoolfaculty_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schoolfaculty_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='schoolfaculty_directoryentry_node',
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
        db_table = 'directoryenties_schoolfaculty'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'School Faculty'
        verbose_name_plural = 'School Faculty'
        default_manager_name = 'base_manager'

    def force_title(self):
        return 'School Faculty: {0} {1}'.format(
            self.employee.first_name,
            self.employee.last_name,
        )

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class SchoolCommunityCouncilMember(DirectoryEntry):

    PARENT_TYPE = ''
    PARENT_URL = ''
    URL_PREFIX = ''
    HAS_PERMISSIONS = False
    PAGELAYOUT = '{0}'.format(
        PageLayout.objects.get_or_create(
            namespace='school-community-council-member.html',
            defaults={'title': 'School Community Council Member'}
        )[0].pk
    )

    title = models.CharField(
        max_length=200,
        help_text='',
    )
    first_name = models.CharField(
        null=True,
        blank=False,
        max_length=100,
        verbose_name='First Name',
        help_text='',
    )
    last_name = models.CharField(
        null=True,
        blank=False,
        max_length=100,
        verbose_name='Last Name',
        help_text='',
    )
    role = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Role',
        help_text='',
    )
    email = models.EmailField(
        null=True,
        blank=True,
        max_length=254,
        verbose_name='Email Address',
    )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=11,
        verbose_name='Phone Number',
        help_text='',
    )

    related_node = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        related_name='directoryentries_schoolcommunitycouncilmember_node',
        editable=False,
        on_delete=models.CASCADE,
    )

    schoolcommunitycouncilmember_directoryentry_node = models.OneToOneField(
        DirectoryEntry,
        db_column='schoolcommunitycouncilmember_directoryentry_node',
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
        db_table = 'directoryenties_schoolcommunitycouncilmember'
        ordering = [
            'inline_order',
        ]
        get_latest_by = 'create_date'
        verbose_name = 'School Community Council Member'
        verbose_name_plural = 'School Community Council Members'
        default_manager_name = 'base_manager'

    def force_title(self):
        return '{0} {1}'.format(
            self.first_name,
            self.last_name,
        )

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash
