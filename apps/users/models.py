from django.db import models
from django.conf import settings
import uuid
from django.db.models import Q
import apps.common.functions as commonfunctions
from apps.objects.models import Node, User


class Employee(User):

    PARENT_TYPE = ''
    PARENT_URL = '/accounts/employees/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = True

    title = models.CharField(
        max_length=200,
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

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class System(User):

    PARENT_TYPE = ''
    PARENT_URL = '/accounts/system/'
    URL_PREFIX = ''
    HAS_PERMISSIONS = False

    title = models.CharField(
        max_length=200,
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

    save = commonfunctions.modelsave
    delete = commonfunctions.modeltrash


class PageEditor(models.Model):

    uuid = models.UUIDField(
      primary_key=True,
      unique=True,
      default=uuid.uuid4,
      editable=False,
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='users_pageeditor_employee',
    )
    related_node = models.ForeignKey(
        Node,
        blank=True,
        null=True,
        related_name='users_pageeditor_node',
        editable=False,
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    create_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='objects_pageeditor_create_user',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        to_field='uuid',
        on_delete=models.DO_NOTHING,
        related_name='objects_pageeditor_update_user',
    )
    deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        db_table = 'users_pageeditor'
        get_latest_by = 'create_date'
        verbose_name = 'Page Editor'
        verbose_name_plural = 'Page Editors'

    def __str__(self):
        return '{0}'.format(self.employee.username)
