from django.db import models
from django.db.models import Q
import apps.common.functions
from apps.objects.models import Node, User


class Employee(User):
    PARENT_URL = '/accounts/employees/'

    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
        db_index=True,
    )
    department = models.ForeignKey(
        Node,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to=Q(content_type='school') |
        Q(content_type='department'),
        related_name='users_employee_department',
    )
    job_title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
    )
    non_employee = models.BooleanField(
        default=False,
        db_index=True,
    )
    in_directory = models.BooleanField(
        default=False,
        db_index=True,
    )

    employee_user_node = models.OneToOneField(
        User,
        db_column='employee_user_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'users_employee'
        get_latest_by = 'create_date'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def force_title(self):
        return str(self.email).split('@', 1)[0]

    save = apps.common.functions.usersave
    delete = apps.common.functions.modeltrash


class System(User):
    PARENT_URL = '/accounts/system/'

    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='',
        db_index=True,
    )

    system_user_node = models.OneToOneField(
        User,
        db_column='system_user_node',
        on_delete=models.CASCADE,
        parent_link=True,
        editable=False,
    )

    class Meta:
        db_table = 'users_system'
        get_latest_by = 'create_date'
        verbose_name = 'System'
        verbose_name_plural = 'System'

    def force_title(self):
        return str(self.email).split('@', 1)[0]

    save = apps.common.functions.usersave
    delete = apps.common.functions.modeltrash
